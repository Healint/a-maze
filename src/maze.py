import logging

from typing import List, Any

from src.models import *
from src.helpers import viz_maze

logger = logging.getLogger(__name__)


# entrypoint
def initialise_maze():
    logger.warning("Initialise a maze ...")

    maze = init_empty_maze(5)
    viz_maze(maze)

    logger.warning("Maze generated. ")


# init methods
def init_empty_maze(dimension: int) -> List[List[BaseTile]]:
    """ initialised a square maze """
    return [[BaseTile(i, j) for i in range(dimension)] for j in range(dimension)]


def init_entrance(maze: List[List[BaseTile]]) -> None:
    """ initialise the entrace at any point on the boarder """
    size = len(maze)



def init_exit():
    pass


def generate_correct_path():
    pass


def generate_branches_from_coordinates(x, y, length: int):
    pass


def is_reachable(x, y):
    pass

