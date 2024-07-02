import connection as game
from numpy import argmax, max as listmax
from random import choice, uniform

#Variaveis globais
n_iteracoes: int = 100
plataforma: int
direção: int
estado: int = 0
ação: int
alpha = 0.1
gamma = 0.5
Ep = 0.80 #Ver um valor legal depois
E_minimo = 0.05
decay = 0.997 
q_table = [[0.0, 0.0, 0.0] for i in range(96)]
path = 'Qlearning/resultado.txt'
ac = {0 : "left", 1 : "right", 2 : "jump"}

#Funções
def escrever_tabela():
    with open(path, "w") as file:
        for line in q_table:
            file.write(f"{line[0]:.6f} {line[1]:.6f} {line[2]:.6f}\n")

def carregar_tabela():
    with open(path, 'r') as file:
        for line in range(96):
            q_table[line] = [float(x) for x in file.readline().split(" ")]

def Egreedy(estado_atual):
        p = uniform(0.00, 1.00)
        if p > Ep:
                acao_int = argmax(q_table[estado_atual])
        else:
                acao_int = choice([0, 1, 2])
        return acao_int

def Egreedy_decay(estado_atual):
        global Ep
        acao = Egreedy(estado_atual)
        Ep = max(E_minimo, Ep*decay)
        return acao


#Iniciando conexão com o jogo e carregando a tabela salva
socket = game.connect(2037)
carregar_tabela()
print("TABLE\n\n\n", q_table, "\n\n\n")

#Qlearning
for i in range(n_iteracoes):
    ação = Egreedy_decay(estado)
    string_estado, r = game.get_state_reward(socket, ac[ação])
    novo_estado = int(string_estado[2:9], 2)
    q_table[estado][ação] += alpha * (r + gamma * listmax(q_table[novo_estado]) - q_table[estado][ação]) #Pelo que eu testei, tá funcionando desse jeito a função, mas é bom conferir
    #testar se a função funfa
    estado = novo_estado

#Salvando a tabela e fechando conexão com o jogo
escrever_tabela()
print(q_table)
socket.close()
