import platform

import click
from cmd.supported_distributions import distributions


@click.group()
def jdkman():
    # Commands root
    pass


jdkman.add_command(distributions)

if __name__ == '__main__':
    jdkman()
