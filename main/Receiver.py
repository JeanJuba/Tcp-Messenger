import socket
import time


def start_receiver():
    host = socket.gethostname()
    port = 8899

    s = socket.socket()#socket.AF_INET, socket.SOCK_STREAM)
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

        time.sleep(1)
        print('looping...')

    conn.close()


def decode_command(user_command):
    print('command received: ', user_command)
    return{
        '\server': socket.gethostname(),
        '\dev': "Jean Juba"
    }.get(user_command, "Not Found")


#print(decode_command('\dev'))
start_receiver()
exit(0)