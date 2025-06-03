import json
from datetime import datetime


def carregar_pessoas():
    try:
        with open('pessoas.json', 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        print("Arquivo 'pessoas.json' não encontrado. Iniciando com lista vazia.")
    except json.JSONDecodeError:
        print("Erro ao decodificar o arquivo JSON. Iniciando com lista vazia.")
    return []


def enviar_mensagem_suporte(cpf, nome, mensagem, arquivo="suporte.json"):
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            mensagens = json.load(f)
    except FileNotFoundError:
        mensagens = []

    novo_registro = {
        "nome": nome,
        "cpf": cpf,
        "mensagem": mensagem,
        "data": datetime.now().isoformat(timespec="seconds")
    }

    mensagens.append(novo_registro)

    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(mensagens, f, indent=2, ensure_ascii=False)

    print("✅ Sua mensagem foi enviada ao suporte.")


def encontrar_pessoa_por_email(pessoas, email_digitado):
    email_digitado = email_digitado.strip().lower()
    for pessoa in pessoas:
        email_salvo = pessoa.get("email", "").strip().lower()
        if email_salvo == email_digitado:
            return pessoa
    return None


def mensagem():
    email = input("Digite seu email: ").strip().lower()
    pessoas = carregar_pessoas()
    pessoa_encontrada = encontrar_pessoa_por_email(pessoas, email)
    if pessoa_encontrada:
        nome = pessoa_encontrada["nome"]
        cpf = pessoa_encontrada["cpf"]
        mensagem_texto = input("📩 Digite sua mensagem para o suporte: ")
        enviar_mensagem_suporte(cpf, nome, mensagem_texto)
    else:
        print("❌ Email não encontrado entre os cadastrados.")

if __name__ == "__main__":
    mensagem()