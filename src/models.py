class BaseTile:
    """
    A base class for the maze
    """
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return self.__class__.__name__


class Entrance(BaseTile):
    """The entrance of the maze"""
    pass


class Exit(BaseTile):
    """The exit tile of the maze"""
    pass


class CorrectPathTile(BaseTile):
    pass
