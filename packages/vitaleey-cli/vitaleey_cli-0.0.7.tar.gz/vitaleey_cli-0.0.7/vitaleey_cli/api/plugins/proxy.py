from .plugin import Plugin


class ProxyPlugin(Plugin):
    default_options = {
        "sequential": False,
    }
