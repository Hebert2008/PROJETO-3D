from models.usuario import Usuario

class Impressor(Usuario):
    def __init__(self, id_usuario, nome, email, senha):
        super().__init__(id_usuario, nome, email, senha)
        
        # Atributos focados na jornada do negócio
        self.__pedidos_assumidos = []
        self.__reputacao = 5.0

 
    def get_pedidos_assumidos(self):
        return self.__pedidos_assumidos

    def get_reputacao(self):
        return self.__reputacao

   
    def assumir_pedido(self, pedido):
        """
        Adiciona o pedido à fila pessoal de produção do impressor.
        """
        self.__pedidos_assumidos.append(pedido)
        print(f"O pedido foi adicionado à fila de produção de {self.get_nome()}.")

    def concluir_trabalho(self, id_pedido):
        """
        Libera o painel do impressor removendo o trabalho finalizado.
        """
        for pedido in self.__pedidos_assumidos:
            if pedido.get_id_pedido() == id_pedido:
                self.__pedidos_assumidos.remove(pedido)
                print(f"Trabalho {id_pedido} concluído e removido da sua fila.")
                return
                
        raise ValueError("Pedido não encontrado na sua lista de assumidos.")

    # ==========================================
    # POLIMORFISMO
    # ==========================================
    def exibir_painel(self):
        print(f"\n--- PAINEL DO IMPRESSOR: {self.get_nome()} ---")
        print(f"Reputação: {self.__reputacao} estrelas | Horas livres: {self.__horas_disponiveis}h")
        print(f"Trabalhos na fila atual: {len(self.__pedidos_assumidos)}")
        print("1. Buscar novos pedidos no mercado")
        print("2. Atualizar status de um pedido")
        print("3. Sair")