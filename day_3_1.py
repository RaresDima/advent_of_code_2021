import os
import sys
from operator import not_

from typing import *


def parse_bitstring(bitstring: str) -> List[int]:
    return list(map(int, bitstring))


INPUT_FILE = os.path.splitext(os.path.split(sys.argv[0])[1])[0] + '_input.txt'

with open(INPUT_FILE) as f:
    raw_data = f.read()


bitstrings = list(map(parse_bitstring, raw_data.split('\n')))

n_one_bits_per_position = list(map(sum, zip(*bitstrings)))
half_n_bitstrings = len(bitstrings) / 2

gamma_bits = [n_ones > half_n_bitstrings for n_ones in n_one_bits_per_position]
epsilon_bits = list(map(not_, gamma_bits))

gamma = int(''.join(str(int(bit)) for bit in gamma_bits), 2)
epsilon = int(''.join(str(int(bit)) for bit in epsilon_bits), 2)

print(gamma, epsilon, gamma * epsilon)
