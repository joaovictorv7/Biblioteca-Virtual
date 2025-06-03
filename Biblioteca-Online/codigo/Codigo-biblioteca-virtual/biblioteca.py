import json
from pathlib import Path
from adminlog import login  # Importando a função login do arquivo admin/login.py


ARQUIVO_PADRAO = Path("acervo.json")
def sincronizar_com_json(lista, caminho: Path | str = ARQUIVO_PADRAO):
    caminho = Path(caminho)
    if caminho.exists():
        try:
            with caminho.open("r", encoding="utf-8") as f:
                dados = json.load(f)
                lista.clear()
                lista.extend(dados)
        except json.JSONDecodeError:
            print("Aviso: O arquivo JSON está vazio ou corrompido. Iniciando com lista vazia.")


def salvar_json(lista, caminho: Path | str = ARQUIVO_PADRAO):
    caminho = Path(caminho)
    with caminho.open("w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=4)

acervo_online = []
sincronizar_com_json(acervo_online)


def menu():
    while True:
        print('=:=' * 15)
        print('CADASTRAR LIVROS '.center(40))
        print('[1] - Gerenciar livros\n[2] - Sair')
        try:
            escolha = int(input('-: '))
        except ValueError:
            print('Opção inválida. Digite um número de 1 a 2.')
            continue
        if escolha == 1:
            biblioteca()
        elif escolha == 2:
            print("Saindo do sistema...")
            break
        else:
            print('Opção inválida. Tente novamente.')


def biblioteca():
    while True:
        print('=:=' * 15)
        print('LIVROS '.center(40))
        print('[1] - Cadastrar livro\n[2] - Editar Livro\n[3] - Excluir Livro\n[4] - Visualizar Acervo\n[5] - Sair')
        try:
            escolha = int(input('-: '))
        except ValueError:
            print('Opção inválida. Digite um número de 1 a 5.')
            continue
        if escolha == 1:
            cadastar_livro()
        elif escolha == 2:
            editar_livro()
        elif escolha == 3:
            excluir_livro()
        elif escolha == 4:
            visualizar_acervo()
        elif escolha == 5:
            break
        else:
            print('Opção inválida. Tente novamente.')

def pedir_titulo():
    while True:
        titulo = input("Título: ").strip()
        if not titulo:
            print("Erro: O título não pode ser vazio.")
            continue
        for livro in acervo_online:
            if livro['titulo'].lower() == titulo.lower():
                print("Título já cadastrado. Tente outro!")
                break
        else:
            return titulo


def pedir_autor():
    while True:
        autor = input("Autor: ").strip()
        if autor.replace(" ", "").isalpha():
            return autor
        else:
            print("Autor inválido. Digite apenas letras.")


def pedir_sinopse():
    while True:
        sinopse = str(input('Sinopse [MIN 20 CARACTERS]: ')).strip()
        if len(sinopse) >= 20:
            return sinopse
        else:
            print('Erro! Minimo 20 caracters.')
            continue


def pedir_preco():
    while True:
        entrada = input('Preço R$: ').replace(',', '.').strip()
        try:
            preco = float(entrada)
            return preco
        except ValueError:
            print('Digite apenas números válidos!')


def cadastar_livro():
    print('=:=' * 15)
    print('TELA DE CADASTRO'.center(40))
    livro = {
        'titulo': pedir_titulo(),
        'autor': pedir_autor(),
        'sinopse': pedir_sinopse(),
        'preco' : pedir_preco()
    }
    acervo_online.append(livro)
    salvar_json(acervo_online)
    print('=:=' * 15)
    print("Livro cadastrado com sucesso!")
    print(acervo_online)


def editar_livro():
    titulo = input("Título do livro a editar: ").strip()
    if not titulo:
        print("Erro: O título não pode ser vazio.")
        return
    for livro in acervo_online:
        if livro['titulo'].lower() == titulo.lower():
            print("Título encontrado!")
            print('[1] - Mudar Título\n[2] - Mudar Autor\n[3] - Mudar Sinopse\n[4] - Mudar preço')
            try:
                escolha = int(input('-: '))
            except ValueError:
                print("Entrada inválida. Digite um número.")
                return
            if escolha == 1:
                livro['titulo'] = pedir_titulo()
            elif escolha == 2:
                livro['autor'] = pedir_autor()
            elif escolha == 3:
                livro['sinopse'] = pedir_sinopse()
            elif escolha == 4:
                livro['preco'] = pedir_preco()
            else:
                print("Opção inválida.")
                return
            print("Livro atualizado com sucesso!")
            salvar_json(acervo_online)
            return
    print("Livro não encontrado.")


def excluir_livro():
    while True:
        titulo = str(input('Título do livro para excluir: ')).strip()
        encontrado = False
        for livro in acervo_online:
            if livro['titulo'].lower() == titulo.lower():
                acervo_online.remove(livro)
                salvar_json(acervo_online)
                print('Livro removido.')
                encontrado = True
                break
        if encontrado:
            break
        else:
            print(f'O livro "{titulo}" não foi encontrado.')


def visualizar_acervo():
    if not acervo_online:
        print("\nNenhum livro cadastrado no acervo.\n")
        return
    print("\n" + "="*45)
    print("ACERVO DE LIVROS".center(45))
    print("="*45)
    for i, livro in enumerate(acervo_online, start=1):
        print(f"\n📚 Livro {i}")
        print("-" * 30)
        print(f"📖 Título : {livro['titulo']}")
        print(f"👤 Autor  : {livro['autor']}")
        print(f"📝 Sinopse: {livro['sinopse']}")
        print(f"💸 Preço R$: {livro['preco']}")
        print("-" * 30)


if __name__ == "__main__":
    if login():
        menu()
    else:
        print("Falha no login. Encerrando o programa...")