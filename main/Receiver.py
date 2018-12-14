import geocoder
import socket
import datetime
import urllib.request as req
import re
import sys
import os
from uuid import getnode as get_mac
sys.path.append(os.getcwd())


def start_receiver():
    '''
    Escuta a porta 8899 e processa qualquer mensagem que receber
    :return:
    '''
    host = '0.0.0.0'
    port = 8899

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))

    print('host: %s  port: %s' % (host, port))

    s.listen(5)

    while True:
        conn, addr = s.accept()
        print('Address: ', addr)
        try:
            data = conn.recv(1024)

            if not data:
                break
            print('Data: ', data)

            message = decode_command(data.decode('utf-8'))
            conn.sendall(bytes(message, encoding='UTF-8'))

        except socket.error:
            print('Message failed')
            break

        # time.sleep(1)
        # print('looping...')

    conn.close()


def get_dolar():
    cot = Cotacao()
    return '$' + str(cot.dolar())


def get_euro():
    cot = Cotacao()
    return '€' + str(cot.euro())


def get_location():
    g = geocoder.ip('me')
    j = g.geojson

    return j.get('features')[0].get('properties').get('address')


def get_sys_info():
    return os.uname()


def get_server_mac():
    return get_mac()


def decode_command(user_command):
    '''
    Recebe o comando do usuário e procura na lista de comandos existentes a resposta adequada.
    :param user_command:
    :return:
    '''

    print('command received: ', user_command)
    return{
        '\ip': socket.gethostbyname(socket.gethostname()),
        '\dev': "Jean Juba",
        '\dolar': get_dolar(),
        '\euro': get_euro(),
        '\location': get_location(),
        '\\time': datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S'),
        '\sys': str(get_sys_info())[18:],
        '\mac': str(hex(get_server_mac()))
    }.get(user_command, "Not Found")


class Cotacao:
    '''
    Classe que possui os métodos para as cotações do euro e do dólar.
    '''

    def __init__(self):
        pass

    def __get_cotacao(self, url, regex='^.*nacional" value="([0-9,]+)"'):
        pagina = req.urlopen(url)
        s = pagina.read().decode('utf-8')

        m = re.match(regex, s, re.DOTALL)
        if m:
            return float(m.group(1).replace(',', '.'))
        else:
            return 0

    def dolar(self):
        return self.__get_cotacao('http://dolarhoje.com/')

    def euro(self):
        return self.__get_cotacao('http://eurohoje.com/')


start_receiver()
exit(0)
