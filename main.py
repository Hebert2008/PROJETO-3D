from models.solicitante import Solicitante
from models.impressor import Impressor
from models.pedido import Pedido

# Banco de dados em memória para conectar Solicitantes e Impressores
mercado_pedidos = []

def fluxo_solicitante(usuario):
    while True:
        usuario.exibir_painel()
        opcao = input("\nEscolha uma opção (1 a 3): ")

        if opcao == "1":
            print("\n--- NOVO PEDIDO ---")
            descricao = input("O que deseja imprimir? ")
            link = input("Link do modelo 3D (.stl): ")
            qtd = int(input("Quantidade de peças: "))
            valor = float(input("Valor sugerido (R$): "))
            
            try:
                novo_pedido = Pedido(descricao, qtd, valor, link)
                mercado_pedidos.append(novo_pedido)
                usuario.novo_pedido(novo_pedido)

            except ValueError as erro:
                print(f"[!] Erro ao criar pedido: {erro}")

        elif opcao == "2":
            id_arq = int(input("\nInforme o ID do pedido para arquivar: "))
            try:
                usuario.finalizar_pedido(id_arq)
            except ValueError as erro:
                print(f"[!] Erro: {erro}")

        elif opcao == "3":
            print("Desconectando Solicitante...")
            break
        else:
            print("Opção inválida.")

def fluxo_impressor(usuario):
    while True:
        usuario.exibir_painel()
        opcao = input("\nEscolha uma opção (0 a 2): ")

        if opcao == "1":
            print("\n--- MERCADO DE PEDIDOS ABERTOS ---")
            pedidos_abertos = [p for p in mercado_pedidos if p.status == "Aberto"]
            
            if not pedidos_abertos:
                print("Não há pedidos abertos no mercado no momento.")
            else:
                for p in pedidos_abertos:
                    p.exibir_detalhes()
                
                id_assumir = int(input("\nDigite o ID do pedido que deseja assumir: "))
                
                # Busca o pedido no mercado e vincula ao impressor
                for p in pedidos_abertos:
                    if p.id_pedido == id_assumir:
                        p.status = "Em Produção"
                        try:
                            usuario.assumir_pedido(p)
                        except ValueError as erro:
                            print(f"[!] Erro: {erro}")
                        break

        elif opcao == "2":
            id_conc = int(input("\nInforme o ID do trabalho para concluir: "))
            try:
                usuario.concluir_pedido(id_conc)
                # Atualiza o status global para que o Solicitante possa arquivar depois
                for p in mercado_pedidos:
                    if p.id_pedido == id_conc:
                        p.status = "Finalizado"
            except ValueError as erro:
                print(f"[!] Erro: {erro}")

        elif opcao == "3":
            print("Desconectando Impressor...")
            break
        else:
            print("Opção inválida.")

def main():
    # Instanciando usuários de teste para você não precisar criar do zero a cada execução
    cliente = Solicitante(1, "Ana Maker", "ana@email.com", "senha123")
    impressor = Impressor(2, "Carlos 3D", "carlos@email.com", "senha123")

    while True:
        print("\n" + "=" * 45)
        print("    BEM-VINDO AO SISTEMA DE IMPRESSÃO 3D")
        print("=" * 45)
        print("1. Entrar como Solicitante (Ana)")
        print("2. Entrar como Impressor (Carlos)")
        print("3. Desligar Sistema")
        
        escolha = input("\nComo deseja logar? ")

        if escolha == "1":
            fluxo_solicitante(cliente)
        elif escolha == "2":
            fluxo_impressor(impressor)
        elif escolha == "3":
            print("Sistema encerrado.")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()