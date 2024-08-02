import sys

from gibson.command.auth.Login import Login
from gibson.command.auth.Logout import Logout
from gibson.command.BaseCommand import BaseCommand


class Auth(BaseCommand):
    def execute(self):
        if len(sys.argv) != 3:
            self.usage()
        elif sys.argv[2] == "login":
            Login(self.configuration).execute()
        elif sys.argv[2] == "logout":
            Logout(self.configuration).execute()
        else:
            self.usage()

    def usage(self):
        self.conversation.type(
            f"usage: {self.configuration.command} auth login\n"
            + f"   or: {self.configuration.command} auth logout\n"
        )
        self.conversation.newline()
        exit(1)
