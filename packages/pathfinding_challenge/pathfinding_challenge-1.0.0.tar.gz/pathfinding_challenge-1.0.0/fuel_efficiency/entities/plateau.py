from dataclasses import dataclass, field

from fuel_efficiency import MissingAttrError
from fuel_efficiency.entities.node import Node
from fuel_efficiency.entities.position import Position


@dataclass(slots=True)
class Plateau(Node):
    weight: float = float(1)
    position: Position = field(default_factory=Position)

    def __hash__(self):
        """
        Return a hash value for the object.

        Returns:
            int: A hash based on the x and y coordinates of the position.
        """
        return hash((self.position.x, self.position.y))

    def __eq__(self, other):
        """
        Determine the equality between Plateau and other objects.

        Args:
            other: The other Plateau object to compare with.

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
        Compare a Plateau node and other node by their weight.

        Args:
            other: The other Plateau object to compare with.

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
        Compare a Plateau node and other node by their weight.

        Args:
            other: The other Plateau object to compare with.

        Returns:
            bool: True if the current object's weight is greater than
                the other's, False otherwise.

        Raises:
            MissingAttrError: If the 'weight' attribute is missing in
            either object.
        """
        if not hasattr(self, 'weight') or not hasattr(other, 'weight'):
            raise MissingAttrError('Missing `weight` attribute')
        return self.weight > other.weight

    def __ne__(self, other) -> bool:
        """
        Compare a Plateau node and other node by their weight.

        Args:
            other: The other Plateau object to compare with.

        Returns:
            bool: True if the current object's weight is not equal
                to the other's, False otherwise.

        Raises:
            MissingAttrError: If the 'weight' attribute is missing in
            either object.
        """
        if not hasattr(self, 'weight') or not hasattr(other, 'weight'):
            raise MissingAttrError('Missing `weight` attribute')
        return self.weight != other.weight
