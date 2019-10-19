import logging
import numpy as np

from typing import List, Any

from src.models import *

logger = logging.getLogger(__name__)


def viz_maze(maze: List[List[Any]]) -> None:
    maze.reverse()
    for row in maze:
        print("   ".join([str(item) for item in row]) + "\n")


class TileException(Exception):
    pass
