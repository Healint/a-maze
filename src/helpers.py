import logging
import numpy as np

from typing import List, Any

from src.models import *

logger = logging.getLogger(__name__)


def viz_maze(maze: List[List[Any]]) -> None:
    print(np.matrix(maze))


class TileException(Exception):
    pass
