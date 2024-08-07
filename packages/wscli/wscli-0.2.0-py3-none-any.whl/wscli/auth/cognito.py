import os
from dataclasses import dataclass
from typing import Literal

import boto3

from .login import Login
from .login_tokens import LoginTokens
from .signin_details import SigninDetails

AuthFlow = Literal[
    "USER_PASSWORD_AUTH",
    "REFRESH_TOKEN_AUTH",
]


AwsRegion = Literal[
    "us-east-1",
    "us-east-2",
    "eu-west-1",
]


@dataclass
class LoginCognito(Login):
    client_id: str | None = os.environ.get("WSAPI_LOGIN_COGNITO_CLIENT_ID")
    auth_flow: AuthFlow = "USER_PASSWORD_AUTH"
    aws_region: AwsRegion = "us-east-1"

    @property
    def session(self) -> boto3.Session:
        return boto3.Session(region_name=self.aws_region)

    @property
    def client(self):
        return self.session.client("cognito-idp")

    def login(self, details: SigninDetails) -> LoginTokens:
        response = self.client.initiate_auth(
            ClientId=self.client_id,
            AuthFlow=self.auth_flow,
            AuthParameters={
                "USERNAME": details.username,
                "PASSWORD": details.password,
            },
        )

        auth_results = response["AuthenticationResult"]
        return LoginTokens(
            access_token=auth_results["AccessToken"],
            id_token=auth_results["IdToken"],
            refresh_token=auth_results["RefreshToken"],
        )

    def refresh(self, tokens: LoginTokens) -> LoginTokens:
        if not tokens.refresh_token:
            raise TypeError("no refresh token available")
        response = self.client.initiate_auth(
            ClientId=self.client_id,
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={
                "REFRESH_TOKEN": str(tokens.refresh_token),
            },
        )

        auth_results = response["AuthenticationResult"]
        refresh_token = (
            auth_results["RefreshToken"]
            if "RefreshToken" in auth_results
            else tokens.refresh_token
        )
        return LoginTokens(
            access_token=auth_results["AccessToken"],
            id_token=auth_results["IdToken"],
            refresh_token=refresh_token,
        )
