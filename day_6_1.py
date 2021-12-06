import os
import sys
from operator import attrgetter
from toolz import compose

from typing import *


class LinkedList:

    class Node:
        value: Any
        next: 'LinkedList.Node'

        def __init__(self, value: Any, next_: 'LinkedList.Node' = None):
            self.value = value
            self.next = next_

        def __str__(self) -> str:
            return (f'LinkedList.Node['
                    f'value={self.value}, '
                    f'location={hex(id(self))}, '
                    f'next={None if self.next is None else hex(id(self.next))}]')

        __repr__ = __str__

    class Iterator:
        current_node: 'LinkedList.Node'

        def __init__(self, current_node: 'LinkedList.Node'):
            self.current_node = current_node

        def __next__(self) -> 'LinkedList.Node':
            if self.current_node.next is None:
                raise StopIteration
            else:
                self.current_node = self.current_node.next
                return self.current_node

    root: Node
    end: Node
    len: int

    def __init__(self, values: Iterable[Any] = ()):
        self.root = None
        self.len = 0
        for value in values:
            if self.root is None:
                self.root = LinkedList.Node(value)
                previous_node = self.root
            else:
                current_node = LinkedList.Node(value)
                previous_node.next = current_node
                previous_node = current_node
            self.len += 1

        self.end = None
        try:
            self.end = previous_node
        except NameError:
            pass

    def __iter__(self) -> Node:
        before_root = LinkedList.Node(None, self.root)
        return LinkedList.Iterator(before_root)

    def __len__(self) -> int:
        return self.len

    def __str__(self) -> str:
        return f'LinkedList[len={self.len}][{", ".join(map(compose(repr, attrgetter("value")), self))}]'

    __repr__ = __str__

    def append(self, value: Any):
        new_node = LinkedList.Node(value, None)
        self.end.next = new_node
        self.end = new_node
        self.len += 1

    def extend(self, values: Iterable[Any]):
        for value in values:
            self.append(value)


def pass_day(times_to_reproduce: LinkedList):
    to_spawn = 0
    for node in times_to_reproduce:
        node.value -= 1
        if node.value < 0:
            node.value = 6
            to_spawn += 1
    times_to_reproduce.extend([8] * to_spawn)


INPUT_FILE = os.path.splitext(os.path.split(sys.argv[0])[1])[0] + '_input.txt'

with open(INPUT_FILE) as f:
    raw_data = f.read()


times_to_reproduce = LinkedList(map(int, raw_data.split(',')))

print('Initial state:', times_to_reproduce)
for i in range(1, 80+1):
    pass_day(times_to_reproduce)
    print(f'Len after {i:>3} days:', times_to_reproduce.len)
