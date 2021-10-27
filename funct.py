from random import randrange, getrandbits, choice
from string import ascii_letters
from hashlib import sha3_512, sha3_256
from tqdm import tqdm
import base64
import pathlib
import os
import os.path
#
def verificarAssinatura(mensagem, chave, assinatura):
    hash = int.from_bytes(sha3_256(mensagem).digest(), byteorder = 'big')
    hashAssinatura = pow(int(assinatura), int(chave[1]), int(chave[0]))

    if hash == int.from_bytes(decriptaOAEP(hashAssinatura), byteorder = 'big'):
        print('Assinatura Válida.')
    else:
        print('Assinatura Inválida.')
    input('Aperte Enter para continuar!')

def encriptaOAEP(mensagem):
    mm = mensagem + (b'\x00' * 32)
    r = ''.join(choice(ascii_letters) for i in range(64)).encode('ascii')
    G = sha3_512(r).digest()
    X = funcaoXOR(mm, G)
    H = sha3_512(X).digest()
    Y = funcaoXOR(r, H)

    return X + Y

def decriptaOAEP(assinatura):
    XY = int(assinatura).to_bytes(128, 'big')
    r = funcaoXOR(XY[64:], sha3_512(XY[:64]).digest())
    mm = funcaoXOR(XY[:64], sha3_512(r).digest())
    return mm[0:32]

def gerarAssinatura(mensagem, chave):
    hash = int.from_bytes(encriptaOAEP(sha3_256(mensagem).digest()), byteorder = 'big')
    assinatura = pow(hash, int(chave[1]), int(chave[0]))

    assinatura_caminho = pathlib.Path('assinatura.txt').absolute()
    print(f"Escrevendo a assinatura em {assinatura_caminho}")

    with open(assinatura_caminho, 'w', encoding = 'utf-8') as file:
        file.write(f"{assinatura}")
    input('Aperte Enter para continuar!')

def gerarChaves():
    for i in tqdm(range(1), desc="Gerando chaves"):
        prim = gerarNumeroPrimo()
        seg = gerarNumeroPrimo()
        n = prim * seg
        
    #print('Gerando os números em (p-1)*(q-1)...')
    while True:
        exp = randrange(2 ** 1, 2 ** 16)
        if mdc(exp, (prim - 1) * (seg - 1)) == 1:
            break
    
    #print('Calculando d mod inverso de e...')
    d_mod = calcularInversoMod(exp, (prim - 1) * (seg - 1))

    caminho = pathlib.Path().absolute()
   
    if (not os.path.exists(caminho)):
        os.makedirs(caminho)

    print(f"Salvando as chaves em {caminho}")
    with open(pathlib.Path("publica.key").absolute(), 'w', encoding = 'utf-8') as file:
        file.write(f"n={n}\nexp={exp}")

    with open(pathlib.Path(f"privada.key").absolute(), 'w', encoding = 'utf-8') as file:
        file.write(f"n={n}\nd_mod={d_mod}")
    i = input('Deseja exibir as chaves? (s/n)\n')
    if(i == 's' or i == 'S'):
        print('n = ',n)
        print('Publica(exp) = ',exp )
        print('Privada(d_mod) = ',d_mod)
    
        input('Aperte Enter para continuar!')


def numPrimo(numero, k=128):

    if numero == 2 or numero == 3:
        return True
    if numero <= 1 or numero % 2 == 0:
        return False
    
    s = 0
    r = numero - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    
    for _ in range(k):
        a = randrange(2, numero - 1)
        x = pow(a, r, numero)
        if x != 1 and x != numero - 1:
            j = 1
            while j < s and x != numero - 1:
                x = pow(x, 2, numero)
                if x == 1:
                    return False
                j += 1
            if x != numero - 1:
                return False
    return True

def gerarCandPrim(tamanho):

    # generate random bits
    p = getrandbits(tamanho)
    # apply a mask to set MSB and LSB to 1
    p |= (1 << tamanho - 1) | 1
    return p

def gerarNumeroPrimo():
    tamanho = 1024
    p = 4
    # enquanto ha falha no teste de primalidade
    while not numPrimo(p, 128):
        p = gerarCandPrim(tamanho)
    return p

def mdc(x, y): #Maximo Divisor Comum
    while x != 0:
        x, y = y % x, x
    return y

def calcularInversoMod(a, m):
    if mdc(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

def funcaoXOR(x, y):
    assert len(x) == len(y)
    return bytearray([ xx ^ yy for xx, yy in zip(x, y)])
