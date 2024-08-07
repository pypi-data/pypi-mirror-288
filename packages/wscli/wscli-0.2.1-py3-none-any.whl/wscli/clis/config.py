import click

from wscli.config import WsConfig, pass_config
from wscli.utils import pprint


@click.group()
def cli():
    pass


@cli.command()
@pass_config
def list_keys(config: WsConfig):
    keys = list(config.storer.list_keys())
    click.echo(pprint(keys))


@cli.command()
@click.option("--key", required=True)
@click.option("--var", required=True)
@pass_config
def pop_var(config: WsConfig, key: str, var: str):
    storer = config.storer
    conf = storer.get_key(key)
    conf.pop(var, None)
    storer.set_key(key, conf)


@cli.command()
@click.option("--key", required=True)
@click.option("--var", required=True)
@click.option("--val", required=True)
@pass_config
def set_var(config: WsConfig, key: str, var: str, val: str):
    storer = config.storer
    conf = storer.get_key(key)
    conf[var] = val
    storer.set_key(key, conf)


@cli.command()
@click.option("--key", required=True)
@pass_config
def get_key(config: WsConfig, key: str):
    conf = config.storer.get_key(key)
    click.echo(pprint(conf))


@cli.command()
@click.option("--key", required=True)
@pass_config
def list_vars(config: WsConfig, key: str):
    conf = config.storer.get_key(key)
    click.echo(pprint(list(conf.keys())))


@cli.command()
@click.option("--key", required=True)
@click.option("--var", required=True)
@pass_config
def get_var(config: WsConfig, key: str, var: str):
    conf = config.storer.get_key(key)
    click.echo(conf.get(var))


@cli.command()
@click.option("--key", required=True)
@pass_config
def rm_key(config: WsConfig, key: str):
    config.storer.rm_key(key)
