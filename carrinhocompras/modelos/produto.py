from dataclasses import dataclass
from typing import Dict

@dataclass
class Produto:
    id: int
    nome: str
    preco: float
    estoque: int

    def to_dict(self) -> Dict:
        return self.__dict__

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**data)