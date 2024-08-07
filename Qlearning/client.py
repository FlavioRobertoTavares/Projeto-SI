import connection as game
import subprocess
import time
import os   
from random import choice, uniform
from numpy import argmax, sum, array, exp
from numpy.random import choice as choose

#Inicia o jogo
socket = game.connect(2037)

Q = []

for i in range(96):
    Q.append([0.000000, 0.000000, 0.000000])

E: float #Se for usar o decay, é bom ter um E inicial alto, tipo 0.5
E_minimo: float = 0.15
decay: float = 1 - 3*10e-6
Temperatura : float = 0.1 #Quanto menor o valor de temperatura, maior a chance de escolher a melhor ação

# Colocar os caminho relativos para seus txts
path = {
    'Q' : 'Qlearning/resultado.txt',
    'E' : 'Qlearning/E.txt'
}

def escrever_tabela():
    with open(path['Q'], 'w') as file:
        for line in Q:
            file.write(f"{line[0]:.6f} {line[1]:.6f} {line[2]:.6f}\n")

def carregar_tabela():
    with open(path['Q'], 'r') as file:
        for line in range(96):
            Q[line] = [float(x) for x in file.readline().split(" ")]

def escrever_E():
    global E
    with open(path['E'], 'w') as file:
        file.write(f'{E:.4f}')

def carregar_E():
    global E
    with open(path['E'], 'r') as file:
        E = float(file.read())

def random_search(estado_atual):
    return choice([0, 1, 2])

def Win(estado_atual):
    acao_int = Q[estado_atual].index(max(Q[estado_atual]))
    return acao_int

def Egreedy(estado_atual):
    global E
    p = uniform(0.00, 1.00)

    if p > E:
        #(1-E)% de ser a melhor
        acao_int = argmax(Q[estado_atual])
    else:
        #E% de chance de ser random
        acao_int = random_search(estado_atual)

    #Usa aquele dicionario pra transformar o int em str
    return acao_int

def Egreedy_decay(estado_atual):
    global E
    acao = Egreedy(estado_atual)
    E = max(E_minimo, E*decay) #diminui a chance de escolher algo random da proxima vez
    return acao

def Tratar(q):

    index = q.index(min(q))
    deltas = [abs(q[index] - q[x]) for x in range (3) if x != index]

    for i in range (3):
        if i == index:
            q[i] = abs(q[i])
        
        else:
            q[i] = abs(q[index]) + deltas.pop(0)
    
    return q

def Softmax(estado_atual):
    Qt = Tratar(Q[estado_atual])
    if(sum(Qt) == 0): return random_search(estado_atual) #caso seja a primeira vez naquela linha da qtable

    possiveis_valores = [(x*x)/Temperatura for x in Qt]
    valor_total = sum(possiveis_valores)
    probabilidades = possiveis_valores / valor_total
    
    acao_int = choose([0, 1, 2], p=probabilidades)
    return acao_int

carregar_tabela()

def treinar(algoritmo, n_iteracoes):
    carregar_E()
    estado: int = 0
    ação: int
    alpha = 0.1
    gamma = 0.96
    i = 0
    print(f"rodada 1")
    while (i < n_iteracoes):
        ação = algoritmo(estado)
        comando = ["left", "right", "jump"][ação]
        string_estado, r = game.get_state_reward(socket, comando)
        novo_estado = int(string_estado[2:9], 2)
        Q[estado][ação] += alpha * (r + gamma * (max(Q[novo_estado])) - Q[estado][ação])
        estado = novo_estado
        if (r < -20) or (r > 0):
            if r > 0: print("YAAAAAY!!!!!!!!!!!")
            i += 1
            if i % 4 == 3:
                escrever_tabela()
                escrever_E()
            print(f"E: {E:.4f}")
            if i < n_iteracoes: print(f"rodada {i+1}")

    #Fecha a conexão com o jogo
    socket.close()

treinar(Win, 5)


