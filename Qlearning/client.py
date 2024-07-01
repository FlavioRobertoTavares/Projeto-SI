import connection as game
import subprocess
import time
import os
from random import choice

#Executa o jogo de forma automatica no Windowns;
#pasta = os.path.dirname(os.path.abspath(__file__));
#atalho= os.path.join(pasta, 'Game.lnk');
#startupinfo = subprocess.STARTUPINFO();
#startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW;
#process = subprocess.Popen(['cmd', '/c', 'start', '', atalho], startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, close_fds=True, shell=True);

#Inicia o jogo
#start = input("Aperte enter para iniciar o algoritmo")
pular, esquerda, direita, socket = "jump", "left", "right", game.connect(2037)

q_table = []

for i in range(96):
    q_table.append([0.000000, 0.000000, 0.000000])

# Colocar o caminho relativo para seu txt
path = 'Projeto-SI/Qlearning/resultado.txt'

def escrever_tabela():
    with open(path, "w") as file:
        for line in q_table:
            file.write(f"{line[0]:.6f} {line[1]:.6f} {line[2]:.6f}\n")

def carregar_tabela():
    with open(path, 'r') as file:
        for line in range(96):
            q_table[line] = [float(x) for x in file.readline().split(" ")]

print("TABLE\n\n\n", q_table, "\n\n\n")
#Inicio do Qlearning
n_iteracoes: int = 1000
plataforma: int
direção: int
estado: int = 0
ação: int
alpha = 0.1
gamma = 0.5

ac = {
    "left" : 0,
    "right" : 1,
    "jump" : 2,
}

for i in range(n_iteracoes):
    comando = choice([esquerda, direita, pular])
    string_estado, r = game.get_state_reward(socket, comando)
    ação = ac[comando]
    plataforma = int(string_estado[2:7], 2)
    direção = int(string_estado[7:9], 2)
    novo_estado = int(string_estado[2:9], 2)
    q_table[estado][ação] += alpha * (r + gamma * (max(q_table[novo_estado][0],
                                                        q_table[novo_estado][1],
                                                        q_table[novo_estado][2])))
    estado = novo_estado
escrever_tabela()
print(q_table)
socket.close()

#Fecha a conexão com o jogo
socket.close()
