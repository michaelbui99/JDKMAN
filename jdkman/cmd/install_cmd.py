import click
from jdkman.jdk_manager.jdk_manager import JdkManager
from jdkman.distributions.supported_distributions import SupportedDistribution


@click.command('install')
@click.option('--distribution', default='Zulu',
              help='JDK distribution to install. use the distributions subcommand to see all supported distributions')
@click.argument("version")
def install(version: str, distribution: str):
    manager = JdkManager()
    result = manager.install_new_jdk_version(version=version, distribution=SupportedDistribution(distribution))
    click.echo(f'Installation {result.value}')
