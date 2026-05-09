from unittest.mock import MagicMock
from modelos.carrinho import Carrinho
from modelos.venda import Venda, FormaPagamento
from repositorio.produto_repositorio import ProdutoRepositorio

def test_venda_com_mock():
    """Teste Unitário com Mock"""
    repo = ProdutoRepositorio()
    carrinho = Carrinho(repo)
    carrinho.adicionar_item(1, 1)   # Notebook

    api_mock = MagicMock()
    api_mock.processar_pagamento.return_value = {
        "status": "APROVADO",
        "mensagem": "Sucesso",
        "transacao_id": "TX999999"
    }

    venda = Venda(carrinho, FormaPagamento.PIX, desconto=5.0)
    resultado = venda.finalizar(api_mock)

    assert resultado["status"] == "APROVADO"
    assert venda.valor_final() > 0
    print("✅ Teste Unitário com Mock passou!")


def test_integracao_atualizacao_estoque():
    """Teste de Integração: Venda → Atualização de Estoque"""
    repo = ProdutoRepositorio()
    estoque_inicial = repo.buscar_por_id(2).estoque   # Mouse

    carrinho = Carrinho(repo)
    carrinho.adicionar_item(2, 2)

    api_mock = MagicMock()
    api_mock.processar_pagamento.return_value = {"status": "APROVADO", "transacao_id": "TX123"}

    venda = Venda(carrinho, FormaPagamento.PIX)
    venda.finalizar(api_mock)

    estoque_final = repo.buscar_por_id(2).estoque
    assert estoque_final == estoque_inicial - 2
    print("✅ Teste de Integração (Estoque) passou!")


if __name__ == "__main__":
    test_venda_com_mock()
    test_integracao_atualizacao_estoque()
    print("\n Todos os testes executados com sucesso!")