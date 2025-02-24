import argparse
from collections import defaultdict

from .environments import EnvironmentService


class CLIParser:
    # It can be click but i want to do requirements minimal as possible
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Simple CLI")
        self.subparsers = self.parser.add_subparsers(dest="command", description="Commands")
        self.subparsers.required = True
        self.commands = {}
        self.command_arguments = defaultdict(list)

    def register_command(self, func: callable) -> callable:
        self.commands[func.__name__.rstrip("_")] = func
        subparser = self.subparsers.add_parser(func.__name__.rstrip("_"), help=func.__doc__)
        for args, kwargs in self.command_arguments[func.__name__]:
            subparser.add_argument(*args, **kwargs)
        return func

    def add_argument(self, *args, **kwargs) -> callable:
        def wrapper(func):
            self.command_arguments[func.__name__.rstrip("_")].append((args, kwargs))
            return func

        return wrapper

    def run(self) -> None:
        args = self.parser.parse_args()
        _args = vars(args)
        command = _args.pop("command")
        self.commands[command](**vars(args))


parser = CLIParser()


@parser.register_command
def list_() -> None:
    services = EnvironmentService.list_environments()
    print("Environments:")
    for service in services:
        print(service)


@parser.register_command
@parser.add_argument("name", help="Name of the environment")
def save(name: str) -> None:
    EnvironmentService.save_current_environment(name)


@parser.register_command
@parser.add_argument("name", help="Name of the environment")
def activate(name: str) -> None:
    try:
        print(EnvironmentService.activate_environment_cmd(name))
    except FileNotFoundError:
        print("Environment not found")
        return


@parser.register_command
@parser.add_argument("name", help="Name of the environment")
def remove(name: str) -> None:
    try:
        EnvironmentService.remove_environment(name)
    except FileNotFoundError:
        print("Environment not found")
        return


def main() -> None:
    parser.run()


if __name__ == "__main__":
    main()
