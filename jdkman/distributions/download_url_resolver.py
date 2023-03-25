from abc import ABC, abstractmethod


class DownloadUrlResolver(ABC):
    @abstractmethod
    def get_url(self, version: str, platform: Platform) -> str:
        pass

    @abstractmethod
    def get_file_to_download(self, version: str, platform: Platform) -> str:
        pass
