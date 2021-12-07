import os
import sys
from statistics import median

from typing import *


INPUT_FILE = os.path.splitext(os.path.split(sys.argv[0])[1])[0] + '_input.txt'

with open(INPUT_FILE) as f:
    raw_data = f.read()


crab_positions = list(map(int, raw_data.split(',')))

alignment_target = round(median(crab_positions))
fuel_required = sum(abs(alignment_target - crab_position)
                        for crab_position in crab_positions)

print(f'Aligned on {alignment_target} for {fuel_required} fuel.')
