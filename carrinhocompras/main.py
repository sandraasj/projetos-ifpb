from repositorio.produto_repositorio import ProdutoRepositorio
from modelos.carrinho import Carrinho
from modelos.venda import Venda, FormaPagamento
from servicos.pagamento_servico import PagamentoServico

def main():
    repositorio = ProdutoRepositorio()
    carrinho = Carrinho(repositorio)
    pagamento_servico = PagamentoServico()

    print("=== SISTEMA DE CARRINHO DE COMPRAS ===\n")

    while True:
        print("1. Adicionar produto ao carrinho")
        print("2. Ver carrinho")
        print("3. Finalizar compra")
        print("0. Sair")
        
        op = input("\nEscolha uma opção: ").strip()

        if op == "1":
            try:
                prod_id_str = input("ID do produto: ").strip()
                if not prod_id_str:
                    print("❌ Você deve informar o ID do produto!\n")
                    continue
                
                prod_id = int(prod_id_str)
                
                qtd_str = input("Quantidade: ").strip()
                qtd = int(qtd_str) if qtd_str else 1
                
                if qtd <= 0:
                    print("❌ Quantidade deve ser maior que zero!\n")
                    continue
                
                carrinho.adicionar_item(prod_id, qtd)
                print("✅ Produto adicionado com sucesso!\n")
                
            except ValueError:
                print("❌ Erro: ID ou Quantidade inválidos! Digite apenas números.\n")
            except Exception as e:
                print(f"❌ Erro inesperado: {e}\n")

        elif op == "2":
            itens = carrinho.get_itens()
            if not itens:
                print("Carrinho vazio!\n")
                continue
            print("\n--- SEU CARRINHO ---")
            for p, q in itens:
                print(f"{q}x {p.nome:<25} R$ {p.preco * q:,.2f}")
            print(f"Total: R$ {carrinho.valor_total():,.2f}\n")

        elif op == "3":
            if not carrinho.get_itens():
                print("Carrinho vazio!\n")
                continue
                
            print("\nFormas de pagamento:")
            print("1. PIX")
            print("2. Dinheiro")
            print("3. Cartão")
            
            try:
                f = int(input("Escolha: "))
                forma = [FormaPagamento.PIX, FormaPagamento.DINHEIRO, FormaPagamento.CARTAO][f-1]
                
                desconto_str = input("Desconto (%) [0]: ").strip()
                desconto = float(desconto_str) if desconto_str else 0.0
                
                venda = Venda(carrinho, forma, desconto=desconto)
                print(f"\nValor Final: R$ {venda.valor_final():,.2f}")
                
                if input("Confirmar pagamento? (s/n): ").lower() == 's':
                    resultado = pagamento_servico.processar_pagamento(venda)
                    
                    if resultado["status"] == "APROVADO":
                        print(f"Transação: {resultado.get('transacao_id')}")
                        carrinho.limpar()
                        print("✅ Compra finalizada com sucesso!\n")
            except Exception as e:
                print(f"❌ Erro: {e}\n")

        elif op == "0":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida!\n")


if __name__ == "__main__":
    main()