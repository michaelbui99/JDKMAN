import click

from distributions.supported_distributions import SupportedDistributions


@click.command()
def distributions():
    for distribution in SupportedDistributions:
        click.echo(distribution.value)
