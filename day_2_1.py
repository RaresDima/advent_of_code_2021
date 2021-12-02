import os
import sys

from typing import *


def parse_instruction(instruction_str: str) -> Tuple[str, int]:
    direction, distance = instruction_str.split()
    return direction, int(distance)


direction_handler = {
    'forward': lambda distance, position, depth: (position + distance, depth),
    'up'     : lambda distance, position, depth: (position, depth - distance),
    'down'   : lambda distance, position, depth: (position, depth + distance)
}


INPUT_FILE = os.path.splitext(os.path.split(sys.argv[0])[1])[0] + '_input.txt'

with open(INPUT_FILE) as f:
    raw_data = f.read()

instructions = list(map(parse_instruction, raw_data.split('\n')))

position, depth = 0, 0
for direction, distance in instructions:
    position, depth = direction_handler[direction](distance, position, depth)

print(position * depth)
