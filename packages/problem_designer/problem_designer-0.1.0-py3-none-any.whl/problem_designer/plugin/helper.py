import importlib
import pkgutil
from importlib.metadata import EntryPoint, entry_points
from types import ModuleType
from typing import TypeVar

from problem_designer.plugin.typedef import Plugin


def load_entrypoints(group: str | None) -> list[EntryPoint]:
    """
    Loads all entry points defined in pyproject.toml from a given group.
    For an example see here: https://docs.pytest.org/en/latest/how-to/writing_plugins.html#pip-installable-plugins
    Args:
        group: The name of the group

    Returns: A list of entrypoints or an empty list
    >>> load_entrypoints(group='non-existing-group')
    []
    """
    return entry_points(group=group)


T = TypeVar("T")


def flatten(iterable: list[T | list[T]]) -> list[T]:
    """
    Flattens a given iterable with mixed types (list and item type) into a 1D list.
    Flattens only the first layer
    Args:
        iterable: Iterable of items and lists

    Returns: flattened list

    Examples:
        >>> flatten([1, 2, 3, [1, 2], 1])
        [1, 2, 3, 1, 2, 1]
    """
    flattened_list = []
    for item in iterable:
        if isinstance(item, list):
            flattened_list.extend(item)
        else:
            flattened_list.append(item)
    return flattened_list


def build_mapping_dict(plugins: list[Plugin | list[Plugin]]):
    """
    Builds a mapping dict using the meta information of a plugin
    Args:
        plugins: A list with plugin (can contain nested lists)

    Returns: A mapping dict which maps the global id to the plugin
    """
    return dict([(plugin.get_id(), plugin) for plugin in flatten(plugins)])


def iter_namespace(ns_pkg):
    # Specifying the second argument (prefix) to iter_modules makes the
    # returned name an absolute name instead of a relative one. This allows
    # import_module to work without having to do additional modification to
    # the name.
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


def discover_namespace_packages(package: ModuleType):
    """
    Search and discovery sub packages of a given package
    Args:
        package: The package to scan

    Returns: A dictionary mapping the name to the loaded module

    Examples:
        >>> import problem_designer.typedef
        >>> 'problem_designer.typedef.spec' in discover_namespace_packages(problem_designer.typedef).keys()
        True
    """
    return {name: importlib.import_module(name) for finder, name, is_pkg in iter_namespace(package)}
