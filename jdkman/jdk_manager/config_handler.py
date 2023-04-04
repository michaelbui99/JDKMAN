import json
import os.path

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
        """
        Parses Config from file.

        If None is passed, then jdkman_config.json located at package root will be read first to find JDKMAN installation path.
        If JDKMAN_INSTALLATION_PATH has been configured, then jdkman_config.json at JDKMAN installation path will be parsed.

        :param path:path to file to parse Config from.
        :return:Config
        """
        if not path:
            path = self.file_name
        # Search local config file for installation path
        with open(Path(path).absolute(), "r") as config_file:
            data = json.load(config_file)
            # Use the config file in installation path as the principal one, since user might have edited it manually
            principal_config_path = os.path.expanduser(f'{data["JDKMAN_INSTALLATION_PATH"]}/{self.file_name}')
            if not os.path.exists(principal_config_path):
                return Config(jdkman_installation_path=expandvars(data["JDKMAN_INSTALLATION_PATH"]),
                              current_jdk_version=expandvars(data["CURRENT_JDK_VERSION"]),
                              current_jdk_distribution=expandvars(data["CURRENT_JDK_DISTRIBUTION"]))
            with open(Path(principal_config_path).resolve(),
                      "r") as principal_config_file:
                principal_data = json.load(principal_config_file)
                if len(principal_data) == 0:
                    return Config(jdkman_installation_path=expandvars(data["JDKMAN_INSTALLATION_PATH"]),
                                  current_jdk_version=expandvars(data["CURRENT_JDK_VERSION"]),
                                  current_jdk_distribution=expandvars(data["CURRENT_JDK_DISTRIBUTION"]))
                return Config(jdkman_installation_path=expandvars(principal_data["JDKMAN_INSTALLATION_PATH"]),
                              current_jdk_version=expandvars(principal_data["CURRENT_JDK_VERSION"]),
                              current_jdk_distribution=expandvars(principal_data["CURRENT_JDK_DISTRIBUTION"]))

    def write_config(self, config: Config, path: str | None) -> None:
        """
        Writes config to jdkman_config.json both at packge root and at JDKMAN installation path.
        :param config:Updated configurations to write
        :param path:Path to jdkman_config.json to write to. If None is passed, then the jdkman_config.json at package root will be read first to locate the JDKMAN installation path.
        :return: None
        """
        if not path:
            path = self.file_name
        if not os.path.exists(path):
            with open(Path(path), "a") as config_file:
                config_file.write(json.dumps(config.__dict__))
        with open(Path(path).absolute(), "r") as config_file:
            data = json.load(config_file)
            principal_config_path = f'{data["JDKMAN_INSTALLATION_PATH"]}/{self.file_name}'
            with open(os.path.expanduser(principal_config_path), "w") as principal_config_file:
                principal_config_file.write(json.dumps(config.__dict__))
