import click
from jdk_manager.jdk_manager import JdkManager
from distributions.supported_distributions import SupportedDistribution
from distributions.azul_zulu.zulu_download_url_resolver import ZuluDownloadUrlResolver
from util.environment_util import get_platform


@click.command('install')
@click.option('--distribution', default='Zulu',
              help='JDK distribution to install. use the distributions subcommand to see all supported distributions')
@click.argument("version")
def install(version: str, distribution: str):
    resolver = ZuluDownloadUrlResolver()
    manager = JdkManager()

    result = manager.install_new_jdk_version(version=version, distribution=SupportedDistribution(distribution))
    click.echo(f'Installation {result.value}')
