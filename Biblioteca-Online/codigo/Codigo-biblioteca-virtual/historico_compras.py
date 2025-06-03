import json

def carregar_pessoas(arquivo="pessoas.json"):
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def historico_de_compras(usuario_logado, pessoas):
    email = usuario_logado['email']
    for pessoa in pessoas:
        if pessoa['email'] == email:
            print(f"\nHistórico de compras de {pessoa['nome']}:")
            livros = pessoa.get('livros_comprados', [])
            if livros:
                for i, livro in enumerate(livros, start=1):
                    print(f"{i}. {livro}")
            else:
                print("Nenhuma compra registrada!")
            break
    else:
        print("Usuário não encontrado.")

def exibir_historico_usuario(usuario_logado):
    if usuario_logado:
        pessoas = carregar_pessoas()
        historico_de_compras(usuario_logado, pessoas)
    else:
        print("Você não fez login!")
