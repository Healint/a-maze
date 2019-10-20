import click

from src.maze import MazeGenerator


@click.group()
def cli():
    pass


@cli.command()
def init_maze():
    MazeGenerator(
        dimension=10, traps={"FireBridge": 2, "DynamicSpike": 2, "StaticSpike": 2}
    ).initialise_maze()


if __name__ == "__main__":
    cli()
