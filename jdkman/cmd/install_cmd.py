import click


@click.command('install')
@click.option('--distribution', default='Azul',
              help='JDK distribution to install. use the distributions subcommand to see all supported distributions')
@click.argument("version")
def install(version: str, distribution: str):
    click.echo(f"Install works. Passed version: {version}, distribution: {distribution}")
