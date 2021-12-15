import os
import sys
from functools import lru_cache
from functools import partial
from toolz import compose
from collections import defaultdict
from collections import deque

import numpy as np

from typing import *


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

    start = (row, col)

    cost_to_reach_from_start_location = defaultdict(lambda: float('inf'))
    cost_to_reach_from_start_location[start] = 0

    to_evaluate_cost_to_neighbours = deque([start])

    while to_evaluate_cost_to_neighbours:

        current = to_evaluate_cost_to_neighbours.popleft()
        neighoburs = get_neighbours(*current)

        for neighobur in neighoburs:
            neighbour_row, neighbour_col = neighobur

            current_cost_to_neighbour = cost_to_reach_from_start_location[neighobur]
            possible_cost_to_neighbour = cost_to_reach_from_start_location[current] + \
                                         risks[neighbour_row, neighbour_col]

            if possible_cost_to_neighbour < current_cost_to_neighbour:
                print(f'Cost to reach {neighobur} went from {current_cost_to_neighbour} to {possible_cost_to_neighbour}.')
                cost_to_reach_from_start_location[neighobur] = possible_cost_to_neighbour
                to_evaluate_cost_to_neighbours.append(neighobur)

    return cost_to_reach_from_start_location[(end_row, end_col)]


INPUT_FILE = os.path.splitext(os.path.split(sys.argv[0])[1])[0] + '_input.txt'

with open(INPUT_FILE) as f:
    raw_data = f.read()

risks = np.array(list(map(compose(list, partial(map, int)), raw_data.split('\n'))))
height, width = risks.shape

print(risks)
print(f'h x w = {height} x {width}')
print(risk_of_least_risk_path(0, 0, height-1, width-1, risks))
