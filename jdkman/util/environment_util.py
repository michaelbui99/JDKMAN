import sys
from enum import Enum


class Platform(Enum):
    WINDOWS = 'Windows'
    LINUX = 'Linux'
    NOT_SUPPORTED = "Not Supported"


def get_platform() -> Platform:
    match sys.platform.lower():
        case 'windows':
            return Platform.WINDOWS
        case 'linux':
            return Platform.LINUX
        case _:
            return Platform.NOT_SUPPORTED
