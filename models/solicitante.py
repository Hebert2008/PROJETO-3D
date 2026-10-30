from models.usuario import Usuario

class Solicitante(Usuario):
    #CONSTRUTOR:
    def __init__(self, id, nome, email, senha):
        super().__init__(id, nome, email, senha)

        self.__pedidos_ativos = []
        self.__pedidos_historico = []


    #PROCESSANDO PEDIDOS:
    def adicionar_pedido(self, pedido):
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

    #MÉTODO ABSTRATO:
    def exibir_painel(self):

        return f"Painel do Solicitante: {self.get_nome()}"