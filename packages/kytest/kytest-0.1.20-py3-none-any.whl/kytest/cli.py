import click
from . import __version__
from .scaffold import create_scaffold


@click.group()
@click.version_option(version=__version__, help="Show version.")
# 老是变，等最后定下来再搞，目前也没啥用
def main():
    pass


@main.command()
@click.option('-p', '--platform', help="Specify the platform.")
def create(platform):
    """Create a new item."""
    create_scaffold(platform)

