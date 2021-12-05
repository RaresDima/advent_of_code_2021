import os
import sys
from operator import methodcaller
from operator import itemgetter
from operator import le
from functools import partial
from toolz import compose
from collections import defaultdict

from typing import *


def sign(x: int) -> int:
    if x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return 1


class VentLine:
    x1: int
    y1: int
    x2: int
    y2: int

    def __init__(self, s: str):
        self.x1, self.y1, self.x2, self.y2 = map(int, s.replace(',', ' -> ').split(' -> '))

    def __str__(self) -> str:
        return f'({self.x1},{self.y1}) -> ({self.x2},{self.y2})'

    __repr__ = __str__

    def is_vertical(self) -> bool:
        return self.x1 == self.x2

    def is_horizontal(self) -> bool:
        return self.y1 == self.y2

    def is_orthogonal(self) -> bool:
        return self.is_vertical() or self.is_horizontal()

    def line_points(self) -> List[Tuple[int, int]]:
        x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2
        points = []
        while True:
            points += [(x1, y1)]
            if x1 == x2 and y1 == y2:
                break
            x_velocity = sign(x2 - x1)
            y_velocity = sign(y2 - y1)
            x1 += x_velocity
            y1 += y_velocity
        return points

    def diagram_str(self, width: int = 10, height: int = 10) -> str:
        points = self.line_points()
        diagram = [['.'] * width
                   for _ in range(height)]
        for x, y in points:
            diagram[y][x] = '1'

        return f'[{self}]\n' + '\n'.join(' '.join(row) for row in diagram)


class VentField:
    lines: List[VentLine]
    points_by_line: List[Set[Tuple[int, int]]]
    lines_trough_point: Dict[Tuple[int, int], int]

    def __init__(self, lines: List[VentLine], orthogonal_only: bool = False):
        if orthogonal_only:
            lines = list(filter(methodcaller('is_orthogonal'), lines))
        else:
            lines = lines.copy()

        self.lines = lines
        self.points_by_line = list(map(compose(set, methodcaller('line_points')), self.lines))
        self.lines_trough_point = defaultdict(int)
        for line_points in self.points_by_line:
            for point in line_points:
                self.lines_trough_point[point] += 1

    def width(self) -> int:
        return max(map(itemgetter(0), self.lines_trough_point.keys())) + 1

    def height(self) -> int:
        return max(map(itemgetter(1), self.lines_trough_point.keys())) + 1

    def diagram_str(self) -> str:
        diagram = [[0] * self.width()
                   for _ in range(self.height())]

        for line_points in self.points_by_line:
            for x, y in line_points:
                diagram[y][x] += 1

        diagram = [['.' if cell == 0 else str(cell)
                    for cell in row]
                   for row in diagram]

        return f'[{len(self.lines)} lines]\n' + '\n'.join(' '.join(row) for row in diagram)


INPUT_FILE = os.path.splitext(os.path.split(sys.argv[0])[1])[0] + '_input.txt'

with open(INPUT_FILE) as f:
    raw_data = f.read()

lines = [VentLine(line) for line in raw_data.split('\n')]

field = VentField(lines, orthogonal_only=True)

print(len(list(filter(partial(le, 2), field.lines_trough_point.values()))))
