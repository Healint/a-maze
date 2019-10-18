import click

from src.maze import MazeGenerator


@click.group()
def cli():
    pass


@cli.command()
def init_maze():
    MazeGenerator().initialise_maze()


if __name__ == '__main__':
    cli()
