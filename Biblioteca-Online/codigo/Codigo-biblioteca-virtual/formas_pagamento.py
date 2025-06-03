import json
from pathlib import Path


ARQUIVO_PADRAO = Path("formas_pagamento.json")
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

opcoes = []
sincronizar_com_json(opcoes)


def menu():
    while True:
        print('=:=' * 15)
        print('CADASTRAR LIVROS '.center(40))
        print('[1] - Adicionar Forma de Pagamento\n[2] - Alterar disponibilidade\n[3] - Visualizar Formas de Pagamento\n[4] - Sair')
        try:
            escolha = int(input('-: '))
        except ValueError:
            print('Opção inválida. Digite um número de 1 a 2.')
            continue
        if escolha == 1:
            formas_pagamentos()
        elif escolha == 2:
            editar_disponibilidade()
        elif escolha == 3:
            pagamento_disponiveis()
        elif escolha == 4:
            print("Saindo do sistema...")
            break
        else:
            print('Opção inválida. Tente novamente.')


def pedir_forma():
    while True:
        escolha = input("Forma de pagamento: ").strip().upper()
        if escolha.replace(" ", "").isalpha():
            return escolha
        else:
            print("Forma de pagamento inválida. Digite apenas letras.")


def disponibilidade():
    while True:
        escolha = input("Disponível - [D] / Indisponível - [I]: ").strip().upper()
        if escolha == 'D':
            return 'Disponível'
        elif escolha == 'I':
            return 'Indisponível'
        else:
            print("Erro. Digite apenas [D] ou [I].")


def formas_pagamentos():
    nova_opcao = {
        'Forma': pedir_forma(),
        'Disponibilidade': disponibilidade()
    }
    opcoes.append(nova_opcao)
    salvar_json(opcoes)


def pagamento_disponiveis():
    if not opcoes:
        print("\nNenhuma forma de pagamento cadastrada.\n")
        return
    print("\n" + "="*45)
    print("Formas de pagamentos".center(45))
    print("="*45)
    for i, opcao in enumerate(opcoes, start=1):
        print(f"\n Opção {i}")
        print("-" * 30)
        print(f" Forma: {opcao['Forma']}")
        print(f" Disponibilidade: {opcao['Disponibilidade']}")
        print("-" * 30)


def editar_disponibilidade():
    forma = input("Digite a forma de pagamento que deseja alterar a disponibilidade: ").strip().upper()
    if not forma:
        print("Forma de pagamento não informada.")
        return

    for opcao in opcoes:
        if opcao['Forma'].upper() == forma:
            print(f"Forma de pagamento encontrada: {opcao['Forma']}")
            print(f"Disponibilidade atual: {opcao['Disponibilidade']}")
            nova_disponibilidade = disponibilidade()
            opcao['Disponibilidade'] = nova_disponibilidade
            salvar_json(opcoes)
            print("Disponibilidade atualizada com sucesso!")
            return

    print("Forma de pagamento não encontrada.")

if __name__ == "__main__":
    menu()