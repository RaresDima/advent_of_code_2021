import os
import sys

import numpy as np

from typing import *

np.set_printoptions(linewidth=400)


class DotSheet:
    dot_sheet: np.ndarray
    allow_unequal_folds: bool

    def __init__(self, dots: Sequence[Tuple[int, int]], allow_unequal_folds: bool = False):
        xs, ys = list(zip(*dots))
        cols = max(xs) + 1
        rows = max(ys) + 1

        self.dot_sheet = np.zeros((rows, cols), dtype=np.bool)
        self.dot_sheet[ys, xs] = True

        self.allow_unequal_folds = allow_unequal_folds

    def __str__(self) -> str:
        rows, cols = self.dot_sheet.shape
        return '\n'.join((f'DotSheet[',
                          f'  dims: {rows} x {cols}',
                          f'  dots: {self.num_dots()}',
                          f'  sheet:',
                          '    ' +
                          str(self.dot_sheet).replace('[', '')
                                             .replace(']', '')
                                             .replace(' True', '#')
                                             .replace('False', '.')
                                             .replace('\n', '\n   '),
                          ']'))

    __repr__ = __str__

    def num_dots(self) -> int:
        return self.dot_sheet.sum()

    def fold_up(self, y: int):
        upper_half = self.dot_sheet[:y]
        lower_half = self.dot_sheet[y+1:]

        lower_half_flipped = np.flipud(lower_half)

        if upper_half.shape == lower_half_flipped.shape:
            self.dot_sheet = np.logical_or(upper_half, lower_half_flipped)
            return

        if not self.allow_unequal_folds:
            print(upper_half.shape)
            print(lower_half_flipped.shape)
            raise ValueError(f'Unequal halves for folding up. y={y}')

        upper_half_rows = upper_half.shape[0]
        lower_half_flipped_rows = lower_half_flipped.shape[0]
        if upper_half_rows < lower_half_flipped_rows:
            smaller_half = upper_half
            taller_half = lower_half_flipped
        else:
            smaller_half = lower_half_flipped
            taller_half = upper_half

        width = upper_half.shape[1]
        height_difference = abs(upper_half_rows - lower_half_flipped_rows)
        empty_rows = np.zeros((height_difference, width), dtype=np.bool)

        smaller_half = np.vstack((empty_rows, smaller_half))

        self.dot_sheet = np.logical_or(smaller_half, taller_half)

    def fold_left(self, x: int):
        left_half = self.dot_sheet[:, :x]
        right_half = self.dot_sheet[:, x+1:]

        right_half_flipped = np.fliplr(right_half)

        if left_half.shape == right_half_flipped.shape:
            self.dot_sheet = np.logical_or(left_half, right_half_flipped)
            return

        if not self.allow_unequal_folds:
            raise ValueError(f'Unequal halves for folding left. x={x}')

        left_half_cols = left_half.shape[1]
        right_half_flipped_cols = right_half_flipped.shape[1]
        if left_half_cols < right_half_flipped_cols:
            smaller_half = left_half
            wider_half = right_half_flipped
        else:
            smaller_half = right_half_flipped
            wider_half = left_half

        height = left_half.shape[0]
        width_difference = abs(left_half_cols - right_half_flipped_cols)
        empty_rows = np.zeros((height, width_difference), dtype=np.bool)

        smaller_half = np.hstack((empty_rows, smaller_half))

        self.dot_sheet = np.logical_or(smaller_half, wider_half)



INPUT_FILE = os.path.splitext(os.path.split(sys.argv[0])[1])[0] + '_input.txt'

with open(INPUT_FILE) as f:
    raw_data = f.read()

dots, folds = raw_data.split('\n\n')

dots = [list(map(int, dot.split(',')))
        for dot in dots.split('\n')]

folds = [(lambda t: (t[0], int(t[1])))(fold[11:].split('='))
         for fold in folds.split('\n')]

sheet = DotSheet(dots, allow_unequal_folds=True)
print(sheet)

for direction, coordinate in folds:
    print(f'Folding along {direction}={coordinate}')

    if direction == 'x':
        sheet.fold_left(coordinate)
    else:
        sheet.fold_up(coordinate)

    print(sheet)
