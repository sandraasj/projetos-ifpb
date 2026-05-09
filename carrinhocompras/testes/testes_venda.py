from unittest.mock import MagicMock
import shutil
import os
from repositorio.produto_repositorio import ProdutoRepositorio
from modelos.carrinho import Carrinho
from modelos.venda import Venda, FormaPagamento


def test_regras_desconto_juros():
    repo = ProdutoRepositorio()
    carrinho = Carrinho(repo)
    carrinho.adicionar_item(1, 1)

    # PIX → Desconto 5%
    venda_pix = Venda(carrinho, FormaPagamento.PIX)
    assert venda_pix.desconto == 5.0
    assert venda_pix.juros == 0.0

    # Cartão → Juros 5%
    venda_cartao = Venda(carrinho, FormaPagamento.CARTAO)
    assert venda_cartao.desconto == 0.0
    assert venda_cartao.juros == 5.0

    print("✅ Regras de Desconto e Juros automáticos OK!")


def test_valor_final_cartao_com_juros():
    repo = ProdutoRepositorio()
    carrinho = Carrinho(repo)
    carrinho.adicionar_item(1, 1)  # Notebook 4500

    venda = Venda(carrinho, FormaPagamento.CARTAO)
    valor_esperado = 4500 * 1.05
    assert abs(venda.valor_final() - valor_esperado) < 0.01
    print("✅ Cálculo com Juros no Cartão correto!")


def test_venda_com_mock():
    repo = ProdutoRepositorio()
    carrinho = Carrinho(repo)
    carrinho.adicionar_item(2, 1)

    api_mock = MagicMock()
    api_mock.processar_pagamento.return_value = {"status": "APROVADO", "transacao_id": "TX999"}

    venda = Venda(carrinho, FormaPagamento.PIX)
    resultado = venda.finalizar(api_mock)

    assert resultado["status"] == "APROVADO"
    print("✅ Teste Unitário com Mock OK!")


def test_integracao_estoque():
    backup = "produtos_backup.json"
    if os.path.exists("produtos.json"):
        shutil.copy("produtos.json", backup)

    try:
        repo = ProdutoRepositorio()
        estoque_inicial = repo.buscar_por_id(2).estoque

        carrinho = Carrinho(repo)
        carrinho.adicionar_item(2, 2)

        api_mock = MagicMock()
        api_mock.processar_pagamento.return_value = {"status": "APROVADO"}

        venda = Venda(carrinho, FormaPagamento.DINHEIRO)
        venda.finalizar(api_mock)

        estoque_final = repo.buscar_por_id(2).estoque
        assert estoque_final == estoque_inicial - 2
        print("✅ Teste de Integração (Estoque) OK!")
    finally:
        if os.path.exists(backup):
            shutil.copy(backup, "produtos.json")
            os.remove(backup)


if __name__ == "__main__":
    print("Executando Testes...\n")
    test_regras_desconto_juros()
    test_valor_final_cartao_com_juros()
    test_venda_com_mock()
    test_integracao_estoque()
    print("\n Todos os testes passaram com sucesso!")