import re
from datetime import datetime
import json
import hashlib


def carregar_pessoas():
    try:
        with open('pessoas.json', 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        print("Arquivo 'pessoas.json' não encontrado. Iniciando com lista vazia.")
    except json.JSONDecodeError:
        print("Erro ao decodificar o arquivo JSON. Iniciando com lista vazia.")
    return []


pessoas_cadastradas = carregar_pessoas()
def salvar_pessoas():
    with open('pessoas.json', 'w', encoding='utf-8') as arquivo:
        json.dump(pessoas_cadastradas, arquivo, ensure_ascii=False, indent=4)


def menu():
    while True:
        print('=:=' * 15)
        print('LOGIN/CADASTRO'.center(40))
        print('[1] - Cadastro\n[2] - Login\n[3] - Sair')
        try:
            escolha = int(input('-: '))
        except ValueError:
            print('Opção inválida. Digite um número de 1 a 3.')
            continue
        if escolha == 1:
            cadastro()
        elif escolha == 2:
            usuario_logado = login()
            if usuario_logado:
                return usuario_logado
            else:
                print("❌ Falha no login.")
        elif escolha == 3:
            return None
        else:
            print('Opção inválida. Tente novamente.')

def pedir_nome():
    while True:
        nome = input("Nome: ").strip()
        if nome.replace(" ", "").isalpha():
            return nome
        else:
            print("Nome inválido. Digite apenas letras.")


def pedir_email():
    while True:
        email = input("Email: ").strip()
        padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'
        if not re.match(padrao, email):
            print("Email inválido. Tente novamente.")
            continue
        
        for pessoa in pessoas_cadastradas:
            if pessoa['email'] == email:
                print("Email já existe. Tente outro!")
                break
        else:
            return email   
        
             
def pedir_senha():
    while True:
        senha = str(input('Senha: ')).strip()
        if len(senha) < 6:
            print('Minimo 6 caracters!')
            continue
        else:
            hash_senha = hash_senha = hashlib.sha256(senha.encode()).hexdigest()
            return hash_senha
    

def pedir_cpf():
    while True:
        cpf_usuario = input('CPF [somente números, sem traços ou pontos]: ').strip()

        if not cpf_usuario.isdigit():
            print("Entrada inválida. Digite apenas números.")
            continue

        if not autenticador_cpf(cpf_usuario):
            print("CPF inválido.")
            continue

        for pessoa in pessoas_cadastradas:
            if pessoa['cpf'] == cpf_usuario:
                print("CPF já existe. Tente outro!")
                break
        else:
            return cpf_usuario


def autenticador_cpf(cpf):
    cpf_enviado_usuario = re.sub(r'\D', '', cpf)

    if len(cpf_enviado_usuario) != 11:
        print("CPF deve conter 11 dígitos numéricos.")
        
    entrada_e_sequencial = cpf_enviado_usuario == cpf_enviado_usuario[0] * 11
    if entrada_e_sequencial:
        print('Você enviou dados sequenciais. CPF inválido ❌')

    nove_digitos = cpf_enviado_usuario[:9]
    contador_regressivo_1 = 10
    resultado_digito_1 = 0
    for digito in nove_digitos:
        resultado_digito_1 += int(digito) * contador_regressivo_1
        contador_regressivo_1 -= 1

    digito_1 = (resultado_digito_1 * 10) % 11
    digito_1 = digito_1 if digito_1 <= 9 else 0

    dez_digitos = nove_digitos + str(digito_1)
    contador_regressivo_2 = 11
    resultado_digito_2 = 0
    for digito in dez_digitos:
        resultado_digito_2 += int(digito) * contador_regressivo_2
        contador_regressivo_2 -= 1

    digito_2 = (resultado_digito_2 * 10) % 11
    digito_2 = digito_2 if digito_2 <= 9 else 0

    cpf_gerado_pelo_calculo = f'{nove_digitos}{digito_1}{digito_2}'

    if cpf_enviado_usuario == cpf_gerado_pelo_calculo:
        return True
    else:
        return False


def pedir_data():
    while True:
        data = input("Digite sua data de nascimento (dd/mm/aaaa): ")
        try:
            nascimento = datetime.strptime(data, "%d/%m/%Y")
            if nascimento.year < 1900:
                print("Ano muito antigo. Digite um ano a partir de 1900.")
                continue
            return data
        except ValueError:
            print("Formato inválido. Use dd/mm/aaaa.")
        return


def login():
    print('=:=' * 15)
    print('TELA DE LOGIN'.center(40))
    email = input("EMAIL: ").strip()
    pessoa_encontrada = None
    for pessoa in pessoas_cadastradas:
        if pessoa['email'] == email:
            pessoa_encontrada = pessoa
            break
    if pessoa_encontrada:
        while True:
            senha = input("Senha: ")
            hash_senha = hashlib.sha256(senha.encode()).hexdigest()
            if hash_senha == pessoa_encontrada['senha']:
                print("✅ Acesso liberado.")
                return pessoa_encontrada
            else:
                print("Senha inválida. Tente novamente.")
    else:
        print("Email não encontrado.")
    print('=:=' * 15)
    return None


def cadastro():
    print('=:=' * 15)
    print('TELA DE CADASTRO'.center(40))
    cadastro = {
        'nome': pedir_nome(),
        'email': pedir_email(),
        'senha': pedir_senha(),
        'cpf': pedir_cpf(),
        'data_nascimento': pedir_data()
    }
    pessoas_cadastradas.append(cadastro)
    salvar_pessoas()
    print("✅ Cadastro realizado com sucesso!")
    print('=:=' * 15)
