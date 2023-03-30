import click
from jdkman.jdk_manager.jdk_manager import JdkManager, GenericCommandResult
from jdkman.distributions.supported_distributions import SupportedDistribution


@click.command('use')
@click.option('--distribution', default='Zulu',
              help='JDK distribution and version to use.')
@click.argument("version")
def use(version: str, distribution: str):
    manager = JdkManager()
    result = manager.use_jdk(distribution=SupportedDistribution(distribution), version=version)

    match result:
        case GenericCommandResult.FAIL:
            click.echo(f'Failed to use JDK {distribution} {version}')
        case GenericCommandResult.SUCCESS:
            click.echo(f'{distribution} {version}')
