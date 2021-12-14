import os
import sys
from collections import deque
from collections import Counter

from typing import *


def do_insertions(polymer: Deque[str], insertion_rules: Dict[str, str]) -> Deque[str]:
    new_polymer = deque([polymer[0]])
    index1, index2 = 0, 1

    while index2 < len(polymer):
        element1 = polymer[index1]
        element2 = polymer[index2]
        pair = element1 + element2
        if pair in insertion_rules:
            new_element = insertion_rules[pair]
            new_polymer.append(new_element)
        new_polymer.append(element2)
        index1 += 1
        index2 += 1

    return new_polymer


INPUT_FILE = os.path.splitext(os.path.split(sys.argv[0])[1])[0] + '_input.txt'

with open(INPUT_FILE) as f:
    raw_data = f.read()

polymer, insertion_rules = raw_data.split('\n\n')

polymer = deque(polymer)
insertion_rules = dict(rule.split(' -> ') for rule in insertion_rules.split('\n'))

print(insertion_rules)

print(f'Initial polymer (size={len(polymer)}): {"".join(polymer)}')

for i in range(10):
    polymer = do_insertions(polymer, insertion_rules)
    print(f'Polymer after {i+1:2} insertions (size={len(polymer):5}): {"".join(polymer)}')

counts = Counter(polymer)
most_occurrences = max(counts.values())
least_occurrences = min(counts.values())
print(counts)
print(most_occurrences - least_occurrences)
