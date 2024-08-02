import os
import requests

from gibson.core.Configuration import Configuration


class BaseApi:
    API_ENV = os.environ.get("GIBSONAI_API_ENV", "staging")
    VERSION = "v1"

    def __init__(self, configuration: Configuration):
        self.configuration = configuration

    def api_domain(self):
        domains = {
            "local": "http://localhost:8000",
            "staging": "https://staging-api.gibsonai.com",
            "production": "https://api.gibsonai.com",
        }
        return domains[self.API_ENV]

    def app_domain(self):
        domains = {
            "local": "http://localhost:5173",
            "staging": "https://staging-app.gibsonai.com",
            "production": "https://app.gibsonai.com",
        }
        return domains[self.API_ENV]

    def base_url(self):
        return f"{self.api_domain()}/{self.VERSION}"

    def client_id(self):
        return {
            "local": "9b0cbebd-3eb4-47be-89ac-4aa589316ff4",
            "staging": "02459e16-f356-4c01-b689-59847ed04b0a",
            "production": "da287371-240b-4b53-bfde-4b1581cca62a",
        }[self.API_ENV]

    def get(self, endpoint):
        r = requests.get(self.url(endpoint), headers=self.headers())

        if r.status_code == 401 and self.refresh_auth_tokens():
            r = requests.get(self.url(endpoint), headers=self.headers())

        self.__raise_for_status(r)

        return r.json()

    def headers(self):
        raise NotImplementedError

    def post(self, endpoint, json: dict):
        r = requests.post(self.url(endpoint), headers=self.headers(), json=json)

        if r.status_code == 401 and self.refresh_auth_tokens():
            r = requests.post(self.url(endpoint), headers=self.headers(), json=json)

        self.__raise_for_status(r)

        return r

    def put(self, endpoint, json: dict):
        r = requests.put(self.url(endpoint), headers=self.headers(), json=json)

        if r.status_code == 401 and self.refresh_auth_tokens():
            r = requests.put(self.url(endpoint), headers=self.headers(), json=json)

        self.__raise_for_status(r)

        return r

    def refresh_auth_tokens(self):
        refresh_token = self.configuration.get_refresh_token()
        if not refresh_token:
            return False

        r = requests.post(
            f"{self.base_url()}/auth/token/refresh",
            headers=self.headers(),
            json={"refresh_token": refresh_token},
        )

        if r.status_code != 200:
            return False

        parsed = r.json()
        self.configuration.set_auth_tokens(
            parsed["access_token"], parsed["refresh_token"]
        )
        return True

    def url(self, endpoint):
        if self.PREFIX:
            return f"{self.base_url()}/{self.PREFIX}/{endpoint}"
        return f"{self.base_url()}/{endpoint}"

    def __raise_for_status(self, r):
        try:
            r.raise_for_status()
        except:
            try:
                message = r.json()

                print("=" * 78)
                print("Raw Response:\n")
                print(message)
                print("\n" + "=" * 78)
            except requests.exceptions.JSONDecodeError:
                pass

            raise
