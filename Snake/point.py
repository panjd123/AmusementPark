class Point:
    row = 0
    col = 0
    color = (0, 0, 0)

    def __init__(self, row=0, col=0, color=(0, 0, 0)):
        self.row = row
        self.col = col
        self.color = color

    def __eq__(self, rhs):
        return self.row == rhs.row and self.col == rhs.col

    def __str__(self):
        return f'point: {self.row} {self.col}'

    def copy(self):
        return Point(self.row, self.col, self.color)


class SnakeCell(Point):
    def copy(self):
        return SnakeCell(self.row, self.col, self.color)


if __name__ == '__main__':
    pass
