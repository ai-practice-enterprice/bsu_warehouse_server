class Node():
    def __init__(
        self,
        x: int,
        y: int,
        type: int,
        neigbours: dict
    ):
        self.x: int = x
        self.y: int = y
        self.type: int = type
        self.neigbours: dict = neigbours


