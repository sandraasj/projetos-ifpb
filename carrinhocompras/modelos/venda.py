from enum import Enum
from modelos.carrinho import Carrinho

class FormaPagamento(Enum):
    PIX = "PIX"
    DINHEIRO = "Dinheiro"
    CARTAO = "Cartão"


class Venda:
    def __init__(self, carrinho: Carrinho, forma_pagamento: FormaPagamento):
        self.carrinho = carrinho
        self.forma_pagamento = forma_pagamento
        self.desconto = 0.0
        self.juros = 0.0

        
        if forma_pagamento in [FormaPagamento.PIX, FormaPagamento.DINHEIRO]:
            self.desconto = 5.0
        else:  # CARTÃO
            self.juros = 5.0

        self.validar()

    def validar(self):
        if not self.carrinho.get_itens():
            raise ValueError("Carrinho está vazio!")

        if self.desconto > 0 and self.juros > 0:
            raise ValueError("Não é permitido aplicar desconto e juros ao mesmo tempo.")

        for produto, qtd in self.carrinho.get_itens():
            if produto.preco <= 0 or qtd <= 0:
                raise ValueError("Preço ou quantidade inválidos.")

    def valor_final(self) -> float:
        bruto = self.carrinho.valor_total()
        return round(bruto * (1 - self.desconto / 100) * (1 + self.juros / 100), 2)

    def finalizar(self, api_banco):
        """Processa pagamento e atualiza estoque (FUNÇÃO CORRIGIDA)"""
        resultado = api_banco.processar_pagamento(self)

        if resultado["status"] == "APROVADO":
            print(f"\n✅ Pagamento APROVADO via {self.forma_pagamento.value}")
            print(f"   Desconto: {self.desconto}% | Juros: {self.juros}%")
            
            print("\n🔄 Atualizando estoque...")
            for produto, quantidade in self.carrinho.get_itens():
                sucesso = self.carrinho.repositorio.atualizar_estoque(produto.id, quantidade)
                if sucesso:
                    print(f"   ✅ {produto.nome} → -{quantidade} unidade(s)")
                else:
                    print(f"   ⚠️ Falha ao atualizar estoque de {produto.nome}")
            
            print("✅ Estoque atualizado com sucesso!")
        else:
            print(f"\n❌ Pagamento RECUSADO. Estoque não foi alterado.")
        
        return resultado