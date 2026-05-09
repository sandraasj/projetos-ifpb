from repositorio.produto_repositorio import ProdutoRepositorio
from typing import List, Tuple

class Carrinho:
    def __init__(self, repositorio: ProdutoRepositorio):
        self.repositorio = repositorio
        self.itens: List[Tuple] = []  

    def adicionar_item(self, produto_id: int, quantidade: int = 1):
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero.")

        produto = self.repositorio.buscar_por_id(produto_id)
        if not produto:
            raise ValueError(f"Produto com ID {produto_id} não encontrado.")

        if produto.preco <= 0:
            raise ValueError(f"Preço do produto '{produto.nome}' deve ser maior que zero.")

        if produto.estoque < quantidade:
            raise ValueError(f"Estoque insuficiente! Disponível: {produto.estoque} unidades.")

        
        for i, (p, q) in enumerate(self.itens):
            if p.id == produto_id:
                nova_quantidade = q + quantidade
                if nova_quantidade > p.estoque:
                    raise ValueError("Estoque insuficiente para adicionar essa quantidade!")
                self.itens[i] = (p, nova_quantidade)
                print(f"✅ Quantidade atualizada: {nova_quantidade}x {p.nome}")
                return

        
        self.itens.append((produto, quantidade))
        print(f"✅ Produto adicionado: {quantidade}x {produto.nome}")

    def get_itens(self):
        return self.itens[:]

    def valor_total(self) -> float:
        return sum(produto.preco * qtd for produto, qtd in self.itens)

    def limpar(self):
        self.itens.clear()