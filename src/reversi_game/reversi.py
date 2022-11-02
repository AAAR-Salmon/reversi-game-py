import numpy as np
import itertools as it
from typing import List, Tuple
from .color import Color
from .exceptions import InplaceableError, NoneColorError


class Reversi:
    def __init__(self, height: int, width: int) -> None:
        self.height = height
        self.width = width
        self.turn = Color.DARK
        self.__init_board(width, height)

    def __init_board(self, height: int, width: int) -> None:
        board = np.full((height, width), Color.NONE, np.uint8)
        _u, _v = height // 2 - 1, width // 2 - 1
        board[_u, _v], board[_u, _v+1] = Color.LIGHT, Color.DARK
        board[_u+1, _v], board[_u+1, _v+1] = Color.DARK, Color.LIGHT
        self.board = board

    def __in_board(self, row: int, column: int) -> bool:
        return 0 <= row < self.height and 0 <= column < self.width

    def __calc_indices_to_be_flipped(self, row: int, column: int, color: Color) -> List[Tuple[int, int]]:
        result: List[Tuple[int, int]] = []
        if color == Color.NONE:
            raise NoneColorError()
        for delta_row, delta_column in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            # 同じ色か空白が来るまで探す
            for distance in it.count(1):
                _target_row = row+delta_row*distance
                _target_column = column+delta_column*distance
                if not self.__in_board(_target_row, _target_column):
                    break
                if self.board[_target_row, _target_column] == Color.NONE:
                    break
                if self.board[_target_row, _target_column] == color:  # 見つかった
                    result.extend([(row+delta_row*i, column+delta_column*i)
                                  for i in range(1, distance)])
        return result

    def get_placeable_coords(self, color: Color) -> List[Tuple[int, int]]:
        return [(row, column) for row in range(self.height) for column in range(self.width) if self.is_placeable(row, column, color)]

    def is_placeable(self, row: int, column: int, color: Color) -> bool:
        _indices = self.__calc_indices_to_be_flipped(row, column, color)
        return len(_indices) != 0

    def place_disk(self, row: int, column: int, color: Color) -> None:
        _indices = self.__calc_indices_to_be_flipped(row, column, color)
        if len(_indices) == 0:
            raise InplaceableError(row, column, color)
        self.board[row, column] = color
        for index in _indices:
            self.board[index] = color

    def forward_turn(self) -> Color:
        can_opposite_player_place = len(self.get_placeable_coords(self.turn.next())) != 0
        can_current_player_place = len(self.get_placeable_coords(self.turn)) != 0
        if not can_opposite_player_place and not can_current_player_place:
            return Color.NONE
        if not can_opposite_player_place:
            return self.turn
        return self.turn.next()
