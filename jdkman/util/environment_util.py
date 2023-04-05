import os.path
import platform as pf
import subprocess
import sys
import re
from enum import Enum


class Platform(Enum):
    WINDOWS_X64 = 'win_x64'
    WINDOWS_X32 = 'win_x32'
    LINUX_X64 = 'linux_x64'
    LINUX_X32 = 'linux_x32'
    NOT_SUPPORTED = "Not Supported"


def get_platform() -> Platform:
    architecture_info = pf.architecture()
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


def set_environment_variable(env_key: str, env_val: str, platform: Platform, exact: bool):
    """
    Sets an environment variable persistently based on user's OS.
    If the user is using Windows, then the environment variable will be set through setx.
    If the user is using a Linux distribution, then writing to ~/.profile, ~/.bashrc, /etc/environment will be attempted.
    :param env_key: environment variable key e.g. JAVA_HOME
    :param env_val: environment variable value
    :param platform: Platform is necessary since this function is OS dependent
    :param exact: Search for exact match when replacing
    :return:
    """

    def override_environment_variable_in_file(file_path: str, requires_sudo: bool):
        path = os.path.expanduser(file_path)
        if not requires_sudo:
            with open(os.path.expanduser(path), "r+") as f:
                file_content = f.read()
                regex = f'export {env_key}=.*' if not exact else f'export {env_key}={env_val}'
                updated_file_content = re.sub(regex, f'export {env_key}={env_val}\n', file_content)

                if not re.findall(regex, updated_file_content):
                    f.write(f'export {env_key}={env_val}\n')
                    return

                f.seek(0)
                f.write(updated_file_content)
                f.truncate()
        else:
            res = subprocess.run(['cat', os.path.expanduser(path)], shell=True, stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE)
            file_content = ""
            for line in res.stdout:
                file_content += line
            print(file_content)
            regex = f'export {env_key}=.*' if not exact else f'export {env_key}={env_val}'
            updated_file_content = re.sub(regex, f'export {env_key}={env_val}\n', file_content)

            if not re.findall(regex, updated_file_content):
                subprocess.run(['echo', f'export {env_key}={env_val}\n', '|', 'sudo', 'tee', '-a', file_path],
                               shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                return

            subprocess.run(['echo', updated_file_content, '|', 'sudo', 'tee', file_path],
                           shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    match platform:
        case Platform.WINDOWS_X64 | Platform.WINDOWS_X32:
            result = subprocess.run(['setx', env_key, env_val], capture_output=True, shell=True)
            print(result.stdout)
            print(result.stderr)
        case Platform.LINUX_X64 | Platform.LINUX_X32:
            override_environment_variable_in_file('~/.profile', requires_sudo=False)
            override_environment_variable_in_file('~/.bashrc', requires_sudo=False)
            override_environment_variable_in_file('/etc/environment', requires_sudo=True)

        case _:
            return
