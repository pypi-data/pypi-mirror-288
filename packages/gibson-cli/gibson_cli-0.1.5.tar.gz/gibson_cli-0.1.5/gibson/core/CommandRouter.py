import sys

from gibson.command.Api import Api
from gibson.command.auth.Auth import Auth
from gibson.command.Base import Base
from gibson.command.Build import Build
from gibson.command.Code import Code
from gibson.command.Conf import Conf
from gibson.command.Count import Count
from gibson.command.Dev import Dev
from gibson.command.Forget import Forget
from gibson.command.Import import Import
from gibson.command.List import List
from gibson.command.Merge import Merge
from gibson.command.Model import Model
from gibson.command.Models import Models
from gibson.command.Modify import Modify
from gibson.command.Module import Module
from gibson.command.New import New
from gibson.command.OpenApi import OpenApi
from gibson.command.Question import Question
from gibson.command.Remove import Remove
from gibson.command.Rename import Rename
from gibson.command.Rewrite import Rewrite
from gibson.command.Schema import Schema
from gibson.command.Schemas import Schemas
from gibson.command.Show import Show
from gibson.command.Test import Test
from gibson.command.Tests import Tests
from gibson.command.Tree import Tree
from gibson.command.Version import Version
from gibson.command.WarGames import WarGames
from gibson.core.Configuration import Configuration
from gibson.core.Conversation import Conversation
from gibson.core.Env import Env
from gibson.core.Memory import Memory


