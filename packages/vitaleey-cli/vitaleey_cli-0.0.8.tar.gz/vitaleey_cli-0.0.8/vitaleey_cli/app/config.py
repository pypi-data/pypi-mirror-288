from dataclasses import dataclass

from vitaleey_cli.config import CommandConfig, Config

__all__ = ["application_config"]

DEFAULT_REGISTRY = "gitlab"
AVAILABLE_REGISTRIES = ["gitlab", "pypi"]

DEFAULT_LANGUAGE = "python"
AVAILABLE_LANGUAGES = ["python", "react"]

DEFAULT_APPLICATION_TYPE = "microservice"
AVAILABLE_APPLICATION_TYPES = ["microservice", "package"]


@dataclass(frozen=True)
class ApplicationDataclass(CommandConfig):
    """
    Configuration for the application

    Options:
    - registry: The registry to publish the application to
    - language: The language of the application
    - application_type: The type of the application
    """

    registry: str = DEFAULT_REGISTRY
    language: str = DEFAULT_LANGUAGE
    application_type: str = DEFAULT_APPLICATION_TYPE


class ApplicationConfig(Config):
    """
    Application configuration
    """

    dataclass = ApplicationDataclass


application_config = ApplicationConfig()
