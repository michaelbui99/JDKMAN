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


class JdkManager:
    def __init__(self):
        self.config_handler = ConfigHandler()
        self.download_url_resolver_factory = DownloadUrlResolverFactory()

    def install_new_jdk_version(self, version: str, distribution: SupportedDistribution) -> InstallResult:
        try:
            print(f'Install target: {distribution.value} {version}')
            config = self.config_handler.parse_config_file()
            url_resolver = self.download_url_resolver_factory.get_resolver(distribution)
            version = url_resolver.get_resolved_version(version)

            target_path = self.get_target_path(version, distribution, config)
            resolved_target_path = io_util.as_expanded_path(str(target_path.resolve()))

            platform = environment_util.get_platform()
            zip_file = url_resolver.get_file_to_download(version=version, platform=platform)

            if Path.exists(Path(f'{str(resolved_target_path)}/{zip_file.split(".zip")[0]}')):
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

            os.remove(Path(f'{str(resolved_target_path)}/{zip_file}').absolute())

            return InstallResult.SUCCESS
        except Exception:
            traceback.print_exc()
            return InstallResult.FAIL

    def get_target_path(self, version: str, distribution: SupportedDistribution, config: Config) -> Path:
        return Path(f'{config.JDKMAN_INSTALLATION_PATH}/distributions/{distribution.value}/{version}')
