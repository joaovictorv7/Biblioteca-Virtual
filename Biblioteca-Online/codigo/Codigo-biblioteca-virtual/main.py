from login_cadastro import menu as menu_usuario
from suporte_msg import mensagem as mensagem_suporte
from adminlog import login as login_admin
from biblioteca import biblioteca 
from formas_pagamento import menu 
from buscar_livros import buscar_livro
from historico_compras import exibir_historico_usuario

def main():
    while True:
        print('=:=' * 15)
        print('BIBLIOTECA ONLINE'.center(40))
        print('[1] - Cadastrar/Login\n[2] - Falar com o suporte\n[3] - Área de ADMIN\n[4] - Sair')
        try:
            escolha = int(input('-: '))
        except ValueError:
            print('Opção inválida. Digite um número de 1 a 4.')
            continue

        if escolha == 1:
            usuario_logado = menu_usuario()
            if not usuario_logado:
                continue

            while True:
                print('=:=' * 15)
                print('BEM-VINDO'.center(40))
                print('[1] - Procurar livro\n[2] - Histórico de Compra\n[3] - Sair')
                try:
                    opcao = int(input('-: '))
                except ValueError:
                    print('Opção inválida. Digite um número de 1 a 3.')
                    continue

                if opcao == 1:
                    buscar_livro(usuario_logado)
                elif opcao == 2:
                    exibir_historico_usuario(usuario_logado)
                elif opcao == 3:
                    break

        elif escolha == 2:
            mensagem_suporte()

        elif escolha == 3:
            if login_admin():
                print('=:=' * 15)
                print('ADMINISTRADOR'.center(40))
                print('[1] - Gerenciar pagamentos\n[2] - Gerenciar biblioteca\n[3] - Sair')
                try:
                    opcao = int(input('-: '))
                except ValueError:
                    print('Opção inválida. Digite um número de 1 a 3.')
                    continue
                if opcao == 1:
                    menu()
                elif opcao == 2:
                    biblioteca()
                elif opcao == 3:
                    break
            else:
                print("Login de administrador falhou.")

        elif escolha == 4:
            print("Encerrando o sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
