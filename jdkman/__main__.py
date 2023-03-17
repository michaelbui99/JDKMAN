import platform

import click

from cmd.distributions_cmd import distributions
from cmd.install_cmd import install


@click.group()
def jdkman():
    # Commands root
    pass


jdkman.add_command(distributions)
jdkman.add_command(install)

if __name__ == '__main__':
    jdkman()
