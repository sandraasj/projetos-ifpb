from unittest.mock import MagicMock
from modelos.carrinho import Carrinho
from modelos.venda import Venda, FormaPagamento
from repositorio.produto_repositorio import ProdutoRepositorio

def test_venda_com_mock():
    repo = ProdutoRepositorio()
    carrinho = Carrinho(repo)
    carrinho.adicionar_item(1, 1)   


    api_mock = MagicMock()
    api_mock.processar_pagamento.return_value = {
        "status": "APROVADO",
        "mensagem": "Sucesso",
        "transacao_id": "TX123456"
    }

    venda = Venda(carrinho, FormaPagamento.PIX, desconto=10.0)
    resultado = venda.finalizar(api_mock)

    assert resultado["status"] == "APROVADO"
    assert venda.valor_final() == 4050.0
    print("✅ Teste com Mock passou!")