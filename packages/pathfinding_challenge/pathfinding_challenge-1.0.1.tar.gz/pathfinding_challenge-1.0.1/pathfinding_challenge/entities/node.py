from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from pathfinding_challenge import InvalidComparisonError
from pathfinding_challenge.entities.position import Position


@dataclass(slots=True)
class Node(ABC):
    weight: float
    position: Position = field(default_factory=Position)

    @abstractmethod
    def __hash__(self) -> int:
        """Return a hash value for the object."""
        return hash((self.position.x, self.position.y))

    def __eq__(self, other: Any) -> bool:
        """
        Determine the equality between two objects.
        """
        if not isinstance(other, Node):
            raise InvalidComparisonError(
                f'Cannot compare Node with {type(other)}'
            )
        return self.weight == other.weight

    def __lt__(self, other: Any) -> bool:
        """
        Compare two nodes by their weight.
        """
        if not isinstance(other, Node):
            raise InvalidComparisonError(
                f'Cannot compare Node with {type(other)}'
            )
        return self.weight < other.weight

    def __gt__(self, other: Any) -> bool:
        """
        Compare two nodes by their weight.
        """
        if not isinstance(other, Node):
            raise InvalidComparisonError(
                f'Cannot compare Node with {type(other)}'
            )
        return self.weight > other.weight

    def __ne__(self, other: Any) -> bool:
        """
        Compare two nodes by their weight.
        """
        if not isinstance(other, Node):
            raise InvalidComparisonError(
                f'Cannot compare Node with {type(other)}'
            )
        return self.weight != other.weight
