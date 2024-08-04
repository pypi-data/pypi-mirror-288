from dataclasses import dataclass, field

from pathfinding_challenge import MissingAttrError
from pathfinding_challenge.entities.node import Node
from pathfinding_challenge.entities.position import Position


@dataclass(slots=True)
class DownHill(Node):
    """
    Represents a DownHill terrain node in the grid.

    Attributes:
        weight (float): The weight or difficulty of traversing this terrain.
                        Defaults to 0.5.
        position (Position): The position of this node in the grid.
                             Defaults to a new Position instance.
    """

    weight: float = float(0.5)
    position: Position = field(default_factory=Position)

    def __hash__(self) -> int:
        """
        Return a hash value for the object.

        Returns:
            int: A hash based on the x and y coordinates of the position.
        """
        return hash((self.position.x, self.position.y))

    def __eq__(self, other):
        """
        Determine the equality between DownHill and other objects.

        Args:
            other: The other DownHill object to compare with.

        Returns:
            bool: True if both objects have the same position, False otherwise.

        Raises:
            MissingAttrError: If the 'position' or 'weight' attribute is
                                 missing in either object.
        """
        if (
            not hasattr(self, 'weight')
            or not hasattr(self, 'position')
            or not hasattr(other, 'weight')
            or not hasattr(other, 'position')
        ):
            raise MissingAttrError('Missing `position` or `weight` attribute')
        return self.position == other.position

    def __lt__(self, other) -> bool:
        """
        Compare a DownHill node and other node by their weight.

        Args:
            other: The other DownHill object to compare with.

        Returns:
            bool: True if the current object's weight is less than the other's,
                  False otherwise.

        Raises:
            MissingAttrError: If the 'weight' attribute is missing in
            either object.
        """
        if not hasattr(self, 'weight') or not hasattr(other, 'weight'):
            raise MissingAttrError('Missing `weight` attribute')
        return self.weight < other.weight

    def __gt__(self, other) -> bool:
        """
        Compare a DownHill node and other node by their weight.

        Args:
            other: The other DownHill object to compare with.

        Returns:
            bool: True if the current object's weight is less than the other's,
                  False otherwise.

        Raises:
            MissingAttrError: If the 'weight' attribute is missing in
            either object.
        """
        if not hasattr(self, 'weight') or not hasattr(other, 'weight'):
            raise MissingAttrError('Missing `weight` attribute')
        return self.weight > other.weight

    def __ne__(self, other) -> bool:
        """
        Compare a DownHill node and other node by their weight.

        Args:
            other: The other DownHill object to compare with.

        Returns:
            bool: True if the current object's weight is less than the other's,
                  False otherwise.

        Raises:
            MissingAttrError: If the 'weight' attribute is missing in
            either object.
        """
        if not hasattr(self, 'weight') or not hasattr(other, 'weight'):
            raise MissingAttrError('Missing `weight` attribute')
        return self.weight != other.weight
