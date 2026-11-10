class Pedido:
    def __init__(self, id_pedido, descricao, quantidade, valor, status="Aberto"):
        # O ID agora vem do banco de dados (AUTOINCREMENT) e continua protegido (sem setter)
        self.__id_pedido = id_pedido
        
        # Chama os setters do @property para garantir validação mesmo vindo do banco
        self.descricao = descricao
        self.quantidade = quantidade
        self.valor = valor
        self.status = status

    @property
    def id_pedido(self):
        return self.__id_pedido

    # ==========================================
    # GETTERS E SETTERS (Mantidos intactos)
    # ==========================================
    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao):
        if len(descricao.strip()) > 0:
            self.__descricao = descricao
        else:
            raise ValueError("A descrição/modelo não pode ser vazia.")

    @property
    def quantidade(self):
        return self.__quantidade

    @quantidade.setter
    def quantidade(self, quantidade):
        if quantidade > 0:
            self.__quantidade = quantidade
        else:
            raise ValueError("A quantidade deve ser maior que zero.")

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, valor):
        if valor > 0:
            self.__valor = valor
        else:
            raise ValueError("O valor deve ser maior que zero.")

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, novo_status):
        status_validos = ["Aberto", "Em Produção", "Finalizado", "Cancelado"]
        if novo_status in status_validos:
            self.__status = novo_status
        else:
            raise ValueError(f"Status inválido! Escolha entre: {status_validos}")

    def exibir_detalhes(self):
        print(f"• Pedido #{self.id_pedido} | Peça: {self.descricao} | "
              f"Qtd: {self.quantidade} | R$ {self.valor:.2f} | Status: {self.status}")