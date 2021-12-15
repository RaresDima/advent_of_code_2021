import os
import sys
from functools import partial
from toolz import compose
import multiprocessing


import numpy as np

from typing import *


np.set_printoptions(linewidth=5000)


def get_neighbours(row: int, col: int) -> List[Tuple[int, int]]:
    global risks

    last_row = risks.shape[0] - 1
    last_col = risks.shape[1] - 1

    neighbours = []
    if row > 0:
        neighbours += [(row - 1, col)]
    if row < last_row:
        neighbours += [(row + 1, col)]
    if col > 0:
        neighbours += [(row, col - 1)]
    if col < last_col:
        neighbours += [(row, col + 1)]

    return neighbours


def risk_of_least_risk_path(row: int, col: int,
                            end_row: int, end_col: int,
                            risks: np.ndarray) -> int:

    frontier_cost_evaluations = 0

    start_location = (row, col)
    destination_location = (end_row, end_col)

    visited_locations = set()
    unvisited_locations = {(row_index, col_index)
                           for row_index, row in enumerate(risks)
                           for col_index, col in enumerate(row)}

    frontier = {start_location}

    risk_to_reach = {(row_index, col_index): float('inf')
                     for row_index, row in enumerate(risks)
                     for col_index, col in enumerate(row)}

    risk_to_reach[start_location] = 0

    current_location = start_location

    while True:

        unvisited_neighbours = [neighbour
                                for neighbour in get_neighbours(*current_location)
                                if neighbour not in visited_locations]


        for neighbour in unvisited_neighbours:
            neighbour_row, neighbour_col = neighbour

            current_risk_to_reach = risk_to_reach[neighbour]
            risk_to_reach_trough_current_location = risk_to_reach[current_location] + \
                                                    risks[neighbour_row, neighbour_col]

            if risk_to_reach_trough_current_location < current_risk_to_reach:
                risk_to_reach[neighbour] = risk_to_reach_trough_current_location

        visited_locations.add(current_location)
        unvisited_locations.remove(current_location)

        frontier.update(unvisited_neighbours)
        frontier.remove(current_location)

        if destination_location in visited_locations:
            return risk_to_reach[destination_location]

        current_location = min((risk_to_reach[location[0],
                                              location[1]],
                                location)
                               for location in frontier)[1]

        frontier_cost_evaluations += len(frontier)
        if len(visited_locations) % 1000 == 0:
            print(f'Visited {len(visited_locations)//1000}k nodes '
                  f'({len(unvisited_locations)//1000}k left). '
                  f'{frontier_cost_evaluations} cost evaluations done.')



def increment_tile(original_tile: np.ndarray) -> np.ndarray:
    tile = original_tile.copy()
    tile += 1
    tile[tile == 10] = 1
    return tile


def expand_tile(original_tile: np.ndarray, num_rows: int, num_cols: int) -> np.ndarray:
    row_origins = [original_tile]
    for row_index in range(1, num_rows):
        row_origins += [increment_tile(row_origins[-1])]

    rows = []
    for row_index in range(num_rows):
        row = [row_origins[row_index]]
        for col_index in range(1, num_cols):
            row += [increment_tile(row[-1])]
        rows += [row]

    expanded_tile = np.vstack([np.hstack(row) for row in rows])
    return expanded_tile


INPUT_FILE = os.path.splitext(os.path.split(sys.argv[0])[1])[0] + '_input.txt'

with open(INPUT_FILE) as f:
    raw_data = f.read()

risks = np.array(list(map(compose(list, partial(map, int)), raw_data.split('\n'))))

risks = expand_tile(risks, 5, 5)
height, width = risks.shape

print(risks)
print(f'h x w = {height} x {width}')
print(risk_of_least_risk_path(0, 0, height-1, width-1, risks))
