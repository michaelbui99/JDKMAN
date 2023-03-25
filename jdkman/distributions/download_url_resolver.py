from util.environment_util import Platform
from abc import ABC, abstractmethod


class DownloadUrlResolver(ABC):
    @abstractmethod
    def get_url(self, version: str, platform: Platform) -> str:
        """
        Resolves the JDK download url for a provided distribution specific JDK package version and target platform
        :param version: Distribution specific JDK package version, e.g. 17.40.19 for Azul Zulu
        :param platform: Target platform
        :return:
        """
        pass

    @abstractmethod
    def get_resolved_version(self, version: str):
        """
        Returns the actual version used
        :param version:
        :return:
        """
        pass

    @abstractmethod
    def get_file_to_download(self, version: str, platform: Platform) -> str:
        pass
