"""
This is the cli interface for the reqconfig extension.
Given the interface is very different from the other *ctl commands,
We don't necessarily derive it from the base cli tools.
"""

import argparse
import difflib
import ipaddress
import logging
import pathlib
import re
from typing import Any, Dict, Generator, List, Optional, Tuple

import pyparsing as pp
import yaml
from wmflib.interactive import AbortError, ask_confirmation

from conftool import configuration, yaml_safe_load
from conftool.cli import ConftoolClient
from conftool.drivers import BackendError
from conftool.extensions.reqconfig.translate import (
    VCLTranslator,
    VSLTranslator,
    HAProxyACLTranslator,
    HAProxyDSLTranslator,
)
from conftool.kvobject import Entity

from . import view
from .schema import SCHEMA, get_obj_from_slug, SYNC_ENTITIES
from .error import RequestctlError

irc = logging.getLogger("reqctl.announce")
logger = logging.getLogger("reqctl")
# Actions are special entities, we will need to check them constantly
ACTION_ENTITIES = ["action", "haproxy_action"]
# Mapping of commands to entities. This is used to determine the entity type
# If the list is empty, the object type will be determined from the command line.
CMD_TO_ENTITY = {
    "validate": [],
    "sync": [],
    "dump": [],
    "enable": ACTION_ENTITIES,
    "disable": ACTION_ENTITIES,
    "get": [],
    "vcl": ["action"],
    "log": ["action"],
    "find": ACTION_ENTITIES,
    "find-ip": ["ipblock"],
    "commit": ACTION_ENTITIES,
    "haproxycfg": ["haproxy_action"],
}


SCOPE_TO_ENTITY = {
    "varnish": ["action"],
    "haproxy": ["haproxy_action"],
}


