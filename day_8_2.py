import os
import sys
from operator import eq
from functools import partial
from toolz import compose

from typing import *


# 0 - 6 segments (like 6, 9) | normally uses segments A B C E F G
# 1 - 2 segments             | normally uses segments C F
# 2 - 5 segments (like 3, 5) | normally uses segments A C D E G
# 3 - 5 segments (like 2, 5) | normally uses segments A C D F G
# 4 - 4 segments             | normally uses segments B C D F
# 5 - 5 segments (like 2, 3) | normally uses segments A B D F G
# 6 - 6 segments (like 0, 9) | normally uses segments A B D E F G
# 7 - 3 segments             | normally uses segments A C F
# 8 - 7 segments             | normally uses segments A B C D E F G
# 9 - 6 segments (like 0, 6) | normally uses segments A B C D F G

signal_letters = 'abcdefg'
signal_letters_set = set(signal_letters)

segments_to_digit = {frozenset(list('abcefg')) : 0,
                     frozenset(list('cf'))     : 1,
                     frozenset(list('acdeg'))  : 2,
                     frozenset(list('acdfg'))  : 3,
                     frozenset(list('bcdf'))   : 4,
                     frozenset(list('abdfg'))  : 5,
                     frozenset(list('abdefg')) : 6,
                     frozenset(list('acf'))    : 7,
                     frozenset(list('abcdefg')): 8,
                     frozenset(list('abcdfg')) : 9}


def print_wires(possible_wires: Dict[str, List[str]]):
    for char, possibilities in possible_wires.items():
        print(f'{char} : {{{" ".join(sorted(list(possibilities)))}}}')
    print('-' * 30)


def unshuffle_wires_and_decode_output(signal: List[str], output: List[str]) -> List[int]:
    global signal_letters
    global signal_letters_set
    global segments_to_digit

    print('Shuffled digits:', signal)

    possible_lights_for_wire = {char: set(signal_letters) for char in signal_letters}

    print_wires(possible_lights_for_wire)

    # Find 1
    # The 2 chars are C, F

    one = next(filter(compose(partial(eq, 2), len), signal))
    for char in one:
        possible_lights_for_wire[char] &= set('cf')

    print_wires(possible_lights_for_wire)

    # Done 1

    # Find 4
    # Uses the same chars as 1 plus B, D.
    # Chars not in 1 are B, D

    four = next(filter(compose(partial(eq, 4), len), signal))
    for char in four:
        if char not in one:
            possible_lights_for_wire[char] &= set('bd')

    print_wires(possible_lights_for_wire)

    # Done 1, 4

    # Find 7
    # Uses the same chars as 1 plus A.
    # Char not in 1 is A.

    seven = next(filter(compose(partial(eq, 3), len), signal))
    for char in seven:
        if char not in one:
            possible_lights_for_wire[char] = {'a'}

    print_wires(possible_lights_for_wire)

    # Done 1, 4, 7

    # find 8
    # 8 uses all segments.
    # No information to be found.

    # Done 1, 4, 7, 8

    # find 0, 6, 9
    # Segments missing from 0, 6, 9 are D, C, E.

    zero_six_nine = list(filter(compose(partial(eq, 6), len), signal))
    for number in zero_six_nine:
        number_chars_set = set(number)
        missing_char = next(iter(signal_letters_set - number_chars_set))
        possible_lights_for_wire[missing_char] &= set('dce')

    print_wires(possible_lights_for_wire)

    # Done 0, 1, 4, 6, 7, 8, 9

    n_found_letters = 0

    while True:

        found_letters = {next(iter(possibilities))
                         for char, possibilities in possible_lights_for_wire.items()
                         if len(possibilities) == 1}

        no_new_letters_found = len(found_letters) <= n_found_letters
        if no_new_letters_found:
            break
        else:
            n_found_letters = len(found_letters)

        print(f'Found letters: {{{" ".join(sorted(list(found_letters)))}}}')

        for possibilities in possible_lights_for_wire.values():
            if len(possibilities) == 1:
                continue
            for found_letter in found_letters:
                if found_letter in possibilities:
                    possibilities.remove(found_letter)

        print_wires(possible_lights_for_wire)

    # Read possible_lights_for_wire like this:
    # possible_lights_for_wire[A] == C
    # A wire lights up C light

    wire_to_light = {wire: next(iter(light))
                     for wire, light
                     in possible_lights_for_wire.items()}

    print('Original output:  ', [''.join(d) for d in output])

    translated_output = [frozenset(wire_to_light[light]
                                   for light in output_segments)
                         for output_segments in output]

    print('Translated output:', [''.join(d) for d in translated_output])

    output_digits = [segments_to_digit[segments] for segments in translated_output]

    print('Digits:', output_digits)

    return output_digits


INPUT_FILE = os.path.splitext(os.path.split(sys.argv[0])[1])[0] + '_input.txt'

with open(INPUT_FILE) as f:
    raw_data = f.read()


lines = [[half.split(' ')
          for half in line.split(' | ')]
         for line in raw_data.split('\n')]

signals, outputs = zip(*lines)

output_numbers = []
for signal, output in zip(signals, outputs):
    output_digits = unshuffle_wires_and_decode_output(signal, output)
    output_numbers += [int(''.join(map(str, output_digits)))]

print('Output numbers:', output_numbers)

print(sum(output_numbers))
