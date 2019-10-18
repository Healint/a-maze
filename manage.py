import click

from src.maze import initialise_maze


@click.group()
def cli():
    pass


@cli.command()
def init_maze():
    initialise_maze()


if __name__ == '__main__':
    cli()
