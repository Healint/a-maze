import logging
import numpy as np
import json

from typing import List, Any

from src.models import *

logger = logging.getLogger(__name__)


def viz_maze(maze: List[List[Any]]) -> None:
    maze.reverse()
    for row in maze:
        print("  ".join([str(item) for item in row]) + "\n")


class TileException(Exception):
    pass


def serialise_maze(maze: List[List[Any]]):
    for i in range(len(maze)):
        for j in range(len(maze)):
            maze[i][j] = maze[i][j].__class__.__name__
    return maze
