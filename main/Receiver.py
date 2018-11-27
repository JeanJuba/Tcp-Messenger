import socket
import datetime
import sys
sys.path.append('/home/jean/Área de Trabalho/Python/TcpMessenger')
from main.Currency import Cotacao
from main import Location


def start_receiver():
    host = socket.gethostname()
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
    return Location.get_location()


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


start_receiver()
exit(0)
