import logging
import numpy as np

from typing import List, Any

logger = logging.getLogger(__name__)


def initialise_maze():
    logger.warning("Initialise a maze ...")

    maze = init_empty_maze(3)

    viz_maze(maze)

    logger.warning("Maze generated. ")


def init_empty_maze(dimension: int) -> List[List[Any]]:
    return [[0 for i in range(dimension)] for j in range(dimension)]


def viz_maze(maze: List[List[Any]]) -> None:
    print(np.matrix(maze))


def generate_correct_path():
    pass


def generate_branches_from_coordinates(x, y, length: int):
    pass


def is_reachable(x, y):
    pass

