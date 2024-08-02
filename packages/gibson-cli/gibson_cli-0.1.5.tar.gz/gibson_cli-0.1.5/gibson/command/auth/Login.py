from gibson.api.BaseApi import BaseApi
from gibson.command.BaseCommand import BaseCommand
from gibson.services.auth.Server import Server as AuthServer


class Login(BaseCommand):
    def execute(self):
        api = BaseApi(self.configuration)
        access_token, refresh_token = AuthServer(api.app_domain()).get_tokens()

        if access_token is None or refresh_token is None:
            self.conversation.newline()
            self.conversation.type(
                "Login failed, please try again with `gibson auth login`."
            )
        else:
            self.configuration.set_auth_tokens(access_token, refresh_token)
            self.conversation.type(f"Welcome! You are now logged in.")

        self.conversation.newline()
