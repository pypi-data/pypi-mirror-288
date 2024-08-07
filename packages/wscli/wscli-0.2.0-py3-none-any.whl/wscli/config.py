import json
import os
from collections.abc import Iterator
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import ClassVar, Dict

import click

from wscli.auth import LoginTokens
from wscli.auth.token import Token


@dataclass(kw_only=True)
class ConfigStorer:
    home: str
    ext: str = "json"
    sep: str = "."
    indent: int | None = None

    def setup(self):
        path = Path(self.home)
        path.mkdir(parents=True, exist_ok=True)

    def get_key_file(self, key: str) -> str:
        return self.sep.join([key, self.ext])

    def get_key_path(self, key: str):
        file_name = self.get_key_file(key)
        return f"{self.home}/{file_name}"

    def list_keys(self) -> Iterator[str]:
        for file_name in os.listdir(self.home):
            key, *parts = file_name.split(self.sep)
            if parts == [self.ext]:
                yield key

    def set_key(
        self,
        key: str,
        data: Dict[str, str | int | float],
        indent: int | None = None,
    ):
        with open(self.get_key_path(key), "w") as fid:
            indent = indent or self.indent
            json.dump(data, fid, indent=indent)

    def get_key(self, key: str):
        try:
            with open(self.get_key_path(key), "r") as fid:
                return json.load(fid)
        except Exception:
            return {}

    def rm_key(self, key: str):
        file_name = self.get_key_path(key)
        if os.path.exists(file_name):
            os.remove(file_name)


@dataclass
class WsContext:
    organization: str | None = None
    project: str | None = None
    Key_: ClassVar[str] = "context"


@dataclass
class WsConfig:
    storer: ConfigStorer
    login: LoginTokens | None = None
    context: WsContext = field(default_factory=WsContext)

    @classmethod
    def load(cls, storer):
        token_data = storer.get_key(LoginTokens.Key_)
        tokens = {
            token_type: Token(**params or {})
            for token_type, params in token_data.items()
        }
        return cls(
            storer=storer,
            login=LoginTokens(**tokens) if tokens else None,
            context=WsContext(**storer.get_key(WsContext.Key_)),
        )

    def store(self):
        self.storer.set_key(LoginTokens.Key_, asdict(self.login))
        self.storer.set_key(WsContext.Key_, asdict(self.context))


pass_config = click.make_pass_decorator(
    WsConfig,
    ensure=True,
)
