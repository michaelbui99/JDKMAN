import json
from pathlib import Path
from os.path import expandvars


class Config:
    def __init__(self, jdk_installations_path: str, current_jdk_version: str):
        self.jdk_installations_path = jdk_installations_path
        self.current_jdk_version = current_jdk_version


class ConfigHandler:
    def __init__(self):
        self.file_name = "jdkman_config.json"
        self.config: Config = self.parse_config_file()

    def parse_config_file(self) -> Config:
        config_file = open(Path(self.file_name).resolve(), "r")
        data = json.load(config_file)
        return Config(jdk_installations_path=expandvars(data["JDK_INSTALLATIONS_PATH"]),
                      current_jdk_version=expandvars(data["CURRENT_JDK_VERSION"]))
