import json
from pathlib import Path
from os.path import expandvars


class Config:
    def __init__(self, jdk_installations_path: str, current_jdk_version: str, current_jdk_distribution):
        self.JDK_INSTALLATIONS_PATH = jdk_installations_path
        self.CURRENT_JDK_VERSION = current_jdk_version
        self.CURRENT_JDK_DISTRIBUTION = current_jdk_distribution


class ConfigHandler:
    def __init__(self):
        self.file_name = "jdkman_config.json"
        self.config: Config = self.parse_config_file()

    def parse_config_file(self) -> Config:
        with open(Path(self.file_name).resolve(), "r") as config_file:
            data = json.load(config_file)
            return Config(jdk_installations_path=expandvars(data["JDK_INSTALLATIONS_PATH"]),
                          current_jdk_version=expandvars(data["CURRENT_JDK_VERSION"]),
                          current_jdk_distribution=expandvars(data["CURRENT_JDK_DISTRIBUTION"]))

    def write_config(self, config: Config) -> None:
        with open(Path(self.file_name).resolve(), "w") as config_file:
            config_file.write(json.dumps(config))
