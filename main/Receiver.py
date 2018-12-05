import sys
import os
sys.path.append(os.getcwd())
import geocoder
import socket
import datetime


import urllib.request as req
import re



def start_receiver():
    host = socket.gethostname()
    host = socket.gethostbyname(host)
    port = 8899

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))

    print('host: %s  port: %s' % (host, port))

    s.listen(1)

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


def decode_command(user_command):
    print('command received: ', user_command)
    return{
        '\ip': socket.gethostbyname(socket.gethostname()),
        '\dev': "Jean Juba",
        '\dolar': get_dolar(),
        '\euro': get_euro(),
        '\location': get_location(),
        '\\time': datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')
    }.get(user_command, "Not Found")


class Cotacao:

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

    def libra(self):
        return self.__get_cotacao('http://librahoje.com/')


start_receiver()
exit(0)
