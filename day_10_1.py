import os
import sys
from collections import deque

from typing import *


opening_symbols = {'(', '[', '{', '<'}
closing_symbols = {'(': ')',
                   '[': ']',
                   '{': '}',
                   '<': '>'}

error_scores = {')': 3,
                ']': 57,
                '}': 1197,
                '>': 25137}


INPUT_FILE = os.path.splitext(os.path.split(sys.argv[0])[1])[0] + '_input.txt'

with open(INPUT_FILE) as f:
    raw_data = f.read()

lines = raw_data.split('\n')

error_score = 0
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
                      f'last open chunk does not match current symbol '
                      f'("{last_open_symbol}" and "{symbol}")')
                error_score += error_scores[symbol]
                break
    else:
        print('OK')

print(f'ERROR SCORE: {error_score}')

