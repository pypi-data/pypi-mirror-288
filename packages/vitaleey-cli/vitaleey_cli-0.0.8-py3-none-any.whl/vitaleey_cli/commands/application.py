import os

import click

from vitaleey_cli.app.config import application_config
from vitaleey_cli.config import project_config
from vitaleey_cli.utils.git import git
from vitaleey_cli.utils.poetry import poetry


@click.group(help="Application helper commands")
def group():
    pass


def release_package(latest_tag, registry, language):
    """
    Release package and publish it to GitLab registry
    """

    version = latest_tag.lstrip("v")
    project_config.set("version", version)

    click.secho(f"Updated the version to {version}", fg="green", bold=True)

    if language == "python":
        # Publish python package
        if not poetry.publish_package(registry == "pypi"):
            raise click.ClickException("Failed to publish package")
    git.new_version(latest_tag)
    click.secho("Package published", fg="green")


@group.command(
    help="Release application, all settings will be read from the configuration"
)
def release():
    """
    Release application and publish it to GitLab registry
    """

    app_config = application_config()

    if os.environ.get("GITLAB_CI") != "true":
        click.secho("This command is only available in GitLab CI", fg="red")
        return

    latest_tag = git.latest_tag()
    package_version = project_config().get("version")

    if latest_tag.lstrip("v") == package_version:
        click.secho(f"No new release found, still version {latest_tag}", fg="yellow")
        return

    click.secho(f"New release found: {latest_tag}", fg="green")

    if app_config.application_type == "package":
        release_package(
            latest_tag,
            app_config.registry,
            app_config.language,
        )
    else:
        click.secho("Unknown application type", fg="yellow")
