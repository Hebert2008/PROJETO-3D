from models.usuario import Usuario

class Solicitante(Usuario):
    def __init__(self, id, nome, email, senha):
        super().__init__(id, nome, email, senha)

        self.__pedidos_ativos = []
        self.__pedidos_historico = []


    #PROCESSANDO PEDIDOS:
    @property
    def lista_pedido(self):
        return self.__pedidos_ativos.copy()

    @property
    def lista_historico(self):
        return self.__pedidos_historico.copy()
    
    def novo_pedido(self, pedido):
        if pedido in self.__pedidos_ativos:
            raise ValueError("Este pedido já foi registrado na sua lista.")
        self.__pedidos_ativos.append(pedido)

    def finalizar_pedido(self, id_pedido):
        for pedido in self.__pedidos_ativos:
            if pedido.get_id_pedido() == id_pedido:        
                status = pedido.get_status()

                if status in ["Finalizado", "Cancelado"]:
                    self.__pedidos_ativos.remove(pedido)
                    self.__pedidos_historico.append(pedido)
                    print("Seu pedido foi finalizado/cancelado")
                    return

                else: 
                    raise ValueError ("O pedido não pôde ser finalizado pois ainda está {}".format(status))

        raise ValueError ("Não há pedidos correspondentes a solicitação de finalização")

    #PAINEL USUARIO

    def exibir_lista_pedidos(self):
        if len(self.lista_pedido) > 0:
            print("--- Seus pedidos ativos são: ---")
            for pedido in self.lista_pedido:
                print(f"• Pedido #{pedido.get_id_pedido()} | Status: {pedido.get_status()}")
        else:
            print("Lista de pedidos ativos vazia!")

    def exibir_opcoes(self):
        print("-" * 45)
        print("Opções:")
        print("1. Criar um novo pedido no mercado")
        print("2. Finalizar/Arquivar um pedido da lista")
        print("3. Desconectar")
        print("=" * 45)

    def exibir_painel(self):
        print(f"\n--- PAINEL DO SOLICITANTE: {self.get_nome()} ---")
        self.exibir_user_info()       # Herdado de Usuario (exibe ID, Nome e Email)
        self.exibir_lista_pedidos()   # Exibe os pedidos ativos do Solicitante
        self.exibir_opcoes()          # Exibe as opções de menu do Solicitante


