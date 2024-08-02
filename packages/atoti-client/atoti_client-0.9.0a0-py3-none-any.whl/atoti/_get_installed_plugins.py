from collections.abc import Mapping
from functools import cache
from importlib.metadata import entry_points, version

from _atoti_core import Plugin


@cache
def get_installed_plugins() -> Mapping[str, Plugin]:
    expected_version = version("atoti-client")
    plugins: dict[str, Plugin] = {}

    for entry_point in entry_points(group="atoti.plugins"):
        assert entry_point.dist
        plugin_package_name = entry_point.dist.name
        plugin_version = version(plugin_package_name)

        assert (
            plugin_version == expected_version
        ), f"This version of Atoti only supports {plugin_package_name} v{expected_version} but got v{plugin_version}."

        plugin_class = entry_point.load()
        plugin = plugin_class()

        if not isinstance(plugin, Plugin):
            raise TypeError(f"Unexpected plugin type: {type(plugin)}.")

        plugins[entry_point.name] = plugin

    return plugins
