import click

from distributions.supported_distributions import SupportedDistribution


@click.command()
def distributions():
    for distribution in SupportedDistribution:
        click.echo(distribution.value)
