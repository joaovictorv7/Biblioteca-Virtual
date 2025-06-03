admin = {'email': 'admin@.com', 'senha': '123'}

def login():
    while True:
        email = input("EMAIL ADMIN: ").strip()
        if email == admin['email']:
            while True:
                senha = input("Senha: ").strip()
                if senha == admin['senha']:
                    print("Acesso de admin liberado.")
                    return True
                else:
                    print("Senha inválida. Tente novamente.")
        else:
            print("Email inválido. Tente novamente.")
        print('=:=' * 15)