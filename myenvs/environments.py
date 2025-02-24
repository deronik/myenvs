import os
from pathlib import Path
from typing import Iterator

import pexpect

from .settings import settings


class Environment:
    name: str
    path: str
    shell: str
    envs: dict[str, str] = {}


class EnvironmentRepository:
    STORAGE: Path = settings.storage

    @staticmethod
    def save_environment(name: str, path: str, shell: str, envs: dict[str, str]) -> Environment:
        env = Environment()
        env.name = name
        env.path = path
        env.shell = shell
        env.envs = envs
        with open(EnvironmentRepository.STORAGE / f"{name}.env", "w") as f:
            for key, value in envs.items():
                if key in settings.ignored_envs:
                    continue
                f.write(f'export {key}="{value}"\n')
            f.write(f'export MYENVS_PATH="{path}"\n')
            f.write(f'export MYENVS_SHELL="{shell}"\n')
        os.chmod(EnvironmentRepository.STORAGE / f"{name}.env", 0o700)
        return env

    @classmethod
    def list_environments(cls) -> Iterator[Environment]:
        for f in EnvironmentRepository.STORAGE.glob("*.env"):
            yield cls.get_environment(f.stem)

    @staticmethod
    def get_environment(name: str) -> Environment:
        f = EnvironmentRepository.STORAGE / f"{name}.env"
        if not f.exists():
            raise FileNotFoundError

        envs = {}
        for line in f.read_text().splitlines():
            key, value = line.replace("export ", "").split("=")
            value = value.strip('"')
            envs[key] = value

        env = Environment()
        env.name = f.stem
        try:
            env.path = envs["MYENVS_PATH"]
            env.shell = envs["MYENVS_SHELL"]
        except KeyError:
            raise ValueError("Environment file is corrupted")
        env.envs = envs
        return env


class EnvironmentService:
    @staticmethod
    def save_current_environment(name: str) -> None:
        path = os.getcwd()
        envs = os.environ.copy()
        shell = os.environ.get("SHELL", "")
        EnvironmentRepository.save_environment(name, path, shell, envs)

    @staticmethod
    def list_environments() -> Iterator[str]:
        for env in EnvironmentRepository.list_environments():
            yield env.name

    @staticmethod
    def activate_environment(name: str) -> bool:
        if "MYENVS_PATH" in os.environ:
            raise ValueError("Environment already activated")
        environment = EnvironmentRepository.get_environment(name)
        child = pexpect.spawn(environment.shell, cwd=environment.path)
        child.sendline(f"source {EnvironmentRepository.STORAGE / name}.env")
        child.interact()
        return True
