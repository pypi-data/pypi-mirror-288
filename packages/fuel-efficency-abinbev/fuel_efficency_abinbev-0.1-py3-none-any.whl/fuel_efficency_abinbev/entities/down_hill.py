from dataclasses import dataclass

from fuel_efficency_abinbev.entities.node import Node
from fuel_efficency_abinbev.entities.position import Position


@dataclass(slots=True,eq=False)
class DownHill(Node):
    weight: float = float(0.5)
    position: 'Position' = Position()
