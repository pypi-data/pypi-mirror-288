from dataclasses import InitVar, dataclass
from typing import ClassVar

from wscli.auth.token import Token


@dataclass
class LoginTokens:
    access_token: str | Token | None = None
    refresh_token: str | Token | None = None
    id_token: str | Token | None = None

    exp_gap: InitVar[int] = 60
    Key_: ClassVar[str] = "login_tokens"

    def __post_init__(self, exp_gap: int = 60):
        if isinstance(self.access_token, str):
            self.access_token = Token(value=self.access_token, exp_gap=exp_gap)
        elif isinstance(self.access_token, dict):
            self.access_token = Token(**self.access_token)
        if isinstance(self.id_token, str):
            self.id_token = Token(value=self.id_token, exp_gap=exp_gap)
        elif isinstance(self.id_token, dict):
            self.id_token = Token(**self.id_token)
        if isinstance(self.refresh_token, str):
            self.refresh_token = Token(
                value=self.refresh_token, exp_gap=exp_gap
            )
        elif isinstance(self.refresh_token, dict):
            self.refresh_token = Token(**self.refresh_token)
