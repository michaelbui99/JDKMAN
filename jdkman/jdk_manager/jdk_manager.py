import os
import traceback
from enum import Enum
from pathlib import Path
from .config_handler import ConfigHandler, Config
from jdkman.distributions.supported_distributions import SupportedDistribution
from jdkman.distributions.download_url_resolver_factory import DownloadUrlResolverFactory
from jdkman.util import environment_util, io_util


class InstallResult(Enum):
    ALREADY_INSTALLED = 'Already Installed'
    SUCCESS = 'Success'
    FAIL = 'Fail'


class GenericCommandResult(Enum):
    SUCCESS = 'Success'
    FAIL = 'Fail'


class JdkManager:
    def __init__(self):
        self.config_handler = ConfigHandler()
        self.download_url_resolver_factory = DownloadUrlResolverFactory()

    def install_new_jdk_version(self, version: str, distribution: SupportedDistribution) -> InstallResult:
        """
        Install a new JDK version to <JDKMAN_INSTALLATION_PATH>/distributions/<DISTRIBUTION>/<VERSION>/jdk
        :param version: Version to install
        :param distribution: JDK distribution, e.g. Zulu, Coretto etc.
        :return: InstallResult of either SUCCESS or FAIL
        """
        try:
            print(f'Install target: {distribution.value} {version}')
            config = self.config_handler.parse_config_file(None)
            url_resolver = self.download_url_resolver_factory.get_resolver(distribution)
            version = url_resolver.get_resolved_version(version)

            target_path = self.get_target_path(version, distribution, config)
            resolved_target_path = io_util.as_expanded_path(str(target_path.resolve()))

            platform = environment_util.get_platform()
            zip_file = url_resolver.get_file_to_download(version=version, platform=platform)

            extracted_jdk_folder_name = f'{str(resolved_target_path)}/{zip_file.split(".zip")[0]}'
            if Path.exists(Path(extracted_jdk_folder_name)):
                return InstallResult.ALREADY_INSTALLED

            os.makedirs(target_path, exist_ok=True)

            download_url = url_resolver.get_url(version=version, platform=platform)
            download_to_path = str(Path(f'{str(resolved_target_path)}/{zip_file}').absolute())
            print(f'Downloading {distribution.value} {version} JDK from {download_url} to {download_to_path}')
            io_util.download_from_url(download_url, download_to_path)

            print(f'Unzipping {download_to_path}')
            io_util.unzip(
                download_to_path,
                str(Path(f'{str(resolved_target_path)}').absolute()))

            os.rename(extracted_jdk_folder_name, f'{str(resolved_target_path)}/jdk')
            os.remove(Path(f'{str(resolved_target_path)}/{zip_file}').absolute())

            return InstallResult.SUCCESS
        except Exception:
            traceback.print_exc()
            return InstallResult.FAIL

    def get_target_path(self, version: str, distribution: SupportedDistribution, config: Config) -> Path:
        """
        Target installation path
        :param version: JDK version
        :param distribution: JDK distribution
        :param config: JDKMAN config
        :return:
        """
        return Path(f'{config.JDKMAN_INSTALLATION_PATH}/distributions/{distribution.value}/{version}')

    def set_java_home(self, jdk_path: str) -> None:
        """
        Set JAVA_HOME environment variable persistently
        :param jdk_path: path to JDK
        :return:None
        """
        platform = environment_util.get_platform()
        environment_util.set_environment_variable("JAVA_HOME", jdk_path, platform, exact=False)
        environment_util.set_environment_variable("PATH", f'$PATH:{jdk_path}/bin', platform, exact=True)

    def use_jdk(self, distribution: SupportedDistribution, version: str) -> GenericCommandResult:
        """
        Set JAVA_HOME persistently to specified JDK distribution and version, if the JDK is installed.
        :param distribution: JDK distribution
        :param version: JDK version
        :return: GenericCommandResult of either FAIL or SUCCESS
        """
        config = self.config_handler.parse_config_file(None)
        if not self.jdk_is_installed(distribution=distribution, version=version, config=config):
            print("JDK is not installed. Aborting...")
            return GenericCommandResult.FAIL

        config.CURRENT_JDK_DISTRIBUTION = distribution.value
        config.CURRENT_JDK_VERSION = version
        self.config_handler.write_config(config, None)
        try:
            self.set_java_home(
                jdk_path=str(Path(f'{config.JDKMAN_INSTALLATION_PATH}/distributions/{distribution.value}/{version}/jdk').resolve()))
            return GenericCommandResult.SUCCESS
        except Exception:
            traceback.print_exc()
            return GenericCommandResult.FAIL

    def jdk_is_installed(self, distribution: SupportedDistribution, version: str, config: Config) -> bool:
        """
        Check if a specific JDK is installed.
        :param distribution: JDK distribution
        :param version: JDK version
        :param config: JDKMAN config
        :return: True if installed, else False
        """
        path = Path(
            f'{io_util.as_expanded_path(config.JDKMAN_INSTALLATION_PATH)}/distributions/{distribution.value}/{version}')
        return path.exists()
