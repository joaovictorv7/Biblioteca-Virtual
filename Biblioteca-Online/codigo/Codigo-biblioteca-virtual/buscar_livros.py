import json
from login_cadastro import menu
from comprar_livro import comprar_livro

def carregar_acervo():
    try:
        with open('acervo.json', 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        print("Arquivo 'acervo.json' não encontrado. Iniciando com acervo vazio.")
    except json.JSONDecodeError:
        print("Erro ao decodificar o arquivo JSON. Iniciando com acervo vazio.")
    return []

def buscar_livro(usuario_logado):
    acervo_online = carregar_acervo()

    if not acervo_online:
        print("\nNenhum livro cadastrado no acervo.\n")
        return

    while True:
        print("\n" + "="*45)
        print("Buscar Livros".center(45))
        print("="*45)
        buscar = input('Livro/Autor que deseja buscar (ou "sair" para encerrar): ').strip().lower()

        if buscar == "sair":
            print("Encerrando a busca de livros. Até logo!")
            break

        encontrado = False
        for indice, livro in enumerate(acervo_online, start=1):
            if buscar in livro['titulo'].lower() or buscar in livro['autor'].lower():
                encontrado = True
                print(f"\n📚 Livro {indice} encontrado")
                print("-" * 30)
                print(f"📖 Título : {livro['titulo']}")
                print(f"👤 Autor  : {livro['autor']}")
                print(f"📝 Sinopse:\n{livro['sinopse']}")
                print(f"💸 Preço  : {livro['preco']}")
                print("-" * 30)

                comprar = input('Adquirir livro? [S/N]: ').upper().strip()
                if comprar == 'S':
                    comprar_livro(usuario_logado, livro['titulo'])
                else:
                    print("✔️ Continuando a busca...\n")

        if not encontrado:
            print("❌ Nenhum livro encontrado com esse termo. Tente novamente.")

if __name__ == "__main__":
    usuario_logado = menu()
    if usuario_logado:
        buscar_livro(usuario_logado)
    else:
        print("Você não fez login!")
