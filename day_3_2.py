import os
import sys
from operator import itemgetter
from operator import eq
from functools import partial
from toolz import compose

from typing import *


def parse_bitstring(bitstring: str) -> List[int]:
    return list(map(int, bitstring))


INPUT_FILE = os.path.splitext(os.path.split(sys.argv[0])[1])[0] + '_input.txt'

with open(INPUT_FILE) as f:
    raw_data = f.read()

initial_bitstrings = list(map(parse_bitstring, raw_data.split('\n')))

current_index = 0
bitstrings = initial_bitstrings
while True:
    n_one_bits_at_position_i = sum(map(itemgetter(current_index), bitstrings))
    half_n_bitstrings = len(bitstrings) / 2

    most_common_bit = int(n_one_bits_at_position_i >= half_n_bitstrings)

    bitstrings = list(filter(compose(partial(eq, most_common_bit), itemgetter(current_index)), bitstrings))
    current_index += 1

    print('Finding Oxygen... candidates left:', len(bitstrings))

    if len(bitstrings) == 1:
        break

oxygen = int(''.join(map(str, bitstrings[0])), 2)

print(f'Oxygen is {bitstrings[0]} ({oxygen})')


current_index = 0
bitstrings = initial_bitstrings
while True:
    n_one_bits_at_position_i = sum(map(itemgetter(current_index), bitstrings))
    half_n_bitstrings = len(bitstrings) / 2

    least_common_bit = int(n_one_bits_at_position_i < half_n_bitstrings)

    bitstrings = list(filter(compose(partial(eq, least_common_bit), itemgetter(current_index)), bitstrings))
    current_index += 1

    print('Finding CO2... candidates left:', len(bitstrings))

    if len(bitstrings) == 1:
        break

co2 = int(''.join(map(str, bitstrings[0])), 2)

print(f'CO2 is {bitstrings[0]} ({co2})')

print(oxygen * co2)
