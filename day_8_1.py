import os
import sys
from itertools import chain

from typing import *

# 0 - 6 segments (like 6, 9)
# 1 - 2 segments
# 2 - 5 segments (like 3, 5)
# 3 - 5 segments (like 2, 5)
# 4 - 4 segments
# 5 - 5 segments (like 2, 3)
# 6 - 6 segments (like 0, 9)
# 7 - 3 segments
# 8 - 7 segments
# 9 - 6 segments (like 0, 6)


INPUT_FILE = os.path.splitext(os.path.split(sys.argv[0])[1])[0] + '_input.txt'

with open(INPUT_FILE) as f:
    raw_data = f.read()


lines = [[half.split(' ')
          for half in line.split(' | ')]
         for line in raw_data.split('\n')]

signals, outputs = zip(*lines)

relevant_output_lens = {2, 4, 3, 7}

print(sum((len(output) in relevant_output_lens) for output in chain.from_iterable(outputs)))
