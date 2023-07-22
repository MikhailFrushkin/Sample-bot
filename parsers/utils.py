from dataclasses import dataclass


@dataclass
class SushiSet:
    name: str
    price: int
    weight: int
    quantity: int
    url: str
    coefficient: float
    image: str = None
