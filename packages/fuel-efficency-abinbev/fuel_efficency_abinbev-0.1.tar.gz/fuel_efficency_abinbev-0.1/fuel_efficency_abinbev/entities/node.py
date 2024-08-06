from dataclasses import dataclass
from typing import Protocol, runtime_checkable, Any
from fuel_efficency_abinbev.entities.position import Position

@runtime_checkable
@dataclass
class Node(Protocol):
    """
    Protocol class for a node with weight and position, suitable for use in graph-based algorithms.
    """
    weight: float
    position: Position = Position()

    def __hash__(self) -> int:
        return hash((self.weight, self.position))

    def __eq__(self, other: Any) -> bool:
        """
        Check equality based on weight and position.
        """
        if not isinstance(other, Node):
            raise NotImplementedError("Missing `position` or `weight` attribute")
        return self.weight == other.weight and self.position == other.position

    def __lt__(self, other: Any) -> bool:
        """
        Less than comparison based on weight.
        """
        if not isinstance(other, Node):
            raise NotImplementedError("Missing `weight` attribute")
        return self.weight < other.weight

    def __gt__(self, other: Any) -> bool:
        """
        Greater than comparison based on weight.
        """
        if not isinstance(other, Node):
            raise NotImplementedError("Missing `weight` attribute")
        return self.weight > other.weight

    def __le__(self, other: Any) -> bool:
        """
        Less than or equal comparison based on weight.
        """
        if not isinstance(other, Node):
            raise NotImplementedError("Missing `weight` attribute")
        return self.weight <= other.weight

    def __ge__(self, other: Any) -> bool:
        """
        Greater than or equal comparison based on weight.
        """
        if not isinstance(other, Node):
            raise NotImplementedError("Missing `weight` attribute")
        return self.weight >= other.weight
