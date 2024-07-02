import connection as game
import subprocess
import time
import os
from random import choice, uniform
import numpy as np

#Executa o jogo de forma automatica no Windowns;
#pasta = os.path.dirname(os.path.abspath(__file__));
#atalho= os.path.join(pasta, 'Game.lnk');
#startupinfo = subprocess.STARTUPINFO();
#startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW;
#process = subprocess.Popen(['cmd', '/c', 'start', '', atalho], startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, close_fds=True, shell=True);

#Inicia o jogo
#start = input("Aperte enter para iniciar o algoritmo")
socket = game.connect(2037)

Q = []

for i in range(96):
    Q.append([0.000000, 0.000000, 0.000000])

# Colocar o caminho relativo para seu txt
path = 'Projeto-SI/Qlearning/resultado.txt'

def escrever_tabela():
    with open(path, "w") as file:
        for line in Q:
            file.write(f"{line[0]:.6f} {line[1]:.6f} {line[2]:.6f}\n")

def carregar_tabela():
    with open(path, 'r') as file:
        for line in range(96):
            Q[line] = [float(x) for x in file.readline().split(" ")]


E: float = 0.15 #Se for usar o decay, é bom ter um E inicial alto, tipo 0.5
E_minimo: float = 0.05
decay: float = 0.997 #Decai 0.3% por loop

def Egreedy(estado_atual):
    global E
    p = uniform(0.00, 1.00)

    if p > E:
            #(1-E)% de ser a melhor
            acao_int = np.argmax(Q[estado_atual])
    else:
            #E% de chance de ser random
            acao_int = choice([0, 1, 2])
    
    #Usa aquele dicionario pra transformar o int em str
    return acao_int

def Egreedy_decay(estado_atual):
    global E
    acao = Egreedy(estado_atual)
    E = max(E_minimo, E*decay) #diminui a chance de escolher algo random da proxima vez
    return acao

carregar_tabela()

def treinar(n_iteracoes):
    estado: int = 0
    ação: int
    alpha = 0.1
    gamma = 0.5
    for _ in range(n_iteracoes):
        ação = Egreedy_decay(estado)
        comando = ["left", "right", "jump"][ação]
        string_estado, r = game.get_state_reward(socket, comando)
        novo_estado = int(string_estado[2:9], 2)
        Q[estado][ação] += alpha * (r + gamma * (max(Q[novo_estado])) - Q[estado][ação])
        estado = novo_estado
        if estado == 0: escrever_tabela()
    escrever_tabela()

    #Fecha a conexão com o jogo
    socket.close()

treinar(100)


