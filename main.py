#!/usr/bin/env python

import random
from color import Color
from reversi import Reversi


def main():
    reversi = Reversi(8, 8)
    player_turn = random.choice([Color.DARK, Color.LIGHT])
    while reversi.turn != Color.NONE:
        print(reversi.board)
        row, column = map(int, input(f'color={reversi.turn} R C > ').split())
        reversi.place_disk(row, column, reversi.turn)
        reversi.turn = reversi.forward_turn()
        # break


if __name__ == '__main__':
    main()
