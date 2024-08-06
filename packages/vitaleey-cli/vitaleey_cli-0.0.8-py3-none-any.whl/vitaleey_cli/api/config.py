from dataclasses import dataclass, field

import click

from vitaleey_cli.config import Config

__all__ = ["api_gateway_config"]

DEFAULT_ENVIROMENTS = ["dev", "acc", "prod"]


@dataclass(frozen=True)
class ApiGatewayDataclass:
    """
    Configuration for an APIGateway environment:
        development, acceptance, production

    Options:
    - endpoint_dir: The directory where the endpoint files are stored
    ```
    """

    endpoint_dir: str = "config"


@dataclass(frozen=True)
class EnvironmentDataclass:
    """
    Configuration for all the environments:

    Options:
    - environments: The environments for the APIGateway
    """

    environments: dict[str, ApiGatewayDataclass] = field(default_factory=dict)


class ApiGatewayConfig(Config):
    """
    API Gateway configuration
    """

    def _load_env_configs(self, config):
        """
        Load the environments configurations
        """

        # Get environments
        environments = {}

        config_envs: dict[str, dict] = config.get("env", {})

        # Retrieve environment configurations
        for group, group_config in config_envs.items():
            kwargs = {
                key: value
                for key, value in group_config.items()
                if key in ApiGatewayDataclass.__annotations__
            }

            # Fill missing keys with global_config
            for key in ApiGatewayDataclass.__annotations__:
                if not kwargs.get(key) and config.get(key):
                    kwargs[key] = config.get(key)
            environments[group] = ApiGatewayDataclass(**kwargs)
        return EnvironmentDataclass(environments=environments)

    def load(self, environment: str):
        """
        Load the configuration based on the environment
        """

        if environment not in DEFAULT_ENVIROMENTS:
            raise click.UsageError("Invalid environment")

        config = super().load()
        env_configs = self._load_env_configs(config)

        return env_configs.environments.get(environment)


api_gateway_config = ApiGatewayConfig()
