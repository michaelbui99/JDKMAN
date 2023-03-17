import click
from enum import Enum


class SupportedDistributions(Enum):
    AZUL = 'Azul'


@click.command()
def distributions():
    for distribution in SupportedDistributions:
        click.echo(distribution.value)
