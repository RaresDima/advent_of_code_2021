import os
import sys
from collections import deque
from collections import defaultdict
from collections import Counter
from operator import add

from typing import *


INPUT_FILE = os.path.splitext(os.path.split(sys.argv[0])[1])[0] + '_input.txt'

with open(INPUT_FILE) as f:
    raw_data = f.read()

polymer, insertion_rules = raw_data.split('\n\n')

polymer = defaultdict(int, **Counter(map(add, polymer[:-1], polymer[1:])))
insertion_rules = dict(rule.split(' -> ') for rule in insertion_rules.split('\n'))

print(f'Initial polymer (size={sum(polymer.values())+1}): {dict(polymer)}')

for i in range(40):
    new_polymer = defaultdict(int)
    for pair, times in polymer.items():
        element1, element2 = pair
        new_element = insertion_rules[pair]
        new_pair1 = element1 + new_element
        new_pair2 = new_element + element2
        new_polymer[new_pair1] += times
        new_polymer[new_pair2] += times
    polymer = new_polymer

    print(f'Polymer after {i+1:2} insertions (size={sum(polymer.values())+1}): {dict(polymer)}')

counts = defaultdict(int)
for (element1, element2), times in polymer.items():
    counts[element1] += times
    counts[element2] += times

for element in counts:
    if counts[element] % 2 == 1:
        counts[element] += 1
    counts[element] //= 2

print(counts)

most_occurrences = max(counts.values())
least_occurrences = min(counts.values())
print(most_occurrences - least_occurrences)


