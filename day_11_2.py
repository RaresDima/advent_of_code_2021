import os
import sys
from functools import partial
from toolz import compose

import numpy as np

from typing import *


def get_neighbour_coords(row: int, col: int, height: int, width: int) -> List[Tuple[int, int]]:
    up_left = (row-1, col-1)
    up = (row-1, col)
    up_right = (row-1, col+1)

    left = (row, col-1)
    right = (row, col+1)

    down_left = (row+1, col-1)
    down = (row+1, col)
    down_right = (row+1, col+1)

    neighbour_coords = {up_left, up, up_right,
                        left, right,
                        down_left, down, down_right}

    if row == 0:
        neighbour_coords.remove(up_left)
        neighbour_coords.remove(up)
        neighbour_coords.remove(up_right)

    if row == height-1:
        neighbour_coords.remove(down_left)
        neighbour_coords.remove(down)
        neighbour_coords.remove(down_right)

    if col == 0:
        neighbour_coords.remove(left)
        if up_left in neighbour_coords:
            neighbour_coords.remove(up_left)
        if down_left in neighbour_coords:
            neighbour_coords.remove(down_left)

    if col == width-1:
        neighbour_coords.remove(right)
        if up_right in neighbour_coords:
            neighbour_coords.remove(up_right)
        if down_right in neighbour_coords:
            neighbour_coords.remove(down_right)

    return list(neighbour_coords)


def pass_time(energy_levels: np.ndarray) -> int:
    flashes = 0
    energy_levels += 1

    while energy_levels[energy_levels > 9].any():

        flashes += energy_levels[energy_levels > 9].size
        flash_locations = np.argwhere(energy_levels > 9)

        flash_neighbour_lists = [get_neighbour_coords(*location, *energy_levels.shape)
                                 for location in flash_locations]

        energy_levels[energy_levels > 9] = -100

        for flash_neighbour_list in flash_neighbour_lists:
            energy_levels[tuple(zip(*flash_neighbour_list))] += 1

    energy_levels[energy_levels < 0] = 0

    return flashes


INPUT_FILE = os.path.splitext(os.path.split(sys.argv[0])[1])[0] + '_input.txt'

with open(INPUT_FILE) as f:
    raw_data = f.read()

energy_levels = np.array(list(map(compose(list, partial(map, int)), raw_data.split('\n'))))
total_flashes = 0

print('Before any steps:')
print(energy_levels)

i = 0
while True:
    flashes = pass_time(energy_levels)
    total_flashes += flashes

    print(f'After step {i+1}:')
    print(energy_levels)
    print(f'Flashes this step: {flashes}')
    print(f'Total flashes: {total_flashes}')

    if flashes == energy_levels.size:
        print(f'Synched sfter step {i+1}!')
        break
    else:
        i += 1
