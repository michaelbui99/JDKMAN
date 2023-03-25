import json
from jdkman.util.io_util import as_expanded_path
from pathlib import Path
from os.path import expandvars


class Config:
    def __init__(self, jdkman_installation_path: str, current_jdk_version: str, current_jdk_distribution):
        self.JDKMAN_INSTALLATION_PATH = jdkman_installation_path
        self.CURRENT_JDK_VERSION = current_jdk_version
        self.CURRENT_JDK_DISTRIBUTION = current_jdk_distribution


class ConfigHandler:
    def __init__(self):
        self.file_name = "jdkman_config.json"
        self.config: Config = self.parse_config_file(None)

    def parse_config_file(self, path: str | None) -> Config:
        if not path:
            path = self.file_name
        # Search local config file for installation path
        with open(Path(path).absolute(), "r") as config_file:
            data = json.load(config_file)
            # Use the config file in installation path as the principal one, since user might have edited it manually
            with open(as_expanded_path(f'{data["JDKMAN_INSTALLATION_PATH"]}/{self.file_name}'), "r") as principal_config_file:
                data = json.load(principal_config_file)
                return Config(jdkman_installation_path=expandvars(data["JDKMAN_INSTALLATION_PATH"]),
                              current_jdk_version=expandvars(data["CURRENT_JDK_VERSION"]),
                              current_jdk_distribution=expandvars(data["CURRENT_JDK_DISTRIBUTION"]))

    def write_config(self, config: Config, path: str | None) -> None:
        if not path:
            path = self.file_name
        with open(Path(f'{path}/{self.file_name}').absolute(), "w") as config_file:
            config_file.write(json.dumps(config.__dict__))
