from .plugins import render_plugins
from .utils import read_yaml_file


class Service:
    """
    A class to represent an API Gateway service
    """

    def __init__(self, service_file):
        self.name = service_file.split("/")[-1].replace(".yaml", "")
        self.data = read_yaml_file(service_file)
        self.settings = self.data.get("settings")
        self.endpoints = self.data.get("endpoints")

    def get_protocol(self):
        """
        Get the protocol for the service
        """

        if self.settings.get("tls_secured"):
            return "https"
        return "http"

    def get_host_port(self, endpoint):
        """
        Get the host and port for the service
        """

        hostname = self.settings.get("hostname")
        port = self.settings.get("port")
        port = self.settings.get("port")
        protocol = self.get_protocol()

        if protocol == "https":
            port = self.settings.get("tls_port", port)

        hostname = self.settings.get("hostname")
        return f"{protocol}://{hostname}:{port}"

    def get_endpoint(self, label):
        """
        Get the endpoint with the given label
        """

        for endpoint in self.endpoints:
            if endpoint.get("label") == label:
                return endpoint
        return None

    def render_endpoint(self, label, **options):
        """
        Render the endpoint with the given label
        """

        endpoint = self.get_endpoint(label)
        if not endpoint:
            return None

        context = {
            "url_pattern": endpoint.get("url_pattern"),
            "method": endpoint.get("method"),
            "host": [self.get_host_port(endpoint)],
            "extra_config": render_plugins(endpoint.get("plugins")),
        }

        return context
