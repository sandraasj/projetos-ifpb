import json
from typing import Optional, List
from modelos.produto import Produto

class ProdutoRepositorio:
    def __init__(self, arquivo: str = "produtos.json"):
        self.arquivo = arquivo
        self._produtos: List[Produto] = self._carregar()

    def _carregar(self) -> List[Produto]:
        try:
            with open(self.arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                return [Produto.from_dict(p) for p in dados]
        except FileNotFoundError:
            print(f"⚠️ Arquivo {self.arquivo} não encontrado. Criando um novo...")
            return []
        except json.JSONDecodeError:
            print(f"❌ Erro ao ler o arquivo {self.arquivo}. JSON inválido.")
            return []

    def _salvar(self):
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            json.dump([p.to_dict() for p in self._produtos], f, indent=2, ensure_ascii=False)

    def listar_todos(self) -> List[Produto]:
        return self._produtos[:]

    def buscar_por_id(self, produto_id: int) -> Optional[Produto]:
        for p in self._produtos:
            if p.id == produto_id:
                return p
        return None

    def atualizar_estoque(self, produto_id: int, quantidade: int) -> bool:
        for p in self._produtos:
            if p.id == produto_id:
                if p.estoque >= quantidade:
                    p.estoque -= quantidade
                    self._salvar()
                    return True
                else:
                    print(f"⚠️ Estoque insuficiente para o produto ID {produto_id}")
                    return False
        return False