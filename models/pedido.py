
class Pedido:
    # Contador estático começando em 0, conforme sua lógica
    __contador_id = 0

class Pedido:
    # Adicione o status="Aberto" no final dos parâmetros
    def __init__(self, id_pedido, descricao, quantidade, valor, status="Aberto"):
        self.__id_pedido = id_pedido
        self.__descricao = descricao
        self.__quantidade = quantidade
        self.__valor = valor
        
        self.__status = status

    # IMUTABILIDADE DO ID (Apenas Getter)
    @property
    def id_pedido(self):
        return self.__id_pedido

    # ==========================================
    # GETTERS E SETTERS (Padrão @property)
    # ==========================================
    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao):
        if len(descricao.strip()) > 0:
            self.__descricao = descricao
        else:
            raise ValueError("A descrição/modelo do pedido não pode ser vazia.")
    
    @property
    def quantidade(self):
        return self.__quantidade

    @quantidade.setter
    def quantidade(self, quantidade):
        if quantidade > 0:
            self.__quantidade = quantidade
        else:
            raise ValueError("A quantidade de peças deve ser maior que zero.")

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, valor):
        if valor > 0:
            self.__valor = valor
        else:
            raise ValueError("O valor do pedido deve ser maior que zero.")

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

    # EXIBIÇÃO DO PEDIDO
    def exibir_detalhes(self):
        print(f"• Pedido #{self.id_pedido} | Peça: {self.descricao} | "
              f"Qtd: {self.quantidade} | R$ {self.valor:.2f} | Status: {self.status}")
