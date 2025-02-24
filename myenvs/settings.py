import os
from pathlib import Path


class Settings:
    # We can use pydantic here but i want to do requirements minimal as possible
    def __init__(self) -> None:
        self.storage = Path.home() / ".myenvs"
        if "MYENVS_ENVS_PATH" in os.environ:
            self.storage = Path(os.environ["MYENVS_ENVS_PATH"])
        self.storage.mkdir(exist_ok=True)

        self.ignored_envs = {}


settings = Settings()
