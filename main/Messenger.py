import socket
import sys


def start_messenger(arg):
    host = socket.gethostname()
    port = 8899

    s = socket.socket()#socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host, port))

    s.sendall(bytes(arg, encoding='UTF-8'))

    data = s.recv(1024)
    s.close()

    print('Resposta: ', data.decode('utf-8'))


user_command = input('Insira a mensagem: ')
while user_command is not '\exit':
    start_messenger(user_command)
    user_command = input('Insira a mensagem: ')
