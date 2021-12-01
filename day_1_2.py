import os
import sys


INPUT_FILE = os.path.splitext(os.path.split(sys.argv[0])[1])[0] + '_input.txt'

with open(INPUT_FILE) as f:
    raw_data = f.read()

depths = list(map(int, raw_data.split()))

window_depths = [sum(depths[i: i+3]) for i in range(0, len(depths)-2)]

num_descents = 0
for prev_depth, curr_depth in zip(window_depths[:-1], window_depths[1:]):
    if curr_depth > prev_depth:
        num_descents += 1

print(num_descents)
