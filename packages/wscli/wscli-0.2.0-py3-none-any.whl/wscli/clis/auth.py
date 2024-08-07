from dataclasses import asdict, dataclass
from typing import ClassVar

import click
from pydantic import TypeAdapter

from wscli.auth import SigninDetails
from wscli.auth.cognito import LoginCognito
from wscli.auth.keycloak import LoginKeyCloak
from wscli.config import WsConfig, pass_config
from wscli.utils import pprint


@dataclass
class AuthConfig:
    login_handler: LoginCognito | LoginKeyCloak | None = None
    enabled: bool = False  # if disabled this will ignore logins
    Key_: ClassVar[str] = "auth"


def raise_incomplete_config(config: AuthConfig):
    if config.login_handler is None:
        click.echo(
            "Your Login Details have not been Set. Please reset your client id"
        )
        raise click.Abort


pass_auth = click.make_pass_decorator(
    AuthConfig,
    ensure=True,
)


@click.group()
@click.pass_context
@pass_config
def cli(config: WsConfig, context: click.Context):
    adapter = TypeAdapter(AuthConfig)
    try:
        context.obj = adapter.validate_python(
            config.storer.get_key(AuthConfig.Key_)
        )
    except TypeError as err:
        click.echo(
            f"error loading the store key '{AuthConfig.Key_}'\n"
            f"Error:\n    {err}\n"
            "please use the wscli config commands to fix the issue"
        )
        raise click.Abort()


@cli.command()
@click.option("--client-id", prompt=True)
@pass_config
@pass_auth
def reset_cognito_handler(auth: AuthConfig, config: WsConfig, client_id: str):
    """
    Set your client_id for cognito
    """
    adapter = TypeAdapter(AuthConfig)
    auth.login_handler = LoginCognito(client_id=client_id)
    auth.enabled = True
    config.storer.set_key(auth.Key_, adapter.dump_python(auth))


@cli.command()
@click.option("--keycloak-id", prompt=True)
@pass_config
@pass_auth
def reset_keycloak_handler(auth: AuthConfig, config: WsConfig, client_id: str):
    """
    Set your client_id for keycloak"""
    adapter = TypeAdapter(AuthConfig)
    auth.login_handler = LoginKeyCloak(client_id_key_cloak=client_id)
    config.storer.set_key(auth.Key_, adapter.dump_python(auth))


@cli.command()
@pass_config
@pass_auth
def disable_function(config: WsConfig, auth: AuthConfig):
    """
    Function to disable authentication in the cli
    """
    adapter = TypeAdapter(AuthConfig)
    auth.enabled = False
    config.storer.set_key(auth.Key_, adapter.dump_python(auth))


@cli.command()
@pass_auth
def config_get(auth):
    """print the auth configuration"""
    click.echo(pprint(asdict(auth)))


@cli.command()
@click.option("--auth-url")
@pass_config
@pass_auth
def config_set(auth: AuthConfig, config: WsConfig, auth_url: str | None = None):
    """set the auth configuration"""

    if auth_url:
        auth.auth_url = auth_url
    config.storer.set_key(AuthConfig.Key_, asdict(auth))
    click.echo(pprint(asdict(auth)))


@cli.command()
@click.option("--user-name", prompt=True)
@click.option("--code", prompt=True)
@pass_auth
def confirm(auth: AuthConfig, user_name: str, code: str):
    """signup confirmation using the code"""
    click.echo(f"sign up confirm {auth}, {code}")


@cli.command()
@click.option("--user-name", prompt=True)
@pass_auth
def reset(auth: AuthConfig, user_name: str):
    """request a password reset"""
    click.echo("password reset...")


@cli.command()
@click.option("--user-name", prompt=True)
@click.option("--password", prompt=True, hide_input=True)
@pass_config
@pass_auth
def login(
    login_config: AuthConfig, config: WsConfig, user_name: str, password: str
):
    """login into the WS platform"""
    raise_incomplete_config(login_config)
    click.echo("logging in...")
    click.echo(f"username: {user_name}")
    click.echo("Fetching Token")
    config.login = login_config.login_handler.login(
        SigninDetails(username=user_name, password=password)
    )
    config.store()
    click.echo("Token updated")


@cli.command()
@pass_config
@pass_auth
def refresh(login_config: AuthConfig, config: WsConfig):
    """refresh your id token"""
    click.echo("refresh logging...")
    config.login = login_config.login_handler.refresh(config.login)
    config.store()
    click.echo("Id Token has been refreshed")
