import random
import time
from modelos.venda import Venda

class ApiBanco:
    def processar_pagamento(self, venda: Venda):
        """Simula o processamento de pagamento no banco"""
        time.sleep(0.8)  # Simula delay de rede
        
        
        if random.random() < 0.07:
            return {
                "status": "RECUSADO", 
                "mensagem": "Pagamento recusado pelo banco"
            }
        
        return {
            "status": "APROVADO",
            "mensagem": "Pagamento aprovado com sucesso!",
            "transacao_id": f"TX{random.randint(100000, 999999)}",
            "forma": venda.forma_pagamento.value
        }