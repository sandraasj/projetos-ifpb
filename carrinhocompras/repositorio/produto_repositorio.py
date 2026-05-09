import json
from modelos.produto import Produto
from typing import Optional, List

class ProdutoRepositorio:
    def __init__(self, arquivo: str = "produtos.json"):
        self.arquivo = arquivo

    def listar_todos(self) -> List[Produto]:
        with open(self.arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        return [Produto.from_dict(p) for p in dados]

    def buscar_por_id(self, produto_id: int) -> Optional[Produto]:
        for p in self.listar_todos():
            if p.id == produto_id:
                return p
        return None

    def atualizar_estoque(self, produto_id: int, quantidade: int) -> bool:
        produtos = self.listar_todos()
        for p in produtos:
            if p.id == produto_id:
                if p.estoque < quantidade:
                    return False
                p.estoque -= quantidade
                self._salvar(produtos)
                return True
        return False

    def _salvar(self, produtos: List[Produto]):
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            json.dump([p.to_dict() for p in produtos], f, indent=2, ensure_ascii=False)