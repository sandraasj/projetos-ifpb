from modelos.venda import Venda
from api.api_banco import ApiBanco

class PagamentoServico:

    
    def __init__(self):
        self.api_banco = ApiBanco()

    def processar_pagamento(self, venda: Venda) -> dict:
       
        print(f"Processando pagamento via {venda.forma_pagamento.value}...")
        resultado = self.api_banco.processar_pagamento(venda)
        
        if resultado["status"] == "APROVADO":
            print("✅ Pagamento aprovado!")
        else:
            print("❌ Pagamento recusado!")
            
        return resultado