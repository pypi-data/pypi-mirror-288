import time

import requests
from rich import print
from datazone.core.common.settings import SettingsManager
from datazone.errors.auth import DatazoneInvalidGrantError


class AuthService:
    @staticmethod
    def login() -> dict:
        profile = SettingsManager.get_profile()
        response = requests.post(
            f"{profile.get_service_url()}/auth/token",
            data={
                "email": profile.email,
                "password": profile.password,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        if not response.ok:
            raise DatazoneInvalidGrantError(detail="Invalid email or password!")

        token = response.json()
        SettingsManager.update_profile_token(token=token)

        return token

    @staticmethod
    def refresh_token() -> dict:
        profile = SettingsManager.get_profile()
        token = SettingsManager.get_profile_token()
        if token is None:
            raise DatazoneInvalidGrantError(detail="Token not found!")

        response = requests.post(
            f"{profile.get_service_url()}/auth/refresh",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Bearer {token['refresh_token']}",
            },
        )

        if not response.ok:
            raise DatazoneInvalidGrantError(detail="Invalid refresh token!")

        token = response.json()
        token.update({"refresh_token": token["access_token"]})
        SettingsManager.update_profile_token(token=token)
        return token

    @classmethod
    def get_session(cls) -> requests.Session:
        token = SettingsManager.get_profile_token()
        if token is None:
            print("[bold orange]Token not found, logging in...[/bold orange]")
            token = cls.login()
        elif token["expires_in"] < time.time():
            print("[bold orange]Token expired, refreshing...[/bold orange]")
            token = cls.refresh_token()

        session = requests.Session()
        session.headers.update({"Authorization": f"Bearer {token['access_token']}"})
        return session
