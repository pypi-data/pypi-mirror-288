from .proxy import ProxyPlugin
from .router import RouterPlugin

plugins = {
    "proxy": ProxyPlugin,
    "router": RouterPlugin,
}


def get_plugin(name):
    return plugins.get(name)


def render_plugins(plugin_list=list):
    """
    Render the plugins from the data
    """

    rendered_plugins = {}

    if not plugin_list:
        return rendered_plugins

    for plugin in plugin_list:
        plugin_name = plugin.pop("name")
        plugin_class = get_plugin(plugin_name)
        if plugin_class:
            plugin_object = plugin_class(**plugin)
            rendered_plugins[plugin_name] = plugin_object.render()
    return rendered_plugins
