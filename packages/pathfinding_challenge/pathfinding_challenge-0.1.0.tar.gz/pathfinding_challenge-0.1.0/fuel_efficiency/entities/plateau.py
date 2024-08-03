from dataclasses import dataclass, field

from fuel_efficiency.entities.node import Node
from fuel_efficiency.entities.position import Position


@dataclass(slots=True)
class Plateau(Node):
    weight: float = float(1)
    position: Position = field(default_factory=Position)

    def __hash__(self):
        """Return a hash value for the object."""
        return hash((self.position.x, self.position.y))

    def __eq__(self, other):
        if (
            not hasattr(self, 'weight')
            or not hasattr(self, 'position')
            or not hasattr(other, 'weight')
            or not hasattr(other, 'position')
        ):
            raise NotImplementedError(
                'Missing `position` or `weight` attribute'
            )
        return self.position == other.position

    def __lt__(self, other: 'Plateau') -> bool:
        if not hasattr(self, 'weight') or not hasattr(other, 'weight'):
            raise NotImplementedError('Missing `weight` attribute')
        return self.weight < other.weight

    def __gt__(self, other: 'Plateau') -> bool:
        if not hasattr(self, 'weight') or not hasattr(other, 'weight'):
            raise NotImplementedError('Missing `weight` attribute')
        return self.weight > other.weight

    def __ne__(self, other: 'Plateau') -> bool:
        if not hasattr(self, 'weight') or not hasattr(other, 'weight'):
            raise NotImplementedError('Missing `weight` attribute')
        return self.weight != other.weight
