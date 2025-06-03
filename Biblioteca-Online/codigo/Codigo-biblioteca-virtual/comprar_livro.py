import json
from pathlib import Path

ARQUIVO_PADRAO = Path("formas_pagamento.json")
ARQUIVO_PESSOAS = Path("pessoas.json")

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

def comprar_livro(usuario_logado, titulo_livro):
    if not opcoes:
        print("\nNenhuma forma de pagamento cadastrada.\n")
        return

    print("\n" + "="*45)
    print("Formas de pagamentos".center(45))
    print("="*45)
    for i, opcao in enumerate(opcoes, start=1):
        print(f"\n Opção {i}")
        print("-" * 30)
        print(f" Forma: {opcao.get('Forma', 'Não informado')}")
        print(f" Disponibilidade: {opcao.get('Disponibilidade', 'Não informado')}")
        print("-" * 30)

    while True:
        escolha = input("Digite a forma de pagamento que deseja: ").strip().casefold()
        if not escolha:
            print("Forma de pagamento não informada.")
            return

        for opcao in opcoes:
            if opcao['Forma'].casefold() == escolha:
                if opcao['Disponibilidade'].casefold() == 'disponível':
                    print("-" * 30)
                    print(f"Disponibilidade atual: {opcao['Disponibilidade']}")
                    print('Chave pix: joãovictor@gmail.com')
                    adicionar_livro_comprado(usuario_logado, titulo_livro)
                    print("-" * 30)
                else:
                    print('Opção Indisponível. Por favor, use outra.')
                return

        print("Opção Indisponível. Por favor, use outra.")

def adicionar_livro_comprado(usuario_logado, titulo_livro):
    comprovante = input('Comprovante [S/N] : ').upper().strip()
    if comprovante != 'S':
        print("Compra não realizada.")
        return

    try:
        with ARQUIVO_PESSOAS.open("r", encoding="utf-8") as f:
            pessoas = json.load(f)
    except FileNotFoundError:
        print("Arquivo pessoas.json não encontrado.")
        return
    except json.JSONDecodeError:
        print("Erro ao ler o arquivo pessoas.json.")
        return

    for pessoa in pessoas:
        if pessoa.get("cpf") == usuario_logado.get("cpf"):
            if "livros_comprados" not in pessoa:
                pessoa["livros_comprados"] = []
            pessoa["livros_comprados"].append(titulo_livro)
            print(f"✅ Livro '{titulo_livro}' adicionado ao perfil de {pessoa['nome']}.")

            with ARQUIVO_PESSOAS.open("w", encoding="utf-8") as f:
                json.dump(pessoas, f, ensure_ascii=False, indent=4)
            return

    print("❌ Usuário logado não encontrado no cadastro.")
