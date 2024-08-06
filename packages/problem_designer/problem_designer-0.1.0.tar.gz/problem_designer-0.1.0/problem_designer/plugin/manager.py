import importlib
import logging
from typing import Generic, TypeVar

import pluggy

# import the default namespace package... ignore linting here
from problem_designer import problems  # type: ignore
from problem_designer.plugin.helper import (
    build_mapping_dict,
    iter_namespace,
    load_entrypoints,
)
from problem_designer.plugin.typedef import HookContainer
from problem_designer.typedef.plugin import (
    DesignHookConstants,
    DesignHookSpec,
    DesignSpecPlugin,
    GeneratorHookConstants,
    GeneratorHookSpec,
    GeneratorPlugin,
)

logger = logging.getLogger(__name__)


class HookManager:
    """
    Provides a base for loading and discovering hooks / plugins.
    """

    def __init__(
        self,
        hook_namespace: str,
        hook_specs: list[HookContainer],
        additional_hooks: list[HookContainer] | None = None,
        entrypoint_group: str | None = None,
        namespace_pkg: HookContainer | None = None,
    ):
        """
        Args:
            hook_namespace: The namespace / project name of the hook
            hook_specs: A list of object (modules or classes) defining hooks
            additional_hooks: Load these hooks in specific. Must be a module or class
            entrypoint_group: If set checks entrypoints for any relevant hooks. Automatically tries to load any hook's
            namespace_pkg: Checks the subpackages of the given namespace package for any hooks (in __main__.py of the
            subpackage)
        """
        # setup plugin manager
        self._pm = pluggy.PluginManager(hook_namespace)

        # load specs
        for hook_spec in hook_specs:
            self._pm.add_hookspecs(hook_spec)

        # variable init
        self._hook_specs = hook_specs
        self._hook_namespace = hook_namespace
        self._additional_hooks = additional_hooks
        self._entrypoint_group = entrypoint_group
        self._namespace_pkg = namespace_pkg
        self.loaded_plugins = None

        # load hooks
        if entrypoint_group:
            self._load_hooks_from_entrypoint_group()
        if namespace_pkg:
            self._load_hooks_from_namespace_package(namespace_pkg)

    def _load_hooks_from_namespace_package(self, package):
        """
        Automatically load hook implementations from a namespace package. The package is scanned and any module
        in it is registered in the plugin manager. Any hook in the __init__.py will be collected.
        Args:
            package: Imported package which needs to be scanned.
        """
        discovered_plugins = {name: importlib.import_module(name) for finder, name, is_pkg in iter_namespace(package)}
        for subpackage_name, module in discovered_plugins.items():
            logger.debug(f"Discovered {subpackage_name}.")
            try:
                self._pm.register(module)
            except ValueError as e:
                logger.error(e)

    def _load_hooks_from_entrypoint_group(self):
        """
        Discover plugins using entrypoints. These are defined in the pyproject.toml of another package.
        The entrypoint group is used to filter these. Same style as pytest. Discovered entry points are
        automatically fed to the plugin manager
        """
        entry_points = load_entrypoints(self._entrypoint_group)
        for entry_point in entry_points:
            try:
                self._pm.register(entry_point.load())
            except ValueError as e:
                logger.error(e)

    def _run_hooks(self):
        """
        Implementation of the hook call process
        """
        raise NotImplementedError


PluginT = TypeVar("PluginT")


class PluginManager(HookManager, Generic[PluginT]):
    """
    Handles loading of plugins and building a mapping dict (mapping global name to plugin)
    """

    def get_plugins(self) -> dict[str, PluginT] | None:
        return self.loaded_plugins


class DesignSpecManager(PluginManager[DesignSpecPlugin]):
    """
    A preconfigured plugin manager which picks up any design plugins.
    """

    def __init__(
        self,
        additional_hooks: list[HookContainer] | None = None,
    ):
        super().__init__(
            DesignHookConstants.namespace,
            [DesignHookSpec],
            additional_hooks,
            DesignHookConstants.entrypoint_group,
            problems,
        )
        self.loaded_plugins = None
        self._run_hooks()

    def _run_hooks(self):
        """
        Loads and builds the definition dict
        """
        self.loaded_plugins = build_mapping_dict(self._pm.hook.register_spec())


class GeneratorManager(PluginManager[GeneratorPlugin]):
    """
    A preconfigured plugin manager which picks up any generation plugins.
    """

    def __init__(
        self,
        additional_hooks: list[HookContainer] | None = None,
    ):
        super().__init__(
            GeneratorHookConstants.namespace,
            [GeneratorHookSpec],
            additional_hooks,
            GeneratorHookConstants.entrypoint_group,
            problems,
        )
        self.loaded_plugins = None
        self._run_hooks()

    def _run_hooks(self):
        """
        Loads and builds the definition dict
        """
        self.loaded_plugins = build_mapping_dict(self._pm.hook.register_generator())
