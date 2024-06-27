import connection as game
import subprocess
import time
import os

#Executa o jogo de forma automatica no Windowns
pasta = os.path.dirname(os.path.abspath(__file__))
atalho= os.path.join(pasta, 'Game.lnk')
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
process = subprocess.Popen(['cmd', '/c', 'start', '', atalho], startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, close_fds=True, shell=True)

#Inicia o jogo
start = input("Aperte enter para iniciar o algoritmo")
pular, esquerda, direita, socket = "jump", "left", "right", game.connect(2037)

#Inicio do Qlearning
estado, recompensa = game.get_state_reward(socket, pular)
time.sleep(1) #Se botar um movimento seguido do outro sem esperar nenhum tempo, um bugzinho ocorre
estado, recompensa = game.get_state_reward(socket, pular)
time.sleep(1)
estado, recompensa = game.get_state_reward(socket, pular)
time.sleep(1)
estado, recompensa = game.get_state_reward(socket, pular)
time.sleep(1)
estado, recompensa = game.get_state_reward(socket, pular)
time.sleep(1)

#Fecha a conexão com o jogo
socket.close()
