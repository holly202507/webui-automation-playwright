import os
from dataclasses import dataclass
from typing import Optional

import yaml


@dataclass
class BrowserConfig:
    headless: bool
    slow_mo: int
    viewport_width: int
    viewport_height: int


@dataclass
class EnvConfig:
    base_url: str
    timeout: int


class Config:
    """Singleton configuration loader. Reads config.yaml and supports
    environment variable overrides for CI/CD flexibility."""

    _instance: Optional["Config"] = None
    _data: dict = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self):
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.yaml")
        with open(config_path) as f:
            self._data = yaml.safe_load(f)

    @property
    def env(self) -> str:
        return os.getenv("TEST_ENV", self._data.get("default_env", "dev"))

    @property
    def env_config(self) -> EnvConfig:
        env_data = self._data["environments"][self.env]
        return EnvConfig(
            base_url=os.getenv("BASE_URL", env_data["base_url"]),
            timeout=int(os.getenv("TIMEOUT", env_data["timeout"])),
        )

    @property
    def browser_config(self) -> BrowserConfig:
        bc = self._data["browser"]
        return BrowserConfig(
            headless=os.getenv("HEADLESS", str(bc["headless"])).lower() != "false",
            slow_mo=int(os.getenv("SLOW_MO", bc["slow_mo"])),
            viewport_width=bc["viewport"]["width"],
            viewport_height=bc["viewport"]["height"],
        )

    @property
    def base_url(self) -> str:
        return self.env_config.base_url

    @property
    def timeout(self) -> int:
        return self.env_config.timeout


config = Config()
