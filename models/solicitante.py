from models.usuario import Usuario

class Solicitante(Usuario):
    def __init__(self, id_usuario, nome, email, senha):
        super().__init__(id_usuario, nome, email, senha)
        self.__pedidos_ativos = []
        self.__pedidos_historico = []

    @property
    def lista_pedido(self):
        return self.__pedidos_ativos.copy()

    @property
    def lista_historico(self):
        return self.__pedidos_historico.copy()

    # ==========================================
    # INTEGRAÇÃO COM BANCO DE DADOS
    # ==========================================
    def carregar_pedido_banco(self, pedido):
        """Preenche as listas silenciosamente ao buscar dados do SQLite."""
        if pedido.status in ["Finalizado", "Cancelado"]:
            self.__pedidos_historico.append(pedido)
        else:
            self.__pedidos_ativos.append(pedido)

    # ==========================================
    # MÉTODOS DE NEGÓCIO
    # ==========================================
    def novo_pedido(self, pedido):
        """Usado apenas quando o usuário ativamente cria um pedido no terminal."""
        if pedido in self.__pedidos_ativos:
            raise ValueError("Este pedido já foi registrado na sua lista.")
        self.__pedidos_ativos.append(pedido)
        print("Novo pedido registrado com sucesso!")

    def finalizar_pedido(self, id_pedido):
        for pedido in self.__pedidos_ativos:
            if pedido.id_pedido == id_pedido:        
                if pedido.status in ["Finalizado", "Cancelado"]:
                    self.__pedidos_ativos.remove(pedido)
                    self.__pedidos_historico.append(pedido)
                    print(f"Pedido #{id_pedido} movido para o histórico.")
                    return
                else: 
                    raise ValueError(f"O pedido não pode ser arquivado pois está {pedido.status}.")
        raise ValueError("Pedido não encontrado nos ativos.")

    # ==========================================
    # PAINEL DE INFORMAÇÕES
    # ==========================================
    def exibir_lista_pedidos(self):
        if len(self.lista_pedido) > 0:
            print("--- Seus pedidos ativos são: ---")
            for pedido in self.lista_pedido:
                print(f"• Pedido #{pedido.id_pedido} | Status: {pedido.status}")
        else:
            print("Lista de pedidos ativos vazia!")

    def exibir_opcoes(self):
        print("-" * 45)
        print("Opções:")
        print("1. Criar um novo pedido no mercado")
        print("2. Finalizar/Arquivar um pedido da lista")
        print("0. Desconectar")
        print("=" * 45)

    def exibir_painel(self):
        print(f"\n--- PAINEL DO SOLICITANTE: {self.get_nome()} ---")
        self.exibir_cabecalho()       
        self.exibir_lista_pedidos()   
        self.exibir_opcoes()