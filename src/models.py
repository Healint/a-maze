from src.helpers import TileException

# Should add singleton mixin for entrance and exit


class BaseTile:
    """
    A base class for the maze
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.__class__.__name__} - {self.x},{self.y}"

    def __str__(self):
        return f"{self.__class__.__name__}"[:3] + f"{self.x},{self.y}"

    def _validate_coordinates(self):
        """ independent validation of coordinates """
        return

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Boarder(BaseTile):
    def __init__(self, dimension, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dimension = dimension
        self._validate_coordinates()

    def _validate_coordinates(self):
        if 0 not in (self.x, self.y) and self.dimension - 1 not in (self.x, self.y):
            raise TileException(f"Invalid Coordinates for {self.x, self.y}")


class Entrance(Boarder):
    pass


class Exit(Boarder):
    pass


class BonusExit(BaseTile):
    pass


class Path(BaseTile):
    pass


class SolutionPath(BaseTile):
    pass


class Wall(BaseTile):
    pass


class Trap(BaseTile):
    pass


class StaticSpike(Trap):
    pass


class DynamicSpike(Trap):
    pass


class FireBridge(Trap):
    pass


class Treasure(BaseTile):
    pass


class Armor(Treasure):
    pass
