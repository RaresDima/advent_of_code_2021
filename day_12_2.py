import os
import sys
from itertools import chain
from operator import methodcaller
from collections import defaultdict
from collections import deque

from typing import *


class CaveSystemGraph:
    neighbours: Dict[str, Set[str]]
    small_nodes: Set[str]
    big_nodes: Set[str]

    def __init__(self, nodes: List[str], edges: List[List[str]]):
        self.big_nodes = set(filter(methodcaller('isupper'), nodes))
        self.small_nodes = set(filter(methodcaller('islower'), nodes))
        self.neighbours = defaultdict(set)
        for node1, node2 in edges:
            self.neighbours[node1].add(node2)
            self.neighbours[node2].add(node1)

    def __str__(self) -> str:
        start = 'Graph['
        mid = [f'| {node}: [{"  ".join(neighbours)}]'
               for node, neighbours
               in self.neighbours.items()]
        end = ']'
        return '\n'.join([start, *mid, end])

    __repr__ = __str__


    def _find_paths_from_start_to_end(self,
                                      current_path: Deque[str],
                                      visited_big: Deque[str],
                                      visited_small: Set[str],
                                      medium_cave: str,
                                      medium_cave_visits: int,
                                      start_to_end_paths: Deque[Deque[str]]):

        current_node = current_path[-1]

        if current_node == 'end':
            start_to_end_paths.append(current_path.copy())
            return

        viable_neighbours = self.neighbours[current_node] - visited_small

        if not viable_neighbours:
            return

        for neighbour in viable_neighbours:

            current_path.append(neighbour)
            if neighbour in self.big_nodes:
                visited_big.append(neighbour)
            else:
                if neighbour == medium_cave:
                    medium_cave_visits += 1
                    if medium_cave_visits == 2:
                        visited_small.add(neighbour)
                else:
                    visited_small.add(neighbour)

            self._find_paths_from_start_to_end(current_path,
                                               visited_big,
                                               visited_small,
                                               medium_cave,
                                               medium_cave_visits,
                                               start_to_end_paths)

            current_path.pop()
            if neighbour in self.big_nodes:
                visited_big.remove(neighbour)
            else:
                if neighbour == medium_cave:
                    medium_cave_visits -= 1
                    if medium_cave_visits == 1:
                        visited_small.remove(neighbour)
                else:
                    visited_small.remove(neighbour)

    def find_all_paths_from_start_to_end(self) -> Set[Tuple[str]]:
        current_path = deque(['start'])
        visited_big = deque()
        visited_small = {'start'}

        start_to_end_paths = deque()

        possible_medium_caves = self.small_nodes - {'start', 'end'}
        initial_medium_cave_visits = 0
        for medium_cave in possible_medium_caves:
            self._find_paths_from_start_to_end(current_path,
                                               visited_big,
                                               visited_small,
                                               medium_cave,
                                               initial_medium_cave_visits,
                                               start_to_end_paths)

        start_to_end_paths = set(map(tuple, start_to_end_paths))

        return start_to_end_paths


INPUT_FILE = os.path.splitext(os.path.split(sys.argv[0])[1])[0] + '_input.txt'

with open(INPUT_FILE) as f:
    raw_data = f.read()

edges = [edge.split('-') for edge in raw_data.split('\n')]
nodes = set(chain.from_iterable(edges))

cave_system = CaveSystemGraph(nodes, edges)

print(cave_system)

paths = cave_system.find_all_paths_from_start_to_end()

for i, path in enumerate(sorted(list(paths)), 1):
    print(f'Path {i:3}: {" - ".join(path)}')
