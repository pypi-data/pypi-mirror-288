import os

import click
from pydantic import TypeAdapter

from wscli.clis import auth, config, ml
from wscli.config import ConfigStorer, WsConfig, pass_config

# from wscli.clis import organizations


@click.group()
@click.option(
    "--home",
    envvar="WSCLI_HOME",
    default=lambda: os.environ.get("HOME") + "/.wscli",
)
@click.pass_context
def cli(context, home: str):
    storer = ConfigStorer(home=home)
    storer.setup()
    context.obj = WsConfig.load(storer)


@cli.command()
@pass_config
def show_config(config: WsConfig):
    click.echo(TypeAdapter(WsConfig).dump_json(config, indent=2))


cli.add_command(auth.cli, name="auth")
cli.add_command(config.cli, name="config")
cli.add_command(ml.cli, name="ml")
# cli.add_command(organizations.cli, name="org")
