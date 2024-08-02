class Plugin:
    default_options = {}

    def __init__(self, **options):
        self.options = options

    def get_default_options(self):
        """
        Get the default options for the plugin
        """
        return self.default_options

    def render(self):
        """
        Render the plugin
        """

        for key, value in self.options.items():
            if key in self.get_default_options():
                self.options[key] = value
        return self.options
