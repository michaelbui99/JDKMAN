import platform

import click

from jdkman.cmd.distributions_cmd import distributions
from jdkman.cmd.install_cmd import install
from jdkman.cmd.configure_cmd import configure
from jdkman.cmd.use_cmd import use


@click.group()
def jdkman():
    # Commands root
    pass


jdkman.add_command(distributions)
jdkman.add_command(install)
jdkman.add_command(configure)
jdkman.add_command(use)

if __name__ == '__main__':
    jdkman()
