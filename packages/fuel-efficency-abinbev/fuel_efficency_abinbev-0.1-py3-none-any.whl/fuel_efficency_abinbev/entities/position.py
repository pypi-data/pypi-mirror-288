import sys
from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class Position:
    """
    Represents a coordinate position in a Cartesian space with optional x and y values.
    If no values are provided, it uses the maximum size of an integer for x and y.

    Attributes:
        x (int): The x-coordinate.
        y (int): The y-coordinate.
    """
    x: int = sys.maxsize
    y: int = sys.maxsize

    def __eq__(self, other:'Position'):
        if isinstance(other,Position):
            return other.x == self.x and other.y == self.y
        else:
            raise NotImplementedError(f"Cannot compare equality between Position and {type(other)}")

    def getHashables(self):
        return (self.x, self.y)

    def __hash__(self):
        return hash(self.getHashables())

    def __add__(self, other:'Position') -> Optional['Position']:
        """
        Add two Position objects together.

        Args:
            other (Position): The other Position object to add to this one.

        Returns:
            Position: The sum of the two Position objects.
        """
        if isinstance(other,Position):
            return Position(self.x+other.x,self.y+other.y)
        else:
            raise NotImplementedError(f"Cannot add Position and {type(other)}")

    def __sub__(self, other:'Position') -> Optional['Position']:
        """
        Subtract two Position objects.

        Args:
            other (Position): The other Position object to subtract from this one.

        Returns:
            Position: The difference of the two Position objects.
        """
        if isinstance(other,Position):
            return Position(self.x-other.x,self.y-other.y)
        else:
            raise NotImplementedError(f"Cannot subtract Position and {type(other)}")
