from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from fuel_efficiency.entities.position import Position


@dataclass(slots=True)
class Node(ABC):
    weight: float
    position: Position = field(default_factory=Position)

    # @staticmethod
    # def compare(node1: 'Node', node2: 'Node') -> bool:
    #     """
    #     Compares two nodes based on their 'weight' attribute.

    #     Args:
    #         node1 (Node): The first node to compare.
    #         node2 (Node): The second node to compare.

    #     Returns:
    #         bool: True if the weight of node1 is less than the
    #         weight of node2, otherwise False.

    #     Raises:
    #         ValueError: If node1 and node2 are of different types.

    #     Example:
    #         node1 = Valley(weight=1.0, position=Position(x=0, y=0))
    #         node2 = Valley(weight=2.0, position=Position(x=1, y=1))
    #         result = Node.compare(node1, node2)
    #         # result will be True because 1.0 < 2.0

    #     Notes:
    #         - This method assumes that both nodes are of the same type and
    #         have a 'weight' attribute.
    #         - If the nodes are of different types, a ValueError will
    #           be raised.
    #     """
    #     if type(node1) is not type(node2):
    #         raise ValueError('Cannot compare nodes of different types.')
    #     return node1.weight < node2.weight
    @abstractmethod
    def __hash__(self) -> int:
        """Return a hash value for the object."""
        return hash((self.position.x, self.position.y))

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Node):
            return NotImplemented
        return self.weight < other.weight

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, Node):
            return NotImplemented
        return self.weight > other.weight

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Node):
            return NotImplemented
        return self.weight == other.weight

    def __ne__(self, other: Any) -> bool:
        if not isinstance(other, Node):
            return NotImplemented
        return self.weight != other.weight
