class BoundingBox:
    def __init__(self, x1: int = None, y1: int = None, x2: int = None, y2: int = None):
        self.x1: int = x1
        self.y1: int = y1
        self.x2: int = x2
        self.y2: int = y2

    def get(self) -> [int, int, int, int]:
        return [self.x1, self.y1, self.x2, self.y2]

    def set(self, coords: [int, int, int, int]):
        self.x1 = coords[0]
        self.y1 = coords[1]
        self.x2 = coords[2]
        self.y2 = coords[3]

    def __str__(self):
        return f"x1: {self.x1},\ny1: {self.y1},\nx2: {self.x2},\ny2: {self.y2}"
