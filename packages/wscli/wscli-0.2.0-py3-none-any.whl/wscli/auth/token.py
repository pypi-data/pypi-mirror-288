import time
from dataclasses import dataclass
from functools import partial
from typing import Dict

import jwt

_decoder = partial(jwt.decode, options={"verify_signature": False})


Claims = Dict[str, str | int | bool]


@dataclass
class Token:
    value: str
    exp_gap: int = 60  # secs before actual expiry

    def __str__(self):
        return str(self.value)

    def __bool__(self):
        return bool(self.value)

    @property
    def claims(self) -> Claims:
        return _decoder(self.value)

    @property
    def exp(self):
        return self.claims.get("exp", -1)

    @property
    def is_valid(self):
        if self.exp < 1:
            return False
        else:
            return (self.exp - time.time()) > self.exp_gap

    @property
    def is_expired(self) -> bool:
        return not self.is_valid
