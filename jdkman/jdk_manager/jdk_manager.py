import os
from enum import Enum
from pathlib import Path
from .config_handler import ConfigHandler
from distributions.supported_distributions import SupportedDistribution
from distributions.download_url_resolver_factory import DownloadUrlResolverFactory
from util import environment_util, io_util


class InstallResult(Enum):
    ALREADY_INSTALLED = 'Already Installed',
    SUCCESS = 'Success',
    FAIL = 'Fail'


class JdkManager:
    def __init__(self):
        self.config_handler = ConfigHandler()
        self.download_url_resolver_factory = DownloadUrlResolverFactory()

    def install_new_jdk_version(self, version: str, distribution: SupportedDistribution) -> InstallResult:
        config = self.config_handler.parse_config_file()

        target_path = Path(f'{config.JDK_INSTALLATIONS_PATH}/distributions/{distribution.value}/{version}')
        resolved_target_path = io_util.as_expanded_path(str(target_path.resolve()))

        platform = environment_util.get_platform()
        url_resolver = self.download_url_resolver_factory.get_resolver(distribution)
        zip_file = url_resolver.get_file_to_download(version=version, platform=platform)

        if Path.exists(Path(f'{str(resolved_target_path)}/{zip_file.split(".zip")[0]}')):
            return InstallResult.ALREADY_INSTALLED

        os.makedirs(target_path, exist_ok=True)

        io_util.download_from_url(url_resolver.get_url(version=version, platform=platform),
                                  str(Path(f'{str(resolved_target_path)}/{zip_file}').absolute()))
        io_util.unzip(
            str(Path(f'{str(resolved_target_path)}/{zip_file}').absolute()),
            str(Path(f'{str(resolved_target_path)}').absolute()))

        os.remove(Path(f'{str(resolved_target_path)}/{zip_file}').absolute())

        return InstallResult.SUCCESS
