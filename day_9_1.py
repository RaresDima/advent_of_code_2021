import os
import sys
from operator import ge
from operator import add
from functools import partial
from toolz import compose

import numpy as np

from typing import *


def is_low_point(row: int, col: int, grid: List[List[int]]) -> bool:
    height = grid[row][col]
    neighbours = [grid[row-1][col],
                  grid[row][col-1], grid[row][col+1],
                  grid[row+1][col]]

    return not any(map(partial(ge, height), neighbours))


INPUT_FILE = os.path.splitext(os.path.split(sys.argv[0])[1])[0] + '_input.txt'

with open(INPUT_FILE) as f:
    raw_data = f.read()

heights = list(map(compose(list, partial(map, int)), raw_data.split('\n')))

grid_height = len(heights)
grid_width = len(heights[0])

padded_heights = [[9] * (grid_width+2)] + \
                 [[9] + row + [9] for row in heights] +\
                 [[9] * (grid_width+2)]

low_points = [heights[row][col]
              for row in range(grid_height)
              for col in range(grid_width)
              if is_low_point(row+1, col+1, padded_heights)]

risk_levels = list(map(partial(add, 1), low_points))

print(sum(risk_levels))
