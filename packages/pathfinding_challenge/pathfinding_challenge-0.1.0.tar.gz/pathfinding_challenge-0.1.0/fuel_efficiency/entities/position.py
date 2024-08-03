import sys
from dataclasses import dataclass
from typing import Optional


class PositionError(Exception):
    """Exception raised for errors in the Position operations."""

    def __init__(self, message: str):
        super().__init__(message)


@dataclass(slots=True)
class Position:
    x: int = sys.maxsize
    y: int = sys.maxsize

    def __add__(self, other: 'Position') -> Optional['Position']:
        """
        Add two Position objects together.

        Args:
            other (Position): The other Position object to add to this one.

        Returns:
            Position: The sum of the two Position objects.
        """
        try:
            if not isinstance(other, Position):
                raise NotImplementedError(
                    f'Cannot add Position and {type(other)}'
                )
            new_x = self.x + other.x
            new_y = self.y + other.y
            return Position(new_x, new_y)
        except (OverflowError, PositionError) as e:
            print(f'Error in __add__: {e}')
            return None

    def __sub__(self, other: 'Position') -> Optional['Position']:
        """
        Subtract two Position objects.

        Args:
            other (Position): The other Position object to subtract
                              from this one.

        Returns:
            Position: The difference of the two Position objects.
        """
        try:
            if not isinstance(other, Position):
                raise NotImplementedError(
                    f'Cannot subtract Position and {type(other)}'
                )
            new_x = self.x - other.x
            new_y = self.y - other.y
            return Position(new_x, new_y)
        except (OverflowError, PositionError) as e:
            print(f'Error in __sub__: {e}')
            return None
