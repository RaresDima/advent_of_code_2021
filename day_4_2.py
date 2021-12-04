import os
import sys
from operator import eq
from operator import not_
from functools import partial
from toolz import compose
from itertools import repeat

from typing import *


class BingoBoard:
    board: List[List[int]]
    marked: List[List[bool]]

    def __init__(self, board_str: str):
        self.board = [list(map(int,
                               filter(compose(not_, partial(eq, '')),
                                      row.split(' '))))
                      for row in board_str.split('\n')]

        self.marked = [[False
                        for _2 in range(5)]
                       for _1 in range(5)]

    def __str__(self) -> str:
        board_str = ['Board[']
        for board_row, marked_row in zip(self.board, self.marked):
            row_str = []
            for cell, is_marked in zip(board_row, marked_row):
                cell_str = f'{"*" if is_marked else ""}{cell}'.rjust(3)
                row_str += [cell_str]
            row_str = ' '.join(row_str)
            board_str += [row_str]
        board_str = '\n|'.join(board_str) + '\n]'
        return board_str

    __repr__ = __str__

    def mark(self, number: int):
        for i_row, row in enumerate(self.board):
            for i_cell, cell in enumerate(row):
                if cell == number:
                    self.marked[i_row][i_cell] = True

    def bingo_occurred(self) -> bool:
        if any(map(all, self.marked)):
            return True
        if any(map(all, zip(*self.marked))):
            return True
        return False

    def unmarked_numbers(self) -> List[int]:
        return [cell
                for board_row, marked_row in zip(self.board, self.marked)
                for cell, is_marked in zip(board_row, marked_row)
                if not is_marked]


INPUT_FILE = os.path.splitext(os.path.split(sys.argv[0])[1])[0] + '_input.txt'

with open(INPUT_FILE) as f:
    raw_data = f.read()

called_numbers, *boards = raw_data.split('\n\n')

called_numbers = list(map(int, called_numbers.split(',')))
boards = list(map(BingoBoard, boards))

for called_number in called_numbers:
    winning_boards_this_round = set()
    print('Called number:', called_number)

    for board in boards:
        board.mark(called_number)
        if board.bingo_occurred():
            winning_boards_this_round.add(board)

    boards = [board
              for board in boards
              if board not in winning_boards_this_round]

    print('Boards remaining:', len(boards))
    for board in boards:
        print(board)
    print()

    if len(boards) == 1:
        losing_board = boards[0]

    if len(boards) == 0:
        final_number = called_number
        break

print('Losing board:')
print(losing_board)

print(sum(losing_board.unmarked_numbers()) * final_number)
