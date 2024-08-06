from dataclasses import dataclass

from fuel_efficency_abinbev.entities.node import Node
from fuel_efficency_abinbev.entities.position import Position


@dataclass(slots=True,eq=False)
class UpHill(Node):
    weight: float = float(2)
    position: 'Position' = Position()
