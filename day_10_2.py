import os
import sys
from collections import deque
from statistics import median

from typing import *


opening_symbols = {'(', '[', '{', '<'}
closing_symbols = {'(': ')',
                   '[': ']',
                   '{': '}',
                   '<': '>'}

repair_values = {')': 1,
                 ']': 2,
                 '}': 3,
                 '>': 4}


INPUT_FILE = os.path.splitext(os.path.split(sys.argv[0])[1])[0] + '_input.txt'

with open(INPUT_FILE) as f:
    raw_data = f.read()

lines = raw_data.split('\n')

repair_scores = []
for line in lines:
    print(f'LINE: {line}', end='\t')
    open_chunks = deque()
    for symbol in line:
        if symbol in opening_symbols:
            open_chunks.append(symbol)
        else:
            last_open_symbol = open_chunks.pop()
            if symbol != closing_symbols[last_open_symbol]:
                print(f'CORRUPTED: '
                      f'last open chunk does not match current symbol: '
                      f'{last_open_symbol} and {symbol}')
                break
    else:
        if open_chunks:
            print(f'INCOMPLETE LINE: open chunks {"".join(open_chunks)} ', end=' ')
            repairing_symbols = deque()
            repair_score = 0
            while open_chunks:
                repairing_symbols.append(closing_symbols[open_chunks.pop()])
                repair_score = repair_score * 5 + repair_values[repairing_symbols[-1]]
            repair_scores += [repair_score]
            print(f'can be repaired with {"".join(repairing_symbols)} (score {repair_score})')
        else:
            print('OK')

print(f'REPAIR SCORE: {median(repair_scores)}')

