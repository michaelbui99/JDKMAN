import platform

import click

from jdkman.cmd.distributions_cmd import distributions
from jdkman.cmd.install_cmd import install
from jdkman.cmd.configure_cmd import configure


@click.group()
def jdkman():
    # Commands root
    pass


jdkman.add_command(distributions)
jdkman.add_command(install)
jdkman.add_command(configure)

if __name__ == '__main__':
    jdkman()
