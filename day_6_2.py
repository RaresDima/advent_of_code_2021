import os
import sys

from typing import *


def pass_day(times_to_reproduce: Dict[int, int]):
    to_spawn = times_to_reproduce[0]
    for i in range((8-1)+1):
        times_to_reproduce[i] = times_to_reproduce[i+1]
    times_to_reproduce[8] = to_spawn
    times_to_reproduce[6] += to_spawn


INPUT_FILE = os.path.splitext(os.path.split(sys.argv[0])[1])[0] + '_input.txt'

with open(INPUT_FILE) as f:
    raw_data = f.read()


times_to_reproduce = {i: 0 for i in range(8+1)}
for fish in map(int, raw_data.split(',')):
    times_to_reproduce[fish] += 1

print('Initial state:', times_to_reproduce)
for i in range(1, 256+1):
    pass_day(times_to_reproduce)
    print(f'After {i:>3} days (total {sum(times_to_reproduce.values())}):', times_to_reproduce)
