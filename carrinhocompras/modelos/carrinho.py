from repositorio.produto_repositorio import ProdutoRepositorio

class Carrinho:
    def __init__(self, repositorio: ProdutoRepositorio):
        self.repositorio = repositorio
        self.itens = []  # lista de tuplas (produto, quantidade)

    def adicionar_item(self, produto_id: int, quantidade: int = 1):
        produto = self.repositorio.buscar_por_id(produto_id)
        if not produto:
            raise ValueError(f"Produto ID {produto_id} não encontrado.")
        if produto.estoque < quantidade:
            raise ValueError(f"Estoque insuficiente! Disponível: {produto.estoque}")

        for i, (p, q) in enumerate(self.itens):
            if p.id == produto_id:
                self.itens[i] = (p, q + quantidade)
                return
        self.itens.append((produto, quantidade))

    def valor_total(self) -> float:
        return sum(produto.preco * qtd for produto, qtd in self.itens)

    def get_itens(self):
        return self.itens[:]

    def limpar(self):
        self.itens.clear()