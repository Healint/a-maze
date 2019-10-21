import logging
import random

from typing import List, Any

from src.models import *
from src.helpers import viz_maze

logger = logging.getLogger(__name__)


class MazeGenerator:
    def __init__(self, traps: dict, dimension: int):
        self.dimension = dimension
        self.traps = traps
        self.maze = None
        self.object_maze = None
        self.entrance = None
        self.exit = None
        self.walked_path = []
        self.complexity = self.dimension * 5  # complexity of branches

    def initialise_maze(self):
        logger.warning("Initialise a maze ...")

        # initialise basic maze
        self.maze = self._init_base_maze()
        self.object_maze = self._init_empty_maze()
        self._init_entrance()
        self._init_exit()
        self._init_correct()
        self._init_branches(self.complexity)
        self._paint_walked_path()
        self._init_wall()

        # traps and stuff for object layer
        self._adding_on_path(n=self.traps["FireBridge"], trap_type=FireBridge)
        self._adding_on_path(n=self.traps["DynamicSpike"], trap_type=DynamicSpike)
        self._adding_on_wall(n=self.traps["StaticSpike"], tile_type=StaticSpike)
        self._init_bonus_exit()

        viz_maze(self.maze)
        viz_maze(self.object_maze)

        logger.warning("Maze generated. ")

    # -- init methods --

    def _init_base_maze(self) -> List[List[BaseTile]]:
        """ initialised a square maze with BaseTiles """
        return [
            [BaseTile(j, i) for i in range(self.dimension)]
            for j in range(self.dimension)
        ]

    def _init_empty_maze(self) -> List[List]:
        """ initialised a square maze with BaseTiles """
        return [[None for i in range(self.dimension)] for j in range(self.dimension)]

    def _init_entrance(self) -> None:
        """ initialise the entrance at any point on the boarder """
        remains = self._get_remaining_base_border_tiles()

        chosen_tile = random.choice(remains)

        # avoid corner respawn
        while (
            abs(chosen_tile.x - chosen_tile.y) == 0
            or abs(chosen_tile.x - chosen_tile.y) == self.dimension - 1
        ):
            chosen_tile = random.choice(remains)

        self.entrance = Entrance(self.dimension, x=chosen_tile.x, y=chosen_tile.y)
        self._replace_tile(chosen_tile, self.entrance)

    def _init_exit(self):
        remains = self._get_remaining_base_border_tiles(
            excluding_neighbors=[self.entrance]
        )
        chosen_tile = random.choice(remains)

        while (
            abs(chosen_tile.x - chosen_tile.y) == 0
            or abs(chosen_tile.x - chosen_tile.y) == self.dimension - 1
        ):
            chosen_tile = random.choice(remains)

        self.exit = Exit(self.dimension, x=chosen_tile.x, y=chosen_tile.y)
        self._replace_tile(chosen_tile, self.exit)

    def _init_bonus_exit(self):
        replacing_tile = random.choice(self.walked_path)
        self._replace_tile(
            replacing_tile, BonusExit(replacing_tile.x, replacing_tile.y)
        )

    def _init_correct(self):
        self._random_walk_painting(start=self.entrance, end=self.exit)

    def _init_branches(self, n: int):
        for i in range(n):
            self._random_walk_painting(
                start=random.choice(self.walked_path)  # picked from any walked path
            )

    def _adding_on_path(self, n: int, trap_type: Any):
        paths = self._get_tiles("Path")
        for i in range(n):
            trap_tile = random.choice(paths)
            paths.remove(trap_tile)
            self._replace_tile_object_maze(
                trap_tile, trap_type(trap_tile.x, trap_tile.y)
            )

    def _adding_on_wall(self, n: int, tile_type: Any):
        paths = self._get_tiles("Wall")

        for i in range(n):
            replacing_tile = random.choice(paths)
            paths.remove(replacing_tile)
            self._replace_tile_object_maze(
                replacing_tile, tile_type(replacing_tile.x, replacing_tile.y)
            )
            self._replace_tile(replacing_tile, None)

    def _init_treasures(self):
        pass

    def _init_boarder(self):
        self.boarder_tiles = []
        for base_tile in self._get_remaining_base_border_tiles():
            replacing_tile = Boarder(self.dimension, base_tile.x, base_tile.y)
            self._replace_tile(base_tile, replacing_tile)
            self.boarder_tiles.append(replacing_tile)

    def _init_wall(self):
        """
        generate walls after the completion of path
        including the boarders
        :return:
        """
        for remain in self._get_tiles("BaseTile"):
            self._replace_tile(remain, Wall(remain.x, remain.y))

    # -- helpers --

    def _paint_walked_path(self):
        for tile in self.walked_path:
            if tile is not self.entrance or tile is not self.exit:
                self._replace_tile(tile, Path(tile.x, tile.y))

    def _get_tiles(self, tile_type: str):
        """
        Compute remaining tiles as a list of tuples
        """
        result = []

        for i in range(self.dimension):
            for j in range(self.dimension):
                if not _check_tile_type(self.maze[i][j], tile_type):
                    continue

                result.append(eval(tile_type)(i, j))

        return result

    def _get_remaining_base_border_tiles(self, excluding_neighbors: List = None):
        """
        Compute remaining tiles as a list of tuples
        """
        result = []

        for i in range(self.dimension):
            for j in range(self.dimension):
                if not _check_tile_type(self.maze[i][j], "BaseTile"):
                    continue

                if 0 not in (i, j) and self.dimension - 1 not in (i, j):
                    continue

                result.append(BaseTile(i, j))

        # excluding neighbors if required
        if excluding_neighbors is not None:
            final_result = []
            for tile in result:
                for exclusion in excluding_neighbors:
                    if not is_neighbor(tile, exclusion):
                        final_result.append(tile)

            result = final_result

        return result

    def _get_walkable_neighbors(
        self, current_tile: Any, previous_step: Any = None
    ) -> List:
        # should be tested
        # I am doing this stupid logic again ...
        result = []
        for x in [current_tile.x - 1, current_tile.x, current_tile.x + 1]:
            for y in [current_tile.y - 1, current_tile.y, current_tile.y + 1]:
                if -1 < x < self.dimension and -1 < y < self.dimension:
                    if not (
                        current_tile.x == x and current_tile.y == y
                    ):  # not the original point
                        if not (
                            current_tile.x != x and current_tile.y != y
                        ):  # not moving at the same time
                            result.append(self.maze[x][y])

        # remove blocks such as boarder tile and wall
        result = [item for item in result if not _check_tile_type(item, "Boarder")]

        if previous_step is not None:
            result.remove(previous_step)

        return result

    def _replace_tile(self, this: Any, other: Any):
        self.maze[this.x][this.y] = other

    def _replace_tile_object_maze(self, this: Any, other: Any):
        self.object_maze[this.x][this.y] = other

    def _random_walk_painting(self, start, end=None, walk_before_turn: int = 2):
        """
        Recursively paint the path with a type of tile

        Stop condition

        1. reach end (if on, will avoid boarder)
        2. reach boarder

        Random Walk from a starting point, on all connected BaseTiles
        """
        avoiding_wall = False
        if end is not None:
            logger.warning("End tile provided, destined to reach the end. ")
            avoiding_wall = True

        while True:
            per_loop_counter = 0
            current_tile = start
            current_walked_path = []

            while per_loop_counter <= 10:

                if current_tile is not self.entrance:
                    current_walked_path.append(current_tile)

                # random
                next_steps = self._get_walkable_neighbors(current_tile)

                if self.exit in next_steps:
                    logger.warning(f"Random Walk reach exit. ")
                    break

                if avoiding_wall and end in next_steps:
                    logger.warning(f"Random Walk reach destination. Exit at {end}")
                    break

                # generate path not neighbouring each other
                existing_path = current_walked_path + self.walked_path
                feasible_next_steps = [
                    tile
                    for tile in next_steps
                    if not is_touching_path(tile, current_tile, existing_path)
                ]

                # exclude dead ends to generate correct path
                if avoiding_wall:
                    # remove dead ends if searching for end
                    feasible_next_steps = [
                        tile
                        for tile in feasible_next_steps
                        if not self._is_dead_end(tile)
                    ]

                if len(feasible_next_steps) == 0:

                    if avoiding_wall:
                        # turning back as searching for end
                        current_tile = random.choice(current_walked_path)
                        per_loop_counter += 1
                    else:
                        logger.warning("Reaching a dead end. ")
                        break
                else:
                    # walked
                    current_tile = random.choice(
                        feasible_next_steps
                    )  # as new as current

            if per_loop_counter < 10:
                logger.warning("Maze Path generated")

                self.walked_path.extend(current_walked_path)

                break
            else:
                logger.warning("Retry to generate a path")

    def _is_dead_end(self, this: Any) -> bool:
        """
        test whether the given walking tile is next to boarder
        """
        return len(self._get_walkable_neighbors(this)) == 1


def is_touching_path(this: Any, prev: Any, path: List) -> bool:
    """
    test whether the given walking tile is touching a list of tiles
    except its prev path
    """
    for item in path:

        if item is prev:
            continue

        if item is this:  # crossed path before
            continue

        if is_neighbor(this, item):
            return True

    return False


def is_reachable(this: Any, other: Any, maze: List[List[Any]]) -> None:
    """
    Test in a give maze, the path is reachable from one place to another
    Note this ignoring any additional effect such as traps
    """
    pass


def is_neighbor(this: Any, other: Any) -> bool:
    if this is other:
        raise Exception("Not allowed to check neighbor for the same object")

    # Too lazy to google or think of algo
    neighbours_tiles_coor = [
        (this.x + 1, this.y),
        (this.x - 1, this.y),
        (this.x, this.y + 1),
        (this.x, this.y - 1),
    ]

    if (other.x, other.y) in neighbours_tiles_coor:
        return True

    return False


def _check_tile_type(this, type_of_tile) -> bool:
    """
    Check tile against a string tile type
    """
    if this.__class__.__name__ == type_of_tile:
        return True

    return False
