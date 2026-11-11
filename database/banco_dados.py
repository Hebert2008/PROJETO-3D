import sqlite3

class BancoDeDados:
    def __init__(self, nome_banco="mercado_3d.db"):
        # Encapsula a conexão com o banco
        self.__conexao = sqlite3.connect(nome_banco)
        self.__cursor = self.__conexao.cursor()
        self.__criar_tabelas()

    def __criar_tabelas(self):
        """Método privado que roda assim que o banco é instanciado para garantir que as tabelas existam."""
        
        # Criação da tabela de Usuários (juntando Solicitantes e Impressores)
        self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                tipo TEXT NOT NULL -- 'solicitante' ou 'impressor'
            )
        ''')

        # Criação da tabela de Pedidos
        self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                valor REAL NOT NULL,
                status TEXT NOT NULL,
                id_solicitante INTEGER,
                id_impressor INTEGER,
                FOREIGN KEY (id_solicitante) REFERENCES usuarios(id),
                FOREIGN KEY (id_impressor) REFERENCES usuarios(id)
            )
        ''')
        self.__conexao.commit()

    # ==========================================
    # MÉTODOS DE NEGÓCIO (CRUD)
    # ==========================================
    def inserir_usuario(self, nome, email, senha, tipo):
        try:
            self.__cursor.execute('''
                INSERT INTO usuarios (nome, email, senha, tipo) 
                VALUES (?, ?, ?, ?)
            ''', (nome, email, senha, tipo))
            self.__conexao.commit()
            return True
        except sqlite3.IntegrityError:
            raise ValueError("Erro: Já existe um usuário cadastrado com este e-mail.")

    

    def inserir_pedido(self, descricao, quantidade, valor, id_solicitante):
        self.__cursor.execute('''
            INSERT INTO pedidos (descricao, quantidade, valor, status, id_solicitante) 
            VALUES (?, ?, ?, 'Aberto', ?)
        ''', (descricao, quantidade, valor, id_solicitante))
        self.__conexao.commit()
        return self.__cursor.lastrowid # Retorna o ID gerado automaticamente

    def buscar_pedidos_abertos(self):
        self.__cursor.execute("SELECT * FROM pedidos WHERE status = 'Aberto'")
        return self.__cursor.fetchall()

    def atualizar_status_pedido(self, id_pedido, id_impressor, novo_status):
        self.__cursor.execute('''
            UPDATE pedidos 
            SET status = ?, id_impressor = ? 
            WHERE id = ?
        ''', (novo_status, id_impressor, id_pedido))
        self.__conexao.commit()

    def fechar_conexao(self):
        self.__conexao.close()