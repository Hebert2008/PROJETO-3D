import os
from models.solicitante import Solicitante
from models.impressor import Impressor
from models.pedido import Pedido
# Garanta que esta linha aponta para banco_dados.py e NÃO conexao.py
from database.banco_dados import BancoDeDados 

def main():
    # O uso do caminho absoluto que mandei no exemplo anterior é crucial aqui
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_banco = os.path.join(diretorio_atual, "mercado_3d.db")
    
    db = BancoDeDados(caminho_banco)

def carregar_sessao_solicitante(db, id_usuario, nome, email, senha):
    """Busca o usuário no banco, cria o objeto e hidrata suas listas de pedidos."""
    cliente = Solicitante(id_usuario, nome, email, senha)
    
    # Busca os pedidos que pertencem a este solicitante direto do banco
    db._BancoDeDados__cursor.execute("SELECT id, descricao, quantidade, valor, status FROM pedidos WHERE id_solicitante = ?", (id_usuario,))
    para_carregar = db._BancoDeDados__cursor.fetchall()
    
    for linha in para_carregar:
        pedido = Pedido(id_pedido=linha[0], descricao=linha[1], quantidade=linha[2], valor=linha[3], status=linha[4])
        cliente.carregar_pedido_banco(pedido)
        
    return cliente
        
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
        opcao = input("\nEscolha uma opção (0 a 3): ").strip()

        if opcao == "1":
            print("\n--- NOVO PEDIDO (Deixe em branco e aperte Enter para voltar) ---")
            
            descricao = input("O que deseja imprimir? ").strip()
            if not descricao:
                print("Operação cancelada. Retornando ao painel...")
                continue

            qtd_input = input("Quantidade de peças: ").strip()
            if not qtd_input:
                print("Operação cancelada. Retornando ao painel...")
                continue
            try:
                qtd = int(qtd_input)
            except ValueError:
                print("[!] Erro: A quantidade deve ser um número inteiro.")
                continue

            valor_input = input("Valor sugerido (R$): ").strip()
            if not valor_input:
                print("Operação cancelada. Retornando ao painel...")
                continue
            try:
                valor = float(valor_input)
            except ValueError:
                print("[!] Erro: O valor deve ser um número válido.")
                continue
            
            try:
                id_gerado = db.inserir_pedido(descricao, qtd, valor, usuario.get_id())
                novo_pedido = Pedido(id_gerado, descricao, qtd, valor)
                usuario.novo_pedido(novo_pedido)
            except ValueError as erro:
                print(f"[!] Erro ao criar pedido: {erro}")

        elif opcao == "2":
            id_arq_input = input("\nInforme o ID do pedido para arquivar (ou Enter para voltar): ").strip()
            if not id_arq_input:
                print("Operação cancelada. Retornando ao painel...")
                continue
            try:
                id_arq = int(id_arq_input)
                usuario.finalizar_pedido(id_arq)
                db.atualizar_status_pedido(id_arq, None, "Arquivado")
            except ValueError as erro:
                print(f"[!] Erro: {erro}")

        elif opcao == "3":
            # 1. Verifica se existe pelo menos um pedido "Aberto" antes de prosseguir
            tem_aberto = any(pedido.get_status() == "Aberto" for pedido in usuario.lista_pedido)
            
            if not tem_aberto:
                print("\n[!] Você não possui nenhum pedido 'Aberto' que possa ser cancelado no momento.")
                # Segura o loop até o cliente confirmar que leu
                input("Pressione Enter para voltar ao painel principal...") 
                continue

            # 2. Se tiver, segue o fluxo normal
            id_canc_input = input("\nInforme o ID do pedido para cancelar (ou Enter para voltar): ").strip()
            if not id_canc_input:
                print("Operação cancelada. Retornando ao painel...")
                continue
            try:
                id_canc = int(id_canc_input)
                usuario.cancelar_pedido(id_canc)
                db.atualizar_status_pedido(id_canc, None, "Cancelado")
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
        opcao = input("\nEscolha uma opção (0 a 2): ").strip()

        if opcao == "1":
            print("\n--- MERCADO DE PEDIDOS ABERTOS (Deixe em branco e aperte Enter para voltar) ---")
            pedidos_abertos = db.buscar_pedidos_abertos()
            
            if not pedidos_abertos:
                print("Não há pedidos abertos no mercado no momento.")
            else:
                for linha in pedidos_abertos:
                    print(f"• Pedido #{linha[0]} | Peça: {linha[1]} | Qtd: {linha[2]} | R$ {linha[3]:.2f}")
                
                id_assumir_input = input("\nDigite o ID do pedido que deseja assumir (ou Enter para voltar): ").strip()
                if not id_assumir_input:
                    print("Operação cancelada. Retornando ao painel...")
                    continue
                
                try:
                    id_assumir = int(id_assumir_input)
                    # Encontra os dados daquele ID na lista buscada do banco
                    dados_pedido = next((p for p in pedidos_abertos if p[0] == id_assumir), None)
                    
                    if dados_pedido:
                        # 1. Atualiza no banco
                        db.atualizar_status_pedido(id_assumir, usuario.get_id(), "Em Produção")
                        # 2. Cria o objeto e vincula localmente
                        pedido_assumido = Pedido(dados_pedido[0], dados_pedido[1], dados_pedido[2], dados_pedido[3], "Em Produção")
                        usuario.assumir_pedido(pedido_assumido)
                    else:
                        print("[!] Erro: ID de pedido não encontrado ou inválido.")
                except ValueError as erro:
                    print(f"[!] Erro: {erro}")

        elif opcao == "2":
            id_conc_input = input("\nInforme o ID do trabalho para concluir (ou Enter para voltar): ").strip()
            if not id_conc_input:
                print("Operação cancelada. Retornando ao painel...")
                continue
            try:
                id_conc = int(id_conc_input)
                # 1. Conclui localmente
                usuario.concluir_pedido(id_conc)
                # 2. Atualiza no banco para o solicitante poder ver
                db.atualizar_status_pedido(id_conc, usuario.get_id(), "Finalizado")
            except ValueError as erro:
                print(f"[!] Erro: {erro}")

        elif opcao == "0":
            print("Desconectando o painel de produção...")
            break
        
        else:
            print("Opção inválida.")

    
