import os
from dataclasses import dataclass, field

import click

from ..utils.krakend import Krakend
from .plugins import render_plugins
from .service import Service
from .settings import settings as default_settings
from .utils import filter_dictionary, read_yaml_file, render_template


@dataclass(frozen=True)
class GatewayEndpoint:
    """
    Configuration for an APIGateway endpoint
    """

    endpoint: str = ""
    method: str = "GET"
    description: str = ""
    extra_config: list[dict] = field(default_factory=list)
    backends: list[dict] = field(default_factory=list)
    input_headers: list[str] = field(default_factory=list)
    input_query_strings: list[str] = field(default_factory=list)
    cache_ttl: str = ""


class Gateway:
    """Gateway class for generating API requests"""

    def __init__(self, environment, config_dir):
        self._environment = environment
        self._config_file_is_temporary = False
        self._temporary_dir = os.path.join(os.path.dirname(__file__), ".tmp")
        self._config_dir = os.path.join(os.getcwd(), config_dir)
        self._config_file_saved = False

        # Set the output directory
        self._file_output_dir = os.path.join(os.getcwd(), config_dir)
        self._data = read_yaml_file(os.path.join(self._config_dir, "gateway.yaml"))

    def set_config_file(
        self,
        config_file=None,
        output_dir=None,
    ):
        """
        Set the config file for the gateway
        """

        if not config_file:
            config_file = os.path.join(
                output_dir or self._config_dir, "gateway.json"
            )  # Default config file

        self._filename = config_file

    def write_config_file(self, data):
        """
        Write the data to the config file
        """

        if not os.path.exists(os.path.dirname(self._filename)):
            os.makedirs(os.path.dirname(self._filename))

        with open(self._filename, "w") as f:
            f.write(data)

        self._config_file_saved = True

    def get_settings(self):
        """
        Return the settings for the gateway
        """

        settings = self._data.get("settings")

        for key, value in default_settings.items():
            if key not in settings:
                settings[key] = value

        settings["extra_config"] = render_plugins(settings.get("plugins"))
        return filter_dictionary(settings)

    def get_endpoints(self):
        """
        Return a list of GatewayEndpoint objects
        """

        endpoints = []

        for endpoint in self._data.get("endpoints"):
            backends = []
            for backend in endpoint.get("backends"):
                backends.append(backend)

            gateway_endpoint = GatewayEndpoint(
                endpoint=endpoint.get("endpoint"),
                method=endpoint.get("method"),
                description=endpoint.get("description"),
                extra_config=render_plugins(endpoint.get("plugins")),
                input_headers=endpoint.get("input_headers"),
                input_query_strings=endpoint.get("input_query_strings"),
                backends=backends,
            )

            endpoints.append(gateway_endpoint)
        return endpoints

    def get_service_endpoints(self, service_name):
        """
        Return a list of GatewayEndpoint objects for a given service name
        """

        endpoints = []
        for endpoint in self.get_endpoints():
            for backend in endpoint.backends:
                if backend["service"] == service_name:
                    endpoints.append(endpoint)
        return endpoints

    def get_services(self):
        """
        Return a list of Service objects
        """

        services = []
        service_dir = os.path.join(self._config_dir, "services")

        for service_file in os.listdir(service_dir):
            if not service_file.endswith(".yaml"):
                continue
            service = Service(os.path.join(service_dir, service_file))
            services.append(service)
        return services

    def _get_service(self, service_name):
        """
        Return the service object for a given service name
        """

        for service in self.get_services():
            if service.name == service_name:
                return service
        return None

    def render_backend(self, backend):
        """
        Render the backend for the gateway
        """

        service = self._get_service(backend["service"])
        context = {
            **service.render_endpoint(backend["url_pattern"]),
            "allow": backend.get("allow", []),
            "deny": backend.get("deny", []),
            "disable_host_sanitize": backend.get("disable_host_sanitize", False),
            "encoding": backend.get("encoding", "no-op"),
            "group": backend.get("group", ""),
            "input_headers": backend.get("input_headers", []),
            "is_collection": backend.get("is_collection", True),
            "mapping": backend.get("mapping", {}),
            "sd": backend.get("sd", "static"),
            "sd_scheme": service.get_protocol(),
            "target": backend.get("target", ""),
        }

        return filter_dictionary(context)

    def render_endpoints(self):
        """
        Render the endpoints for the gateway
        """

        endpoints = self.get_endpoints()
        rendered_endpoints = []

        for endpoint in endpoints:
            backends = []
            for backend in endpoint.backends:
                backends.append(self.render_backend(backend))

            context = filter_dictionary(
                {
                    "endpoint": endpoint.endpoint,
                    "method": endpoint.method,
                    "@comment": endpoint.description,
                    "extra_config": endpoint.extra_config,
                    "input_headers": endpoint.input_headers,
                    "input_query_strings": endpoint.input_query_strings,
                    "backend": backends,
                }
            )

            rendered_endpoints.append(context)
        return rendered_endpoints

    def remove_tmp_file(self):
        """
        Remove the temporary gateway file
        """

        if self._config_file_is_temporary:
            for root, _, files in os.walk(self._temporary_dir):
                for file in files:
                    os.remove(os.path.join(root, file))
            os.removedirs(self._temporary_dir)

    def create_gateway_file(self, is_temporary=False):
        """
        Create the gateway file in the output directory
        """

        if is_temporary:
            self._config_file_is_temporary = True
            self._file_output_dir = self._temporary_dir

        self.set_config_file(output_dir=self._file_output_dir)

        settings = self.get_settings()
        endpoints = self.render_endpoints()

        context = {
            "env": self._environment,
            "settings": settings,
            "endpoints": endpoints,
        }

        content = render_template("gateway.j2", context)

        # Write the content to the gateway file
        self.write_config_file(content)

        return self._filename

    def check(self):
        """
        Check if the gateway file is valid
        """

        krakend = Krakend(self._filename)
        result = krakend.check()
        self.remove_tmp_file()  # Remove the temporary file

        if not result:
            raise click.ClickException(
                click.style(
                    "KrakenD check failed, please solve the configuration errors",
                    fg="red",
                )
            )

    def audit(self):
        """
        Audit the gateway file
        """

        if not self._config_file_saved:
            self.create_gateway_file(
                is_temporary=True
            )  # Ensure the gateway file exists

        krakend = Krakend(self._filename)
        result = krakend.audit()
        self.remove_tmp_file()  # Remove the temporary file

        if not result:
            raise click.ClickException(
                click.style(
                    "KrakenD audit failed, please solve the vulnerabilities", fg="red"
                )
            )

    def run(self):
        """
        Run the gateway file
        """

        if not self._config_file_saved:
            self.create_gateway_file(is_temporary=True)

        krakend = Krakend(self._filename)

        try:
            result = krakend.run()
            if not result:
                raise click.ClickException(
                    click.style(
                        "KrakenD run failed, please solve the runtime errors", fg="red"
                    )
                )
        except KeyboardInterrupt:
            print("KrakenD stopped")
            self.remove_tmp_file()
