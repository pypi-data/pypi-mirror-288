from gibson.api.Cli import Cli
from gibson.dev.Dev import Dev
from gibson.command.BaseCommand import BaseCommand
from gibson.core.TimeKeeper import TimeKeeper


class Tests(BaseCommand):
    def execute(self):
        entities = []
        if self.memory.entities is not None:
            for entity in self.memory.entities:
                entities.append(entity["name"])

        if len(entities) == 0:
            self.conversation.cant_no_entities(self.configuration.project.name)
            exit(1)

        time_keeper = TimeKeeper()

        cli = Cli(self.configuration)
        response = cli.code_testing(entities)

        for entry in response["code"]:
            Dev(self.configuration).tests(entry["entity"]["name"], entry["definition"])

            if self.conversation.muted() is False:
                print(entry["definition"])

        if self.conversation.muted() is False:
            time_keeper.display()
