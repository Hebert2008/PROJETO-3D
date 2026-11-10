from models.usuario import Usuario

class Impressor(Usuario):
    def __init__(self, id_usuario, nome, email, senha):
        super().__init__(id_usuario, nome, email, senha)
        self.__pedidos_assumidos = []
        self.__pedidos_concluidos = []

    @property
    def lista_pedido(self):
        return self.__pedidos_assumidos.copy()

    @property
    def lista_concluido(self):
        return self.__pedidos_concluidos.copy()

    # ==========================================
    # INTEGRAÇÃO COM BANCO DE DADOS
    # ==========================================
    def carregar_pedido_banco(self, pedido):
        """Preenche as listas silenciosamente ao buscar dados do SQLite."""
        if pedido.status == "Em Produção":
            self.__pedidos_assumidos.append(pedido)
        elif pedido.status == "Finalizado":
            self.__pedidos_concluidos.append(pedido)
   
    # ==========================================
    # MÉTODOS DE NEGÓCIO
    # ==========================================
    def assumir_pedido(self, novo_pedido):
        """Usado apenas quando o usuário ativamente puxa um pedido no terminal."""
        for pedido_na_fila in self.__pedidos_assumidos:
            if pedido_na_fila.id_pedido == novo_pedido.id_pedido:
                raise ValueError("Esse pedido já está na lista de produção.")

        self.__pedidos_assumidos.append(novo_pedido)
        print(f"Pedido #{novo_pedido.id_pedido} adicionado à fila de {self.get_nome()}.")

    def concluir_pedido(self, id_pedido):
        for pedido in self.__pedidos_assumidos:
            if pedido.id_pedido == id_pedido:
                self.__pedidos_assumidos.remove(pedido)
                self.__pedidos_concluidos.append(pedido)
                print(f"Trabalho {id_pedido} concluído e removido da sua fila.")
                return
        raise ValueError("Pedido não encontrado na sua lista de assumidos.")

    # ==========================================
    # PAINEL DE INFORMAÇÕES 
    # ==========================================
    def exibir_fila_producao(self):
        if len(self.lista_pedido) > 0:
            print("--- Fila de Produção: ---")
            for pedido in self.lista_pedido: 
                print(f"• Pedido #{pedido.id_pedido} | Status: {pedido.status}")
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