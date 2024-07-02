import connection as game
import subprocess
import time
import os
from random import choice, uniform
from numpy import argmax

#Inicia o jogo
socket = game.connect(2037)

Q = []

for i in range(96):
    Q.append([0.000000, 0.000000, 0.000000])

E: float = 0.15 #Se for usar o decay, é bom ter um E inicial alto, tipo 0.5
E_minimo: float = 0.2
decay: float = 1 - 10e-5

# Colocar os caminho relativos para seus txts
path = {
    'Q' : 'Projeto-SI/Qlearning/resultado.txt',
    'E' : 'Projeto-SI/Qlearning/E.txt'
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
    return choice([0, 1, 2, 2, 2])

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

carregar_tabela()

def treinar(algoritmo, n_iteracoes):
    carregar_E()
    estado: int = 0
    ação: int
    alpha = 0.05
    gamma = 0.7
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
            i += 1
            escrever_E()
            print(f"E: {E:.2f}")
            escrever_tabela()
            if i < n_iteracoes: print(f"rodada {i+1}")

    #Fecha a conexão com o jogo
    socket.close()

treinar(Egreedy_decay, 1500)


