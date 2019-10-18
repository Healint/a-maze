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
        return f"{self.__class__.__name__}"

    def _validate_coordinates(self):
        """ indepedent validation of coordinates """
        return


class BoarderTile(BaseTile):

    def __init__(self, dimension, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dimension = dimension
        self._validate_coordinates()

    def _validate_coordinates(self):
        if 0 not in (self.x, self.y) and self.dimension - 1 not in (self.x, self.y):
            raise TileException(f"Invalid Coordinates for {self.x, self.y}")


class Entrance(BoarderTile):
    pass


class Exit(BoarderTile):
    pass


class CorrectPathTile(BaseTile):
    pass
