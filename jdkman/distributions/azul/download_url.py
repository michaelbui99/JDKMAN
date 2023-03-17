from util.environment_util import get_platform, Platform

download_url_root = "https://cdn.azul.com/zulu/bin/zulu17.40.19-ca-jdk17.0.6-linux_x64.zip"


class DownloadUrlResolver:
    def __init__(self):
        self.download_url_root = "https://cdn.azul.com/zulu/bin/"
    def get_url(self, version: str, platform: Platform) -> str:
        return ""