class Requestctl:
    """Cli tool to interact with the dynamic banning of urls."""

    def __init__(self, args: argparse.Namespace) -> None:
        if args.debug:
            lvl = logging.DEBUG
        else:
            lvl = logging.INFO
        logging.basicConfig(
            level=lvl,
            format="%(asctime)s - %(name)s "
            "(%(module)s:%(funcName)s:%(lineno)d) - %(levelname)s - %(message)s",
        )
        self.args = args
        # Now let's load the schema
        self.client = ConftoolClient(
            configfile=self.args.config,
            config=None if self.args.config else configuration.Config(),
            schema=SCHEMA,
            irc_logging=False,
        )
        self.schema = self.client.schema
        # Load the right entities
        self.classes = {obj: self.client.get(obj) for obj in self.object_types}
        # If we only have one entity, we can use it directly
        if len(self.classes) == 1:
            self.cls = list(self.classes.values())[0]
        else:
            self.cls = None
        if "git_repo" in self.args and self.args.git_repo is not None and self.cls is not None:
            self.base_path: Optional[pathlib.Path] = (
                pathlib.Path(self.args.git_repo) / self.cls.base_path()
            )
        else:
            self.base_path = None
        # Load the parsing grammar. If the command is validate, use on-disk check of existence for
        # patterns.
        # Otherwise, check on the datastore.
        if self.args.command == "validate":
            self._obj_exist = self._is_obj_on_fs
        else:
            self._obj_exist = self._is_obj_on_backend
        self.expression_grammar = self.grammar()

    @property
    def object_types(self) -> List[str]:
        """The object type we're operating on."""
        if self.args.command not in CMD_TO_ENTITY:
            raise RequestctlError(
                f"Command {self.args.command} not listed in Requestctl.CMD_TO_ENTITY"
            )
        # If we don't have forced values for the specific command, we expect an object type
        # to be passed in the command line.
        if not CMD_TO_ENTITY[self.args.command]:
            return [self.args.object_type]

        # To make things more user-friendly, we sometimes allow selecting a "scope" of objects
        if "scope" in self.args and self.args.scope in SCOPE_TO_ENTITY:
            return SCOPE_TO_ENTITY[self.args.scope]
        # Otherwise we return the values from the mapping
        return CMD_TO_ENTITY[self.args.command]

    def run(self):
        """Runs the action defined in the cli args."""
        try:
            command = getattr(self, self.args.command.replace("-", "_"))
        except AttributeError as e:
            raise RequestctlError(f"Command {self.args.command} not implemented") from e

        # TODO: add support to let a custom exit code surface, for example for
        # "failed successfully" operations
        command()

    def validate(self):
        """Scans a directory, checks validity of the objects.

        Raises an exception if invalid objects have been found.
        """
        # The code is quite similar to the one in sync; however abstracting it
        # gets ugly fast. I chose code readability over DRY here consciously.
        root_path = pathlib.Path(self.args.basedir)
        failed = False
        for obj_type in SYNC_ENTITIES:
            self.cls = self.client.get(obj_type)
            for tag, fpath in self._get_files_for_object_type(root_path, obj_type):
                obj, from_disk = self._entity_from_file(tag, fpath)
                try:
                    self._verify_change(from_disk, obj_type)
                except RequestctlError as e:
                    failed = True
                    logger.error("%s %s is invalid: %s", obj_type, obj.pprint(), e)
                    continue
        if failed:
            raise RequestctlError("Validation failed, see above.")

    def sync(self):
        """Synchronizes entries for an entity from files on disk."""
        # Let's keep things simple, we only have one layer of tags
        # for request objects.
        failed = False
        # Set cls to the right entity
        self.cls = self.client.get(self.args.object_type)
        for tag, fpath in self._get_files_for_object_type(
            pathlib.Path(self.args.git_repo), self.args.object_type
        ):
            obj, from_disk = self._entity_from_file(tag, fpath)
            try:
                to_load = self._verify_change(from_disk, self.args.object_type)
            except RequestctlError as e:
                failed = True
                logger.error("Error parsing %s, skipping: %s", obj.pprint(), e)
                continue
            changes = self._object_diff(obj, to_load)
            if changes:
                try:
                    self._write(obj, to_load)
                except BackendError as e:
                    logger.error("Error writing to etcd for %s: %s", obj.pprint(), e)
                    failed = True
                    continue

        # If we're not purging, let's stop here.
        if not self.args.purge:
            if failed:
                raise RequestctlError(
                    "synchronization had issues, please check the output for details."
                )
            return

        # Now let's find any object that is in the datastore and not on disk.
        # Given how query is implemented, it's better to just search for all objects
        # and check everything in one go.
        # Given we also need to check consistency, we need all actions too.
        action_types = ["action", "haproxy_action"]
        all_actions = []
        if not set(self.object_types) & set(action_types):
            for obj_type in action_types:
                for action in self.client.get(obj_type).query({"name": re.compile(".*")}):
                    all_actions.append(action)

        for reqobj in self.cls.query({"name": re.compile(".*")}):
            if not self._should_have_path(reqobj).is_file():
                if not self._is_safe_to_remove(reqobj, all_actions):
                    failed = True
                    continue
                if self.args.interactive:
                    try:
                        ask_confirmation(f"Proceed to delete {reqobj}?")
                    except AbortError:
                        continue
                logger.info("Deleting %s", reqobj.name)
                reqobj.delete()

        if failed:
            raise RequestctlError(
                "synchronization had issues, please check the output for details."
            )

    def dump(self):
        """Dump an object type."""
        if self.cls is None:
            raise RequestctlError(
                "No object type selected for dumping. This is a bug, please report it."
            )
        for reqobj in self.cls.query({"name": re.compile(".*")}):
            object_path = self.base_path / f"{reqobj.pprint()}.yaml"
            object_path.absolute().parent.mkdir(parents=True, exist_ok=True)
            contents = reqobj.asdict()[reqobj.name]
            object_path.write_text(yaml.dump(contents))

    def enable(self):
        """Enable an action."""
        self._enable(True)

    def disable(self):
        """Disable an action."""
        self._enable(False)

    def get(self):
        """Get an object, or an entire class of them, print them out."""
        # We should only call this when a class is selected
        if self.cls is None:
            raise RequestctlError(
                "No object type selected for getting. This is a bug, please report it."
            )
        self._pprint(self._get())

    def log(self):
        """Print out the varnishlog command corresponding to the selected action."""
        objs = self._get(must_exist=True)
        objs[0].vsl_expression = self._vsl_from_expression(objs[0].expression)
        print(view.get("vsl").render(objs, "action"))

    def find(self):
        """Find actions that correspond to the searched pattern."""
        pattern = f"pattern@{self.args.search_string}"
        ipblock = f"ipblock@{self.args.search_string}"
        matches = 0
        for action in self._get():
            tokens = self._parse_and_check(action.expression)
            if pattern in tokens or ipblock in tokens:
                matches += 1
                object_type = self._get_object_type_from_entity(action)
                print(f"{object_type}: {action.pprint()}, expression: {action.expression}")
        if not matches:
            print("No entries found.")

    def find_ip(self):
        """Find if the given IP is part of any IP block on disk."""
        # TODO: mayybe search on the datastore?
        if self.base_path is None:
            raise RequestctlError("No git repo specified, cannot search for IP blocks.")
        ip = ipaddress.ip_address(self.args.ip)
        found = False
        for file in self.base_path.glob("**/*.yaml"):
            content = yaml_safe_load(file, {})
            for prefix in content["cidrs"]:
                if ip in ipaddress.ip_network(prefix):
                    found = True
                    ipblock = file.relative_to(self.base_path).with_suffix("")
                    print(f"IP {ip} is part of prefix {prefix} in ipblock {ipblock}")

        if not found:
            print(f"IP {ip} is not part of any ipblock on disk")

    def vcl(self):
        """Print out the VCL for a specific action."""
        objs = self._get(must_exist=True)
        objs[0].vcl_expression = self._vcl_from_expression(objs[0].expression)
        print(view.get("vcl").render(objs, "vcl"))

    def haproxycfg(self):
        """Print out the haproxy config for a specific action."""
        haproxy_actions = self._get(must_exist=True)
        print(self._get_haproxy_config_from_actions(haproxy_actions))

    def _get_haproxy_config_from_actions(self, haproxy_actions: List[Entity]) -> str:
        translator = HAProxyDSLTranslator(self.schema)
        # Check and parse the haproxy actions
        for haproxy_action in haproxy_actions:
            haproxy_action.parsed_expression = self._parse_and_check(haproxy_action.expression)

        # Now translate them to acls and add the haproxy_expression property
        acls = translator.acls_from_actions(haproxy_actions)
        for haproxy_action in haproxy_actions:
            haproxy_action.haproxy_expression = translator.from_expression(
                haproxy_action.parsed_expression
            )
        return view.get("haproxycfg").render(haproxy_actions, acls)

    def commit(self):
        """Commit the enabled actions to the DSLs, asking confirmation with a diff."""
        # All the actions that are not disabled or without log_matching, organized by
        # cluster and type
        batch: bool = self.args.batch
        vcl_actions, haproxy_actions = self._get_actions_by_site_and_type()
        if not batch:
            print("### Varnish VCL changes ###")
        self._commit_vcl(vcl_actions, batch)
        if not batch:
            print("### HAProxy DSL changes ###")
        self._commit_haproxy(haproxy_actions, batch)

    # End public interface
    def _commit_vcl(self, vcl_actions: Dict[str, Dict[str, List[Entity]]], batch: bool):
        batch = self.args.batch
        vcl = self.client.get("vcl")
        for cluster, entries in vcl_actions.items():
            for name, actions in entries.items():
                vcl_content = view.get("vcl").render(actions, "commit")
                obj = vcl(cluster, name)
                if not batch:
                    if obj.exists:
                        prev_vcl = obj.vcl
                    else:
                        prev_vcl = ""
                    if not self._confirm_diff(prev_vcl, vcl_content, obj.pprint()):
                        continue
                obj.vcl = vcl_content
                obj.write()
        # Now clean up things that are leftover
        for rules in vcl.query({"name": re.compile(".*")}):
            cluster = rules.tags["cluster"]
            if rules.name not in vcl_actions[cluster]:
                # ask confirmation if not in batch mode
                if not batch and not self._confirm_diff(rules.vcl, "", rules.pprint()):
                    continue

                rules.update({"vcl": ""})

    def _commit_haproxy(self, haproxy_actions: Dict[str, Dict[str, List[Entity]]], batch: bool):
        haproxy_dsl = self.client.get("haproxy_dsl")
        for cluster, entries in haproxy_actions.items():
            # Here we have a complication. We need to calculate the ACLs
            # for each site combining global and local actions.
            # So we will show the diff for each site.
            for site, actions in entries.items():
                all_actions = []
                all_actions.extend(actions)
                if site != "global":
                    all_actions.extend(haproxy_actions[cluster]["global"])
                haproxy_content = self._get_haproxy_config_from_actions(all_actions)
                site_cfg = haproxy_dsl(cluster, site)
                if not batch:
                    if site_cfg.exists:
                        prev_haproxy = site_cfg.dsl
                    else:
                        prev_haproxy = ""
                    if not self._confirm_diff(prev_haproxy, haproxy_content, site_cfg.pprint()):
                        continue
                site_cfg.dsl = haproxy_content
                site_cfg.write()

        # Now clean up leftovers.
        # In haproxy, we expect site-specific configurations to include the global
        # one, so we cannot just delete the dsl entry. We will need to delete the object alltogether
        # if there is no enabled action there, so that we fallback to the global config.
        for rules in haproxy_dsl.query({"name": re.compile(".*")}):
            cluster = rules.tags["cluster"]
            if rules.name not in haproxy_actions[cluster]:
                # ask confirmation if not in batch mode
                if not batch and not self._confirm_diff(rules.dsl, "", rules.pprint()):
                    continue
                rules.delete()

    def _get_files_for_object_type(
        self, root_path: pathlib.Path, obj_type: str
    ) -> Generator[Tuple[str, pathlib.Path], None, None]:
        """Gets files in a directory that can contain objects."""
        entity_path: pathlib.Path = root_path / self.client.get(obj_type).base_path()
        for tag_path in entity_path.iterdir():
            # skip files in the root dir, including any hidden dirs and the special
            # .. and . references
            if not tag_path.is_dir() or tag_path.parts[-1].startswith("."):
                continue
            tag = tag_path.name
            for fpath in tag_path.glob("*.yaml"):
                yield (tag, fpath)

    def _confirm_diff(self, old: str, new: str, slug: str) -> bool:
        """Confirm if a change needs to be carried on or not."""
        diff = self._dsl_diff(old, new, slug)
        if not diff:
            return False
        print(diff)
        try:
            ask_confirmation("Ok to commit these changes?")
        except AbortError:
            return False
        return True

    def _dsl_diff(self, old: str, new: str, slug: str) -> str:
        """Diffs between two pieces of DSL."""
        if old == "":
            fromfile = "null"
        else:
            fromfile = f"{slug}.old"
        if new == "":
            tofile = "null"
        else:
            tofile = f"{slug}.new"
        return "".join(
            [
                line + "\n"
                for line in difflib.unified_diff(
                    old.splitlines(), new.splitlines(), fromfile=fromfile, tofile=tofile
                )
            ]
        )

    def _get(self, must_exist: bool = False) -> List[Entity]:
        """Get an object, or all of them, return them as a list."""
        objs = []
        has_path = "object_path" in self.args and self.args.object_path

        for cls in self.classes.values():
            if has_path:
                obj = get_obj_from_slug(cls, self.args.object_path)
                if obj.exists:
                    objs.append(obj)
            else:
                objs.extend(cls.query({"name": re.compile(".")}))
        if must_exist and has_path and not objs:
            raise RequestctlError(
                f"{list(self.classes.keys())} '{self.args.object_path}' not found."
            )

        return objs

    def _enable(self, enable: bool):
        """Ban a type of request."""
        for cls in self.classes.values():
            action = get_obj_from_slug(cls, self.args.action)
            if not action.exists:
                continue
            action.update({"enabled": enable})
            # Printing this unconditionally *might* be confusing, as there's nothing to commit if
            # enabling an already-enabled action. So we could check first, with action.changed(),
            # but it probably isn't worth the extra roundtrip.
            print("Remember to commit the change with: sudo requestctl commit")
            return

        # If we got here, the action was not found.
        raise RequestctlError(f"{self.args.action} does not exist, cannot enable/disable.")

    def _parse_and_check(self, expression) -> List[str]:
        """Parse the expression and check if it's valid at all.

        If the expression is not balanced, or has references to inexistent ipblocks or patterns,
        an error will be raised.
        """
        parsed = self.expression_grammar.parseString(expression, parseAll=True)
        # If this didn't raise an exception, the string was valid. Now let's put it in normalized
        # form like it needs to be in etcd

        def flatten(parse):
            res = []
            for el in parse:
                if isinstance(el, list):
                    res.extend(flatten(el))
                else:
                    res.append(el)
            return res

        return flatten(parsed.asList())

    def grammar(self) -> pp.Forward:
        """
        Pyparsing based grammar for expressions in actions.

        BNF of the grammar:
        <grammar> ::= <item> | <item> <boolean> <grammar>
        <item> ::= <pattern> | <ipblock> | "(" <grammar> ")"
        <pattern> ::= "pattern@" <pattern_path>
        <ipblock> ::= "ipblock@"<ipblock_path>
        <boolean> ::= "AND" | "OR" | "AND NOT" | "OR NOT"

        """
        boolean = (
            pp.Keyword("AND NOT") | pp.Keyword("OR NOT") | pp.Keyword("AND") | pp.Keyword("OR")
        )
        lpar = pp.Literal("(")
        rpar = pp.Literal(")")
        element = pp.Word(pp.alphanums + "/-_")
        pattern = pp.Combine("pattern@" + element.setParseAction(self._validate_pattern))
        ipblock = pp.Combine("ipblock@" + element.setParseAction(self._validate_ipblock))
        grm = pp.Forward()
        item = pattern | ipblock | lpar + grm + rpar
        grm << pp.Group(item) + pp.ZeroOrMore(pp.Group(boolean + item))
        return grm

    def _validate_pattern(self, _all, _pos, tokens):
        """Ensure a pattern referenced exists."""
        for pattern in tokens:
            if not self._obj_exist("pattern", pattern):
                msg = f"The pattern {pattern} is not present on the backend."
                logger.error(msg)
                # also raise an exception to make parsing fail.
                raise pp.ParseException(msg)

    def _validate_ipblock(self, _all, _pos, tokens):
        """Ensure an ipblock referenced exists."""
        for ipblock in tokens:
            if not self._obj_exist("ipblock", ipblock):
                msg = f"The ipblock {ipblock} is not present on the backend."
                logger.error(msg)
                raise pp.ParseException(msg)

    def _is_obj_on_backend(self, obj_type: str, slug: str) -> bool:
        """Checks if the pattern exists on the backend."""
        obj = get_obj_from_slug(self.client.get(obj_type), slug)
        return obj.exists

    def _is_obj_on_fs(self, obj_type: str, slug: str) -> bool:
        on_disk: pathlib.Path = (
            pathlib.Path(self.args.basedir) / self.client.get(obj_type).base_path() / f"{slug}.yaml"
        )
        return on_disk.is_file()

    def _pprint(self, entities: List[Entity]):
        """Pretty print the results."""
        # VCL and VSL output modes are only supported for "action"
        # Also, pretty mode is disabled for all but patterns and ipblocks.
        # Actions should be supported, but is temporarily disabled
        #  while we iron out the issues with old versions of tabulate
        output_config = {
            "action": {"allowed": ["vsl", "vcl", "yaml", "json"], "default": "yaml"},
            "haproxy_action": {"allowed": ["yaml", "json", "haproxycfg"], "default": "json"},
            "vcl": {"allowed": ["yaml", "json"], "default": "json"},
            "haproxy_dsl": {"allowed": ["yaml", "json"], "default": "json"},
        }
        # We need output and object type to determine the output format
        if not all([self.args.output, self.args.object_type]):
            raise RequestctlError("Cannot use pprint without output and object type.")
        out = self.args.output
        object_type = self.args.object_type
        if object_type in output_config:
            conf = output_config[object_type]
            if out not in conf["allowed"]:
                out = conf["default"]
        print(view.get(out).render(entities, object_type))

    def _entity_from_file(self, tag: str, file_path: pathlib.Path) -> Tuple[Entity, Optional[Dict]]:
        """Get an entity from a file path, and the corresponding data to update."""
        from_disk = yaml_safe_load(file_path, {})
        entity_name = file_path.stem
        if self.cls is None:
            raise RequestctlError(
                "No entity selected when trying to load from disk."
                "Please ensure self.cls is set before calling this method."
                "This is a bug in the code. If you see this message, please report it."
            )
        entity = self.cls(tag, entity_name)
        return (entity, from_disk)

    def _verify_change(self, changes: Dict[str, Any], object_type: str) -> Dict:
        """
        Verifies a change is ok. Eitehr Raises an exception
        or returns the valid changes.
        """
        if object_type == "pattern":
            if changes.get("body", False) and changes.get("method", "") != "POST":
                raise RequestctlError("Cannot add a request body in a request other than POST.")
        if object_type != "action":
            return changes
        try:
            changes["expression"] = " ".join(self._parse_and_check(changes["expression"]))
        except pp.ParseException as e:
            raise RequestctlError(e) from e
        try:
            # We never sync the enabled state from disk.
            del changes["enabled"]
        except KeyError:
            pass
        return changes

    def _object_diff(self, entity: Entity, to_load: Dict[str, Any]) -> Dict:
        """Asks for confirmation of changes if needed."""
        # find the object type from the entity
        obj_type = self._get_object_type_from_entity(entity).capitalize()
        if entity.exists:
            changes = entity.changed(to_load)
            action = "modify"
            msg = f"{obj_type} {entity.pprint()} will be changed:"
        else:
            action = "create"
            changes = to_load
            msg = f"{obj_type} will be created:"

        if self.args.interactive and changes:
            print(msg)
            for key, value in changes.items():
                print(f"{entity.name}.{key}: '{getattr(entity, key)}' => {value}")
            try:
                ask_confirmation(f"Do you want to {action} this object?")
            except AbortError:
                # act like there were no changes
                return {}
        return changes

    def _write(self, entity: Entity, to_load: Dict[str, Any]):
        """Write the object to the datastore."""
        obj_type = self._get_object_type_from_entity(entity)
        if entity.exists:
            logger.info("Updating %s %s", obj_type, entity.pprint())
            entity.update(to_load)
        else:
            logger.info("Creating %s %s", obj_type, entity.pprint())
            entity.from_net(to_load)
            entity.write()

    def _should_have_path(self, obj: Entity) -> pathlib.Path:
        """Path expected on disk for a specific entity."""
        tag = SCHEMA[self._get_object_type_from_entity(obj)]["tags"][0]
        return self.base_path / obj.tags[tag] / f"{obj.name}.yaml"

    def _is_safe_to_remove(self, entity: Entity, actions: List[Entity]) -> bool:
        """Check if a pattern/ipblock is referenced in any action and thus not safe to remove."""
        object_type = self._get_object_type_from_entity(entity)
        if object_type in ACTION_ENTITIES:
            return True
        expr = f"{object_type}@{entity.pprint()}"
        matches = [r.pprint() for r in actions if expr in r.expression]
        if matches:
            logger.error(
                "Cannot remove %s %s: still referenced in the following actions: %s",
                object_type,
                entity.pprint(),
                ",".join(matches),
            )
            return False
        return True

    def _vsl_from_expression(self, expression: str) -> str:
        parsed = self._parse_and_check(expression)
        vsl = VSLTranslator(self.client.schema)
        return vsl.from_expression(parsed)

    def _vcl_from_expression(self, expression: str) -> str:
        parsed = self._parse_and_check(expression)
        vcl = VCLTranslator(self.client.schema)
        return vcl.from_expression(parsed)

    def _get_actions_by_site_and_type(
        self,
    ) -> Tuple[Dict[str, Dict[str, List[Entity]]], Dict[str, Dict[str, List[Entity]]]]:
        """Get all actions, organized by site and type.

        Organize actions by type, cluster and site, and return a tuple of the
        actions for varnish and haproxy, respectively.

        For VCL generation, we organize them by cache cluster and by site as follows:
        - $cluster/global: all rules that go to all sites for cache misses
        - $cluster/hit-global: all rules that go to all sites for cache hits
        - $cluster/$site: all rules that go to a specific site for cache misses
        - $cluster/hit-$site: all rules that go to a specific site for cache hits

        For HAProxy DSL generation, we organize them by cluster and site as follows:
        - $cluster/$site: all rules that go to a specific site
        - $cluster/global: all rules that go to all sites
        """
        varnish_by_cluster_site = {}
        haproxy_by_cluster_site = {}
        # This will get all actions and haproxy actions
        for action in self._get():
            object_type = self._get_object_type_from_entity(action)
            if not (action.enabled or action.log_matching):
                continue
            if object_type == "action":
                action.vcl_expression = self._vcl_from_expression(action.expression)

            cluster = action.tags["cluster"]
            # Each rule can be global or site specific
            sites = ["global"]
            if action.sites:
                sites = action.sites
            if object_type == "action":
                if cluster not in varnish_by_cluster_site:
                    varnish_by_cluster_site[cluster] = {}

                for site in sites:
                    if not action.cache_miss_only:
                        site = f"hit-{site}"
                    if site not in varnish_by_cluster_site[cluster]:
                        varnish_by_cluster_site[cluster][site] = []
                    varnish_by_cluster_site[cluster][site].append(action)
            elif object_type == "haproxy_action":
                if cluster not in haproxy_by_cluster_site:
                    haproxy_by_cluster_site[cluster] = {}

                for site in sites:
                    if site not in haproxy_by_cluster_site[cluster]:
                        haproxy_by_cluster_site[cluster][site] = []
                    haproxy_by_cluster_site[cluster][site].append(action)

        return varnish_by_cluster_site, haproxy_by_cluster_site

    def _get_object_type_from_entity(self, entity: Entity) -> str:
        """Get the object type from an entity."""
        return entity.__class__.__name__.lower()

    def _collect_haproxy_acl_patterns(
        self, actions: List[Entity]
    ) -> Tuple[str, HAProxyACLTranslator]:
        """Collect all patterns and ipblocks referenced in actions."""
        pattern_label = "pattern@"
        ipblock_label = "ipblock@"
        patterns = set()
        ipblocks = set()
        for action in actions:
            parsed = self._parse_and_check(action.expression)
            for token in parsed:
                if token.startswith(pattern_label):
                    patterns.add(token.replace(pattern_label, ""))
                if token.startswith(ipblock_label):
                    ipblocks.add(token.replace(ipblock_label, ""))
        # Now we have all the patterns and ipblocks, let's get the haproxy dsl for them
        translator = HAProxyACLTranslator(self.schema)
        output = "# ACLs generated by requestctl\n"
        output += translator.from_ipblocks(list(ipblocks))
        output += translator.from_patterns(list(patterns))
        return (output, translator)
