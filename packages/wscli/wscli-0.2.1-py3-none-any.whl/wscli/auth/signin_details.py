from dataclasses import dataclass


@dataclass
class SigninDetails:
    username: str
    password: str
