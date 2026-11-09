from models.impressor import Impressor
# Se já tiver o arquivo models/pedido.py pronto, descomente a linha abaixo:
# from models.pedido import Pedido

# Dublê temporário de Pedido apenas para testar o Impressor isoladamente:
class PedidoTeste:
    def __init__(self, id_pedido, status="Em Produção"):
        self.__id_pedido = id_pedido
        self.__status = status

    def get_id_pedido(self):
        return self.__id_pedido

    def get_status(self):
        return self.__status


def main():
    print("=== 1. TESTANDO CRIAÇÃO E HERANÇA (USUARIO -> IMPRESSOR) ===")
    impressor = Impressor(1, "Carlos Maker", "carlos@maker.com", "senha123")
    impressor.exibir_painel()

    print("\n=== 2. TESTANDO ASSUMIR PEDIDOS ===")
    p1 = PedidoTeste(101, "Em Produção")
    p2 = PedidoTeste(102, "Aberto")

    impressor.assumir_pedido(p1)
    impressor.assumir_pedido(p2)
    impressor.exibir_painel()

   

if __name__ == "__main__":
    main()