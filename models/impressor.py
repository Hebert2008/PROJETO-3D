from models.usuario import Usuario

class Impressor(Usuario):
    def __init__(self, id_usuario, nome, email, senha):
        super().__init__(id_usuario, nome, email, senha)
        
        # Atributos focados na jornada do negócio
        self.__pedidos_assumidos = []
        self.__pedidos_concluidos = []

    @property
    def lista_pedido(self):
        return self.__pedidos_assumidos.copy()
    @property
    def lista_concluido(self):
        return self.__pedidos_concluidos.copy()
   
    def assumir_pedido(self, novo_pedido):
        for pedido_na_fila in self.__pedidos_assumidos:
            if pedido_na_fila.get_id_pedido() == novo_pedido.get_id_pedido():
                raise ValueError("Esse pedido já está na lista de produção.")

        self.__pedidos_assumidos.append(novo_pedido)
        print("O pedido foi adicionado à fila de produção de {}.".format(self.get_nome()))

    def concluir_pedido(self, id_pedido):
        for pedido in self.__pedidos_assumidos:
            if pedido.get_id_pedido() == id_pedido:
                self.__pedidos_assumidos.remove(pedido)
                self.__pedidos_concluidos.append(pedido)

                print(f"Trabalho {id_pedido} concluído e removido da sua fila.")
                return
                
        raise ValueError("Pedido não encontrado na sua lista de assumidos.")


# PAINEL DE INFORMAÇÕES 

    def exibir_fila_producao(self):
        if len(self.lista_pedido) > 0:
            print("--- Os pedidos em produção são: ---")
            for pedido in self.lista_pedido: 
                print(f"• Pedido #{pedido.get_id_pedido()} | Status: {pedido.get_status()}")

        else: 
            print("Fila de produção vazia!")

    def exibir_opcoes(self):
        print("-" * 45)
        print("Opções:")
        print("1. Buscar novos pedidos no mercado")
        print("2. Concluir um trabalho da fila")
        print("0. Desconectar")
        print("=" * 45)



    def exibir_painel(self):
        print(f"\n--- PAINEL DO IMPRESSOR: {self.get_nome()} ---")
        self.exibir_cabecalho()       
        self.exibir_fila_producao()   
        self.exibir_opcoes()

        