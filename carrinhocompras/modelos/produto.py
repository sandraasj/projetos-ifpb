from dataclasses import dataclass

@dataclass
class Produto:
    id: int
    nome: str
    preco: float
    estoque: int

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)