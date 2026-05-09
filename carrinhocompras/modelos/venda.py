from enum import Enum
from modelos.carrinho import Carrinho

class FormaPagamento(Enum):
    PIX = "PIX"
    DINHEIRO = "Dinheiro"
    CARTAO = "Cartão"

class Venda:
    def __init__(self, carrinho: Carrinho, forma_pagamento: FormaPagamento, 
                 desconto: float = 0.0, juros: float = 0.0):
        self.carrinho = carrinho
        self.forma_pagamento = forma_pagamento
        self.desconto = desconto
        self.juros = juros
        self.validar()

    def validar(self):
        if not self.carrinho.get_itens():
            raise ValueError("Carrinho está vazio!")
        if self.desconto > 0 and self.juros > 0:
            raise ValueError("Não pode aplicar desconto e juros ao mesmo tempo.")

    def valor_final(self) -> float:
        bruto = self.carrinho.valor_total()
        return bruto * (1 - self.desconto/100) * (1 + self.juros/100)

    def finalizar(self, api_banco):
        """Finaliza a venda, processa pagamento e atualiza estoque"""
        resultado = api_banco.processar_pagamento(self)
        
        if resultado["status"] == "APROVADO":
            print("\n🔄 Atualizando estoque dos produtos vendidos...")
            
            for produto, quantidade in self.carrinho.get_itens():
                atualizado = self.carrinho.repositorio.atualizar_estoque(produto.id, quantidade)
                if atualizado:
                    print(f"   ✅ {produto.nome} → -{quantidade} unidade(s)")
                else:
                    print(f"   ⚠️ Falha ao atualizar estoque de {produto.nome}")
            
            print("✅ Estoque atualizado com sucesso!\n")
        else:
            print("❌ Pagamento recusado. Estoque não foi alterado.\n")
        
        return resultado