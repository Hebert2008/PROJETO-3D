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
        
        # APENAS UM INPUT AQUI (Já atualizado para 0 a 3)
        opcao = input("\nEscolha uma opção (0 a 3): ")

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
                db.atualizar_status_pedido(id_arq, None, "Arquivado")
            except ValueError as erro:
                print(f"[!] Erro: {erro}")

        elif opcao == "3":
            id_canc = int(input("\nInforme o ID do pedido para cancelar: "))
            try:
                # 1. Tenta cancelar o objeto localmente
                usuario.cancelar_pedido(id_canc)
                # 2. Se não deu erro, atualiza no banco
                db.atualizar_status_pedido(id_canc, None, "Cancelado")
            except ValueError as erro:
                print(f"[!] Erro: {erro}")

        elif opcao == "0":
            print("Desconectando Solicitante...")
            break
        
        else:
            print("Opção inválida.")
    

def fluxo_solicitante(usuario, db):
    while True:
        usuario.exibir_painel()
        
        # APENAS UM INPUT AQUI (Já atualizado para 0 a 3)
        opcao = input("\nEscolha uma opção (0 a 3): ")

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
                db.atualizar_status_pedido(id_arq, None, "Arquivado")
            except ValueError as erro:
                print(f"[!] Erro: {erro}")

        elif opcao == "3":
            id_canc = int(input("\nInforme o ID do pedido para cancelar: "))
            try:
                # 1. Tenta cancelar o objeto localmente
                usuario.cancelar_pedido(id_canc)
                # 2. Se não deu erro, atualiza no banco
                db.atualizar_status_pedido(id_canc, None, "Cancelado")
            except ValueError as erro:
                print(f"[!] Erro: {erro}")

        elif opcao == "0":
            print("Desconectando Solicitante...")
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