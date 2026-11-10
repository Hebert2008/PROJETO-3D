from models.solicitante import Solicitante
from models.impressor import Impressor
from models.pedido import Pedido
from database.banco_dados import BancoDeDados

def preparar_dados_teste(db):
    """Insere usuários de teste no banco caso ele esteja vazio."""
    try:
        db.inserir_usuario("Ana Maker", "ana@email.com", "senha123", "solicitante")
        db.inserir_usuario("Carlos 3D", "carlos@email.com", "senha123", "impressor")
    except ValueError:
        pass # Usuários já existem no banco

def carregar_sessao_solicitante(db, id_usuario):
    """Busca o usuário no banco, cria o objeto e hidrata suas listas de pedidos."""
    cliente = Solicitante(id_usuario, "Ana Maker", "ana@email.com", "senha123")
    
    # Busca os pedidos que pertencem a este solicitante direto do banco
    db._BancoDeDados__cursor.execute("SELECT id, descricao, quantidade, valor, status FROM pedidos WHERE id_solicitante = ?", (id_usuario,))
    para_carregar = db._BancoDeDados__cursor.fetchall()
    
    for linha in para_carregar:
        pedido = Pedido(id_pedido=linha[0], descricao=linha[1], quantidade=linha[2], valor=linha[3], status=linha[4])
        cliente.carregar_pedido_banco(pedido)
        
    return cliente

def carregar_sessao_impressor(db, id_usuario):
    """Busca o usuário no banco, cria o objeto e hidrata suas listas de pedidos."""
    impressor = Impressor(id_usuario, "Carlos 3D", "carlos@email.com", "senha123")
    
    db._BancoDeDados__cursor.execute("SELECT id, descricao, quantidade, valor, status FROM pedidos WHERE id_impressor = ?", (id_usuario,))
    para_carregar = db._BancoDeDados__cursor.fetchall()
    
    for linha in para_carregar:
        pedido = Pedido(id_pedido=linha[0], descricao=linha[1], quantidade=linha[2], valor=linha[3], status=linha[4])
        impressor.carregar_pedido_banco(pedido)
        
    return impressor

def fluxo_solicitante(usuario, db):
    while True:
        usuario.exibir_painel()
        opcao = input("\nEscolha uma opção (0 a 2): ")

        if opcao == "1":
            print("\n--- NOVO PEDIDO ---")
            descricao = input("O que deseja imprimir? ")
            qtd = int(input("Quantidade de peças: "))
            valor = float(input("Valor sugerido (R$): "))
            
            try:
                # 1. Salva no banco de dados primeiro
                id_gerado = db.inserir_pedido(descricao, qtd, valor, usuario.get_id())
                # 2. Cria o objeto Pedido com o ID real do banco
                novo_pedido = Pedido(id_gerado, descricao, qtd, valor)
                # 3. Adiciona à lista local da classe
                usuario.novo_pedido(novo_pedido)
            except ValueError as erro:
                print(f"[!] Erro ao criar pedido: {erro}")

        elif opcao == "2":
            id_arq = int(input("\nInforme o ID do pedido para arquivar (Finalizado/Cancelado): "))
            try:
                usuario.finalizar_pedido(id_arq)
                # Atualiza no banco (opicional dependendo da sua regra de histórico)
                db.atualizar_status_pedido(id_arq, None, "Arquivado")
            except ValueError as erro:
                print(f"[!] Erro: {erro}")

        elif opcao == "0":
            print("Desconectando Solicitante...")
            break
        else:
            print("Opção inválida.")

def fluxo_impressor(usuario, db):
    while True:
        usuario.exibir_painel()
        opcao = input("\nEscolha uma opção (0 a 2): ")

        if opcao == "1":
            print("\n--- MERCADO DE PEDIDOS ABERTOS ---")
            pedidos_abertos = db.buscar_pedidos_abertos()
            
            if not pedidos_abertos:
                print("Não há pedidos abertos no mercado no momento.")
            else:
                for linha in pedidos_abertos:
                    print(f"• Pedido #{linha[0]} | Peça: {linha[1]} | Qtd: {linha[2]} | R$ {linha[3]:.2f}")
                
                id_assumir = int(input("\nDigite o ID do pedido que deseja assumir: "))
                
                # Encontra os dados daquele ID na lista buscada do banco
                dados_pedido = next((p for p in pedidos_abertos if p[0] == id_assumir), None)
                
                if dados_pedido:
                    # 1. Atualiza no banco
                    db.atualizar_status_pedido(id_assumir, usuario.get_id(), "Em Produção")
                    # 2. Cria o objeto e vincula localmente
                    pedido_assumido = Pedido(dados_pedido[0], dados_pedido[1], dados_pedido[2], dados_pedido[3], "Em Produção")
                    try:
                        usuario.assumir_pedido(pedido_assumido)
                    except ValueError as erro:
                        print(f"[!] Erro: {erro}")
                else:
                    print("ID inválido ou pedido não está mais aberto.")

        elif opcao == "2":
            id_conc = int(input("\nInforme o ID do trabalho para concluir: "))
            try:
                # 1. Conclui localmente
                usuario.concluir_pedido(id_conc)
                # 2. Atualiza no banco para o solicitante poder ver
                db.atualizar_status_pedido(id_conc, usuario.get_id(), "Finalizado")
            except ValueError as erro:
                print(f"[!] Erro: {erro}")

        elif opcao == "0":
            print("Desconectando Impressor...")
            break
        else:
            print("Opção inválida.")

def main():
    # Inicializa a conexão com o banco e garante as tabelas
    db = BancoDeDados("mercado_3d.db")
    preparar_dados_teste(db)

    while True:
        print("\n" + "=" * 45)
        print("    BEM-VINDO AO SISTEMA DE IMPRESSÃO 3D")
        print("=" * 45)
        print("1. Entrar como Solicitante (Ana)")
        print("2. Entrar como Impressor (Carlos)")
        print("0. Desligar Sistema")
        
        escolha = input("\nComo deseja logar? ")

        if escolha == "1":
            # O ID 1 corresponde à Ana no nosso dado de teste
            cliente = carregar_sessao_solicitante(db, id_usuario=1)
            fluxo_solicitante(cliente, db)
        
        elif escolha == "2":
            # O ID 2 corresponde ao Carlos no nosso dado de teste
            impressor = carregar_sessao_impressor(db, id_usuario=2)
            fluxo_impressor(impressor, db)
        
        elif escolha == "0":
            print("Encerrando conexões...")
            db.fechar_conexao()
            print("Sistema encerrado.")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()