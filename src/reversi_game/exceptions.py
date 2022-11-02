class ReversiError(Exception):
    def __init__(self) -> None:
        pass


class NoneColorError(ReversiError):
    def __str__(self) -> str:
        return 'cannot place disk of color NONE'


class InplaceableError(ReversiError):
    def __init__(self, row, column, color) -> None:
        super().__init__()

        self.row = row
        self.column = column
        self.color = color

    def __str__(self) -> str:
        return f'cannot place disk of color #{self.color} on ({self.row}, {self.column})'
