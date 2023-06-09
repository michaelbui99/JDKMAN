import platform
import sys
from enum import Enum


class Platform(Enum):
    WINDOWS_X64 = 'win_x64'
    WINDOWS_X32 = 'win_x32'
    LINUX_X64 = 'linux_x64'
    LINUX_X32 = 'linux_x32'
    NOT_SUPPORTED = "Not Supported"


def get_platform() -> Platform:
    architecture_info = platform.architecture()
    match sys.platform.lower():
        case 'windows':
            if architecture_info[0] == '64bit':
                return Platform.WINDOWS_X64
            elif architecture_info[0] == '32bit':
                return Platform.WINDOWS_X32
            return Platform.NOT_SUPPORTED

        case 'linux':
            if architecture_info[0] == '64bit':
                return Platform.LINUX_X64
            elif architecture_info[0] == '32bit':
                return Platform.LINUX_X32
            return Platform.NOT_SUPPORTED

        case _:
            return Platform.NOT_SUPPORTED