def main():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_banco = os.path.join(diretorio_atual, "mercado_3d.db")
    db = BancoDeDados(caminho_banco)

    while True:
        print("\n" + "="*45)
        print("    BEM-VINDO AO SISTEMA DE IMPRESSÃO 3D")
        print("="*45)
        print("1. Fazer Login")
        print("2. Criar nova conta")
        print("0. Desligar Sistema")
        
        escolha = input("\nEscolha uma opção: ").strip()

        if escolha == "1":
            email = input("E-mail: ").strip()
            if not email: continue
            
            senha = input("Senha: ").strip()
            if not senha: continue

            # Consulta o banco de dados
            usuario_dados = db.autenticar_usuario(email, senha)

            if usuario_dados:
                id_user, nome, tipo = usuario_dados
                print(f"\nAutenticação bem-sucedida! Entrando como {nome}...")
                
                # Instancia a classe correta baseada no banco de dados
                if tipo == "solicitante":
                    usuario_logado = carregar_sessao_solicitante(db, id_user, nome, email, senha)
                    fluxo_solicitante(usuario_logado, db)
                
                elif tipo == "impressor":
                    # Aqui você pode criar um carregar_sessao_impressor depois se quiser puxar o histórico
                    usuario_logado = Impressor(id_user, nome, email, senha)
                    fluxo_impressor(usuario_logado, db)
            else:
                print("[!] E-mail ou senha incorretos. Tente novamente.")

        elif escolha == "2":
            print("\n--- CADASTRO DE NOVO USUÁRIO (Enter para cancelar) ---")
            nome = input("Nome completo: ").strip()
            if not nome: continue
            
            email = input("E-mail: ").strip()
            if not email: continue
            
            senha = input("Senha (mín. 6 caracteres): ").strip()
            if not senha: continue
            
            tipo = input("Você é (1) Solicitante ou (2) Impressor? ").strip()
            tipo_str = "solicitante" if tipo == "1" else "impressor" if tipo == "2" else None
            
            if not tipo_str:
                print("[!] Tipo inválido. Cadastro cancelado.")
                continue

            try:
                # 1. Instancia o objeto ANTES de salvar no banco para forçar a validação
                if tipo_str == "solicitante":
                    # Passamos None no ID porque o banco ainda vai gerar um
                    novo_user = Solicitante(None, nome, email, senha)
                else:
                    novo_user = Impressor(None, nome, email, senha)
                
                # 2. Se a classe aceitou os dados sem disparar o ValueError, salva no banco!
                db.inserir_usuario(nome, email, senha, tipo_str)
                print(">>> Conta criada com sucesso! Você já pode fazer login.")
                
            except ValueError as erro:
                # Captura o erro exato que os seus Setters dispararam
                print(f"[!] Erro no cadastro: {erro}")

        elif escolha == "0":
            print("Desligando o sistema... Até logo!")
            db.fechar_conexao()
            break
        
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()