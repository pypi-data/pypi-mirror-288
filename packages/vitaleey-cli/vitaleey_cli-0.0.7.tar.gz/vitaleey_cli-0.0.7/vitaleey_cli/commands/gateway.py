import os

import click

from vitaleey_cli.api.config import DEFAULT_ENVIROMENTS, api_gateway_config
from vitaleey_cli.api.gateway import Gateway


@click.group(help="API Gateway helper commands")
def group():
    pass


@group.command(help="List all API Gateway resources")
@click.argument(
    "environment",
    default=DEFAULT_ENVIROMENTS[0],
    type=click.Choice(DEFAULT_ENVIROMENTS),
)
def services(environment):
    config = api_gateway_config(environment)

    gateway = Gateway(environment, config.endpoint_dir)
    services = gateway.get_services()

    click.secho("Listing API Gateway services\n", bold=True)

    for service in services:
        click.echo(f"Service: {service['name']}")
        for key, value in service["data"]["settings"].items():
            click.echo(f"{key.title()}: {value}")
        click.echo(f"Endpoints: {len(service['data']['endpoints'])}\n")


@group.command(help="Show API Gateway settings")
@click.argument(
    "environment",
    default=DEFAULT_ENVIROMENTS[0],
    type=click.Choice(DEFAULT_ENVIROMENTS),
)
def settings(environment):
    config = api_gateway_config(environment)

    gateway = Gateway(environment, config.endpoint_dir)
    settings = gateway.get_settings()

    click.secho("Show API Gateway settings\n", bold=True)

    for key, value in settings.items():
        click.echo(f"{click.style(f"{key}: ", fg="blue")}{value}")


@group.command(help="Show API Gateway endpoints")
@click.option("--service", "-s", help="Filter by service")
@click.argument(
    "environment",
    default=DEFAULT_ENVIROMENTS[0],
    type=click.Choice(DEFAULT_ENVIROMENTS),
)
def endpoints(environment, **kwargs):
    config = api_gateway_config(environment)

    gateway = Gateway(environment, config.endpoint_dir)
    endpoints = gateway.get_endpoints()

    click.secho("Show API Gateway endpoints\n", bold=True)

    if service := kwargs.pop("service"):
        endpoints = gateway.get_service_endpoints(service)

    for endpoint in endpoints:
        click.echo(f"* Endpoint: {endpoint.endpoint}")
        click.echo(f"  Method: {endpoint.method}")
        click.echo(f"  Extra Config: {endpoint.extra_config}")
        click.echo("  Backends:")
        for backend in endpoint.backends:
            click.echo(f"  * Service: {backend.service}")
            click.echo(f"  * URL Pattern: {backend.url_pattern}")
            click.echo(f"  * Extra Config: {backend.extra_config}\n")


@group.command(help="Create the Kraken API Gateway file")
@click.option("--no-check", is_flag=True, help="Skip the Kraken check")
@click.option("--no-audit", is_flag=True, help="Skip the Kraken audit")
@click.argument(
    "environment",
    default=DEFAULT_ENVIROMENTS[0],
    type=click.Choice(DEFAULT_ENVIROMENTS),
)
def create(environment, **kwargs):
    config = api_gateway_config(environment)

    click.secho("Create the Kraken API Gateway file \n", bold=True)

    gateway = Gateway(environment, config.endpoint_dir)
    gateway_file = gateway.create_gateway_file()

    if gateway_file:
        click.secho(f"Gateway file created: {gateway_file}", fg="green")

    if not kwargs.pop("no_check"):
        gateway.check()

    if not kwargs.pop("no_audit"):
        gateway.audit()


@group.command(help="Check the Kraken API Gateway file")
@click.option(
    "--config_file", "-c", help="Kraken config file", type=click.Path(exists=True)
)
@click.argument(
    "environment",
    default=DEFAULT_ENVIROMENTS[0],
    type=click.Choice(DEFAULT_ENVIROMENTS),
)
def check(environment, **kwargs):
    config = api_gateway_config(environment)

    click.secho("Check the Kraken API Gateway file \n", bold=True)

    gateway = Gateway(environment, config.endpoint_dir)

    if not kwargs.pop("config_file"):
        gateway.create_gateway_file(is_temporary=True)  # Ensure the gateway file exists
    else:
        gateway.set_config_file(os.path.abspath(kwargs.pop("config_file")))

    gateway.check()


@group.command(help="Audit the Kraken API Gateway file")
@click.option(
    "--config_file", "-c", help="Kraken config file", type=click.Path(exists=True)
)
@click.argument(
    "environment",
    default=DEFAULT_ENVIROMENTS[0],
    type=click.Choice(DEFAULT_ENVIROMENTS),
)
def audit(environment, **kwargs):
    config = api_gateway_config(environment)

    click.secho("Audit the Kraken API Gateway file \n", bold=True)

    gateway = Gateway(environment, config.endpoint_dir)

    if not kwargs.pop("config_file"):
        gateway.create_gateway_file(is_temporary=True)  # Ensure the gateway file exists
    else:
        gateway.set_config_file(os.path.abspath(kwargs.pop("config_file")))

    gateway.audit()


@group.command(help="Run the Kraken API Gateway")
@click.option("--save_config", is_flag=True, help="Save the Kraken config file")
@click.option(
    "--config_file", "-c", help="Kraken config file", type=click.Path(exists=True)
)
@click.argument(
    "environment",
    default=DEFAULT_ENVIROMENTS[0],
    type=click.Choice(DEFAULT_ENVIROMENTS),
)
def run(environment, **kwargs):
    config = api_gateway_config(environment)

    click.secho("Run the Kraken API Gateway file \n", bold=True)

    if kwargs.get("config_file") and kwargs.get("save_config"):
        raise click.ClickException(
            click.style(
                "You can't save the config file and provide a custom one at the same time",
                fg="red",
            )
        )

    gateway = Gateway(environment, config.endpoint_dir)
    if not kwargs.pop("config_file"):
        is_temporary = not kwargs.pop("save_config")
        gateway.create_gateway_file(
            is_temporary=is_temporary
        )  # Ensure the gateway file exists
    else:
        gateway.set_config_file(os.path.abspath(kwargs.pop("config_file")))

    gateway.run()
