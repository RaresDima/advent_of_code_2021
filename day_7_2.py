import os
import sys
from statistics import mean

from typing import *


def get_fuel_required_for_crab_movement(crab_position: int, target_position: int) -> int:
    distance = abs(crab_position - target_position)
    return round(distance * (distance + 1) / 2)


def get_fuel_required_for_alignment_target(alignment_target: int, crab_positions: List[int]) -> int:
    return sum(get_fuel_required_for_crab_movement(crab_position, alignment_target)
               for crab_position in crab_positions)



INPUT_FILE = os.path.splitext(os.path.split(sys.argv[0])[1])[0] + '_input.txt'

with open(INPUT_FILE) as f:
    raw_data = f.read()


crab_positions = list(map(int, raw_data.split(',')))

alignment_target = round(mean(crab_positions))
fuel_required = get_fuel_required_for_alignment_target(alignment_target, crab_positions)

print(f'Aligned on {alignment_target} for {fuel_required} fuel.')

while True:
    alignment_target_candidates = [alignment_target + 1, alignment_target - 1]
    candidate_fuels_required = [get_fuel_required_for_alignment_target(alignment_target_candidate, crab_positions)
                                for alignment_target_candidate in alignment_target_candidates]

    best_candidate_index = min(range(1+1), key=lambda i: candidate_fuels_required[i])
    best_alignment_target_candidate = alignment_target_candidates[best_candidate_index]
    best_candidate_fuel_required = candidate_fuels_required[best_candidate_index]

    if best_candidate_fuel_required < fuel_required:
        alignment_target = best_alignment_target_candidate
        fuel_required = best_candidate_fuel_required
        print(f'Aligned on {alignment_target} for {fuel_required} fuel.')
    else:
        break
