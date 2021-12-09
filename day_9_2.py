import os
import sys
from operator import ge
from operator import mul
from functools import partial
from functools import reduce
from toolz import compose

import numpy as np

from typing import *


def is_low_point(row: int, col: int, grid: List[List[int]]) -> bool:
    height = grid[row][col]
    neighbours = [grid[row-1][col],
                  grid[row][col-1], grid[row][col+1],
                  grid[row+1][col]]

    return not any(map(partial(ge, height), neighbours))


def find_basin_from_low_point(row: int, col: int, grid: List[List[int]]) -> Set[Tuple[int, int]]:
    low_point_coords = (row, col)

    basin = {low_point_coords}
    outside_this_basin = set()

    basin_frontier = {low_point_coords}

    while basin_frontier:
        frontier_location = next(iter(basin_frontier))

        frontier_location_row, frontier_location_col = frontier_location

        frontier_location_neighbours = [(frontier_location_row - 1, frontier_location_col),
                                        (frontier_location_row, frontier_location_col - 1),
                                        (frontier_location_row, frontier_location_col + 1),
                                        (frontier_location_row + 1, frontier_location_col)]

        unvisited_frontier_location_neighbours = [neighbour
                                                  for neighbour in frontier_location_neighbours
                                                  if neighbour not in outside_this_basin
                                                  and neighbour not in basin]

        frontier_location_height = grid[row][col]
        for neighbour in unvisited_frontier_location_neighbours:
            neighbour_row, neighbour_col = neighbour
            neighbour_height = grid[neighbour_row][neighbour_col]
            if frontier_location_height < neighbour_height < 9:
                basin.add(neighbour)
                basin_frontier.add(neighbour)
            else:
                outside_this_basin.add(neighbour)

        basin_frontier.remove(frontier_location)

    return basin



INPUT_FILE = os.path.splitext(os.path.split(sys.argv[0])[1])[0] + '_input.txt'

with open(INPUT_FILE) as f:
    raw_data = f.read()

heights = list(map(compose(list, partial(map, int)), raw_data.split('\n')))

grid_height = len(heights)
grid_width = len(heights[0])

padded_heights = [[9] * (grid_width+2)] + \
                 [[9] + row + [9] for row in heights] +\
                 [[9] * (grid_width+2)]

low_point_locations = [(row, col)
                       for row in range(grid_height)
                       for col in range(grid_width)
                       if is_low_point(row+1, col+1, padded_heights)]

basins = [find_basin_from_low_point(row+1, col+1, padded_heights)
          for row, col in low_point_locations]

print(reduce(mul, sorted(map(len, basins), reverse=True)[:3]))
