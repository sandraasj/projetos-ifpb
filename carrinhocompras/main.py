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
                prod_id = int(input("ID do produto: ").strip())
                qtd = int(input("Quantidade: ").strip() or "1")
                carrinho.adicionar_item(prod_id, qtd)
                print("✅ Produto adicionado com sucesso!\n")
            except Exception as e:
                print(f"❌ Erro: {e}\n")

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
            print("1. PIX     → 5% desconto")
            print("2. Dinheiro → 5% desconto")
            print("3. Cartão   → 5% juros")
            
            try:
                f = int(input("Escolha: "))
                forma = [FormaPagamento.PIX, FormaPagamento.DINHEIRO, FormaPagamento.CARTAO][f-1]

                
                venda = Venda(carrinho, forma)

                print(f"\nValor Final: R$ {venda.valor_final():,.2f}")
                print(f"   → {forma.value} | Desconto: {venda.desconto}% | Juros: {venda.juros}%")

                if input("\nConfirmar pagamento? (s/n): ").lower() == 's':
                    resultado = pagamento_servico.processar_pagamento(venda)
                    if resultado["status"] == "APROVADO":
                        carrinho.limpar()
                        print("🎉 Compra finalizada com sucesso!\n")
            except Exception as e:
                print(f"❌ Erro: {e}\n")

        elif op == "0":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida!\n")


if __name__ == "__main__":
    main()