import funct
import os
#######################################################################
#######################################################################
#############                                               ###########
#############                   MAIN                        ###########
#############                                               ###########
#######################################################################
#######################################################################
#
while(True):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('#####################################################################')
    print("########                                                  ###########")
    print("########      Gerador/Verificador de Assinaturas          ###########")
    print("########                                                  ###########")
    print('#####################################################################\n')

    print('Selecione a opcao:')
    print('1 - Gerar as chaves')
    print('2 - Gerar a assinatura')
    print('3 - Validar a assinatura')
    print('4 - Sair')

    op = input()

    if op == '1':
        os.system('cls' if os.name == 'nt' else 'clear')
        funct.gerarChaves() 

    elif op == '2':
        os.system('cls' if os.name == 'nt' else 'clear')
        mensagem = None

        arqMensagem = input('Digite o arquivo da mensagem.txt: ')
        if(os.path.isfile(arqMensagem)):
            with open(arqMensagem, 'rb') as file:
                mensagem = funct.base64.b64encode(file.read())

            chave = None

            arqChave = 'privada.key'

            erro = False
            if(os.path.isfile(arqChave)):
                with open(arqChave, 'r', encoding = 'utf-8') as file:
                    primLinha = file.readline().replace('\r', '\n').replace('\n', '').split('=')
                    segLinha = file.readline().replace('\r', '\n').replace('\n', '').split('=')

                    if segLinha[0] != 'd_mod':
                        print('Erro na utilização da chave, gere um nova na opcao 1 do menu!')
                        erro = True
                    
                    if(erro == False):
                        chave = (primLinha[1], segLinha[1])

                if(erro == False):
                    funct.gerarAssinatura(mensagem, chave)
            else:
                print('Erro, gere uma chave na opcao 1 do menu!')
                input('Aperte Enter para continuar!')
        else:
            print("Erro, o arquivo não existe!")
            input('Aperte Enter para continuar!')

    elif op == '3':
        os.system('cls' if os.name == 'nt' else 'clear')
        mensagem = None

        arqMensagem = input('Digite o arquivo de texto.txt: ')
        if(os.path.isfile(arqMensagem)):
            with open(arqMensagem, 'rb') as file:
                mensagem = funct.base64.b64encode(file.read())

            chave = None

            arqChave = 'publica.key'

            erro = False
            if(os.path.isfile(arqChave)):
                with open(arqChave, 'r', encoding = 'utf-8') as file:
                    primLinha = file.readline().replace('\r', '\n').replace('\n', '').split('=')
                    segLinha = file.readline().replace('\r', '\n').replace('\n', '').split('=')

                    if segLinha[0] != 'exp':
                        print('Erro na utilização da chave, gere um nova na opcao 1 do menu!')
                        erro = True
                    
                    if(erro == False):    
                        chave = (primLinha[1], segLinha[1])
                
                if(erro == False):
                    assinatura = None

                    arqAssinatura = input('Digite o arquivo de assinatura.txt: ')
                    if(os.path.isfile(arqAssinatura)):

                        with open(arqAssinatura, 'r', encoding = 'utf-8') as file:
                            assinatura = file.read()

                        funct.verificarAssinatura(mensagem, chave, assinatura)
                    else:
                        print("Erro, o arquivo não existe!")
                        input('Aperte Enter para continuar!')
            else:
                print('Erro, gere uma chave na opcao 1 do menu!')
                input('Aperte Enter para continuar!')
        else:
            print("Erro, o arquivo não existe!")
            input('Aperte Enter para continuar!')

    elif op == '4':
        exit() 
