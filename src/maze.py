import logging
import random

from typing import List, Any

from src.models import *
from src.helpers import viz_maze

logger = logging.getLogger(__name__)


class MazeGenerator:

    def __init__(self, dimension: int = 5):
        self.dimension = dimension
        self.maze = None
        self.entrance = None
        self.exit = None

    def initialise_maze(self):
        logger.warning("Initialise a maze ...")

        # initialise basic maze
        self.maze = self._init_empty_maze()
        self._init_entrance()
        # self._init_exit()

        # visualise maze
        viz_maze(self.maze)

        # validation checks
        self.solve_maze()
        logger.warning("Maze generated. ")

    def _init_empty_maze(self) -> List[List[BaseTile]]:
        """ initialised a square maze with BaseTiles """
        return [
            [
                BaseTile(i, j) for i in range(self.dimension)
            ]
            for j in range(self.dimension)
        ]

    def _init_entrance(self) -> None:
        """ initialise the entrace at any point on the boarder """
        remains = self._get_remaining_border_tiles()
        entrance_x, entrance_y = random.choice(remains)
        self.entrance = BoarderTile(x=entrance_x, y=entrance_y, dimension=self.dimension)
        self.maze[entrance_x][entrance_y] = self.entrance

    def _init_exit(self):
        remains = self._get_remaining_border_tiles(excluding_neighbors=[self.entrance])
        x, y = random.choice(remains)
        self.exit = BoarderTile(x=x, y=y, dimension=self.dimension)
        self.maze[x][y] = self.exit

    def solve_maze(self):
        pass

    def _get_remaining_tiles(self):
        """
        Compute remaining tiles as a list of tuples
        """
        result = []

        for i in range(self.dimension):
            for j in range(self.dimension):
                if isinstance(self.maze[i][j], BaseTile):
                    result.append((i, j))

        return result

    def _get_remaining_border_tiles(self, excluding_neighbors: List = None):
        """
        Compute remaining tiles as a list of tuples
        """
        result = []

        for i in range(self.dimension):
            for j in range(self.dimension):
                if not isinstance(self.maze[i][j], BaseTile):
                    continue

                if 0 not in (i, j) and self.dimension - 1 not in (i, j):
                    continue

                result.append((i, j))

        # excluding neighbors if required
        if excluding_neighbors is not None:
            final_result = []
            for tile in result:
                for exclusion in excluding_neighbors:
                    if not self.is_neighbor(BaseTile(tile[0], tile[1]), exclusion):
                        final_result.append(tile)

            result = final_result

        print(self.entrance)
        print(result)

        return result

    @staticmethod
    def is_neighbor(this: Any, other: Any) -> bool:
        if this is other:
            raise Exception("Not allowed to check neighbor for the same object")

        # Too lazy to google or think of algo
        neighbours_tiles_coor = [
            (this.x + 1, this.y),
            (this.x - 1, this.y),
            (this.x, this.y + 1),
            (this.x, this.y - 1)
        ]

        if (other.x, other.y) in neighbours_tiles_coor:
            return True

        return False


def generate_correct_path():
    pass


def generate_branches_from_coordinates(x, y, length: int):
    pass


def is_reachable(x, y):
    pass

