import click
import os
from pathlib import Path
from util.io_util import as_expanded_path
from jdk_manager.config_handler import ConfigHandler, Config


@click.command('configure')
def configure():
    config_handler = ConfigHandler()

    install_path_input = input('Enter installation directory (default: $HOME/JDKMAN): ')
    if not install_path_input:
        install_path_input = as_expanded_path("$HOME/JDKMAN/")

    install_path = as_expanded_path(install_path_input)
    if not Path.exists(install_path):
        os.makedirs(install_path, exist_ok=True)
        os.makedirs(Path(f'{install_path}/distributions'))

    config = Config(jdkman_installation_path=str(install_path), current_jdk_distribution="", current_jdk_version="")
    config_handler.write_config(config=config, path=config.JDKMAN_INSTALLATION_PATH)
    config_handler.write_config(config=config, path=as_expanded_path("./"))
    print(f'JDKMAN has been configured. Configurations and distributions can be found at: {install_path}')
