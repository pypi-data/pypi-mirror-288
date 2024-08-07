from typing import Protocol

from .login_tokens import LoginTokens
from .signin_details import SigninDetails


class Login(Protocol):
    def login(self, details: SigninDetails) -> LoginTokens: ...
    def refresh(self, tokens: LoginTokens) -> LoginTokens: ...