class CommandRouter:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.conversation = Conversation()

    def help(self, exit_code=0):
        dev_off = "*"
        dev_on = ""
        if self.configuration.project.dev.active is True:
            dev_off = ""
            dev_on = "*"

        commands = {
            "api": {
                "description": "write the API code for the project",
                "memory": "stored",
            },
            "auth": {
                "description": "login | logout",
                "memory": None,
            },
            "base": {
                "description": "write the base code for the project",
                "memory": "stored",
            },
            "build": {
                "description": "create the entities in the datastore",
                "memory": "stored",
            },
            "code": {"description": "pair program", "memory": None},
            "conf": {"description": "set a configuration variable", "memory": None},
            "count": {
                "description": "show the number of entities stored",
                "memory": "last | stored",
            },
            "dev": {
                "description": f"mode off{dev_off} | on{dev_on}",
                "memory": None,
            },
            "forget": {
                "description": "delete memory",
                "memory": "all | last | stored",
            },
            "help": {"description": "for help", "memory": None},
            "import": {
                "description": "configure from a data source",
                "memory": "stored",
            },
            "list": {
                "description": "show the names of entities in your project",
                "memory": None,
            },
            "merge": {
                "description": "move last changes into project",
                "memory": "last -> stored",
            },
            "model": {
                "description": "write the model code for an entity",
                "memory": "stored",
            },
            "models": {
                "description": "write all the model code",
                "memory": "stored",
            },
            "modify": {
                "description": "change an entity using natural language",
                "memory": "last > stored",
            },
            "module": {"description": "create a new module", "memory": "last"},
            "new": {"description": "start something new", "memory": None},
            "openapi": {"description": "build from an OpenAPI spec", "memory": "last"},
            "remove": {
                "description": "remove an entity from the project",
                "memory": "last > stored",
            },
            "rename": {
                "description": "rename an entity",
                "memory": "last > stored",
            },
            "rewrite": {
                "description": "rewrite all code from scratch",
                "memory": "stored",
            },
            "schema": {
                "description": "write the schema code for an entity",
                "memory": "stored",
            },
            "schemas": {
                "description": "write all the schema code",
                "memory": "stored",
            },
            "show": {"description": "display an entity", "memory": "last > stored"},
            "test": {
                "description": "write the unit tests for an entity",
                "memory": "stored",
            },
            "tests": {
                "description": "write all the unit tests",
                "memory": "stored",
            },
            "tree": {"description": "illustrate the project layout", "memory": None},
            "? | q": {"description": "ask a question", "memory": None},
        }

        self.conversation.set_delay(0.001)
        self.conversation.display_project(self.configuration.project.name)
        self.conversation.type(f"usage: {self.configuration.command} [command]\n\n")
        self.conversation.type(" command  description" + " " * 40 + "memory\n")
        self.conversation.type(" -------  -----------" + " " * 40 + "------\n")

        for command, config in commands.items():
            memory = ""
            if config["memory"] is not None:
                memory = f"[{config['memory']}]"

            spaces = 61 - (8 + 2 + len(config["description"]))

            self.conversation.type(
                f"{command.rjust(8)}"
                + f"  {config['description']}"
                + " " * spaces
                + f"{memory}\n"
            )

        self.conversation.newline()
        self.conversation.type("memory:\n\n")

        stats = Memory(self.configuration).stats()
        self.conversation.type(
            f"{str(stats['entities']['num']).rjust(8)}"
            + f"  {stats['entities']['word']}"
            + " " * (43 if stats["entities"]["word"] == "entities" else 45)
            + "[stored]\n"
        )
        self.conversation.type(
            f"{str(stats['last']['num']).rjust(8)}"
            + f"  {stats['last']['word']}"
            + " " * (43 if stats["last"]["word"] == "entities" else 45)
            + "[last]\n\n"
        )

        exit(exit_code)

    def run(self):
        if len(sys.argv) == 1 or sys.argv[1] == "help":
            self.help()
            return self

        Env().verify(self.configuration)

        command = None
        if sys.argv[1] == "api":
            command = Api(self.configuration)
        elif sys.argv[1] == "auth":
            command = Auth(self.configuration)
        elif sys.argv[1] == "base":
            command = Base(self.configuration)
        elif sys.argv[1] == "build":
            command = Build(self.configuration)
        elif sys.argv[1] == "code":
            command = Code(self.configuration)
        elif sys.argv[1] == "conf":
            command = Conf(self.configuration)
        elif sys.argv[1] == "count":
            command = Count(self.configuration)
        elif sys.argv[1] == "dev":
            command = Dev(self.configuration)
        elif sys.argv[1] == "forget":
            command = Forget(self.configuration)
        elif sys.argv[1] == "import":
            command = Import(self.configuration)
        elif sys.argv[1] == "list":
            command = List(self.configuration)
        elif sys.argv[1] == "merge":
            command = Merge(self.configuration)
        elif sys.argv[1] == "model":
            command = Model(self.configuration)
        elif sys.argv[1] == "models":
            command = Models(self.configuration)
        elif sys.argv[1] == "modify":
            command = Modify(self.configuration)
        elif sys.argv[1] == "module":
            command = Module(self.configuration)
        elif sys.argv[1] == "new":
            command = New(self.configuration)
        elif sys.argv[1] == "openapi":
            command = OpenApi(self.configuration)
        elif sys.argv[1] == "remove":
            command = Remove(self.configuration)
        elif sys.argv[1] == "rename":
            command = Rename(self.configuration)
        elif sys.argv[1] == "rewrite":
            command = Rewrite(self.configuration, with_header=True)
        elif sys.argv[1] == "schema":
            command = Schema(self.configuration)
        elif sys.argv[1] == "schemas":
            command = Schemas(self.configuration)
        elif sys.argv[1] == "show":
            command = Show(self.configuration)
        elif sys.argv[1] == "test":
            command = Test(self.configuration)
        elif sys.argv[1] == "tests":
            command = Tests(self.configuration)
        elif sys.argv[1] == "tree":
            command = Tree(self.configuration)
        elif sys.argv[1] in ["?", "q"]:
            command = Question(self.configuration)
        elif sys.argv[1] in ["--version", "-v"]:
            command = Version(self.configuration)
        else:
            command = WarGames(self.configuration)

        if command is None or command.execute() is False:
            self.help(exit_code=1)
