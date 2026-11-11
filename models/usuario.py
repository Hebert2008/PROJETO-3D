from abc import ABC, abstractmethod

class Usuario(ABC):

    #CONSTRUTOR:
    def __init__(self, id, nome, email, senha):
        self.__id = id
        self.set_nome(nome)
        self.set_email(email)
        self.set_senha(senha)

    #MÉTODOS ID:
    def get_id(self):
        return self.__id  

    #MÉTODOS NOME:
    def get_nome(self):
        return self.__nome
    
    def set_nome(self, nome):
        if len(nome.strip()) > 2: 
            self.__nome = nome
        else:
            raise ValueError ("Nome inválido. O nome não pode ser vazio.")
            

    #MÉTODOS EMAIL:
    def get_email(self):
        return self.__email

    def set_email(self, novo_email):
        # Trocamos o "." genérico pela exigência do ".com"
        if "@" in novo_email and ".com" in novo_email and len(novo_email.strip()) > 0:
            self.__email = novo_email
        else:
            raise ValueError("E-mail inválido. O e-mail deve conter '@' e '.com'.")
        
    #MÉTODO SENHA:
    def get_senha(self):
        return self.__senha

    def set_senha(self, nova_senha):
        if len(nova_senha.strip()) >= 6:
            self.__senha = nova_senha
        else:
            raise ValueError("Senha inválida. A senha deve ter pelo menos 6 caracteres.")


    #PAINEL:

    def exibir_user_info(self):
        print("\n" + "=" * 45)
        print(f"  USUÁRIO: {self.get_nome().upper()}")
        print("=" * 45)
        print(f"E-mail: {self.get_email()}")

    @abstractmethod
    def exibir_opcoes(self):
        pass

    @abstractmethod
    def exibir_painel(self):
        pass
        