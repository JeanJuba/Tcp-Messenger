import socket
from tkinter import *


class GUI:

    def __init__(self):
        self.root = None
        self.text_field = None
        self.text_box = None
        self.server_field = None

    def init_gui_tkinter(self):
        '''
        Define a interface gráfica
        :return:
        '''

        self.root = Tk()
        self.root.title('Graphic Interface')
        rw = 800
        rh = 330
        sw = self.root.winfo_screenmmwidth()
        sh = self.root.winfo_screenmmheight()

        x = int((sw/2) - (rw/2))
        y = int((sh/2) - (rh/2))
        print("sw: %d  sh: %d  x: %d  y: %d" % (sw, sh, x, y))
        self.root.geometry("{}x{}+{}+{}".format(rw, rh, x, y))

        top_frame = Frame(self.root, width=800, height=30)
        top_frame.pack(fill=X)
        Label(top_frame, text='Command: ').grid(row=0, column=0)
        self.text_field = Entry(top_frame)
        self.text_field.grid(row=0, column=1)
        self.text_field.bind('<Return>', self.enter_pressed)
        Button(top_frame, command=self.button_click, text='Send').grid(row=0, column=2)
        Label(top_frame, text='Server').grid(row=0, column=3)
        self.server_field = Entry(top_frame)
        self.server_field.grid(row=0, column=4)

        bottom_frame = Frame(self.root, width=400, height=300)
        bottom_frame.pack(fill=BOTH)
        bottom_frame['bg'] = 'blue'

        self.text_box = Text(bottom_frame)
        self.text_box.pack(fill=BOTH)
        self.root.mainloop()

    def enter_pressed(self, event):
        text = self.text_field.get()
        self.add_to_text_box(text, self.start_messenger(text))

    def button_click(self):
        command = self.text_field.get()
        if not command:
            self.add_to_text_box("Comando inválido: ", "Favor inserir um comando válido")
            return
        elif command[1:] == 'exit':
            exit()

        self.add_to_text_box(command, self.start_messenger(command))

    def add_to_text_box(self, command, answer):
        '''
        Adiciona as mensagens para a caixa de texto
        '''

        self.text_box.insert(END, "{}: {}\n".format(command, answer))

    def start_messenger(self, arg):
        '''
        Inicia a conexão com o IP informado na interface gráfica usando
        a porta 8899 e enviando a mensagem digitada.
        :param arg:
        :return:
        '''

        host = self.server_field.get()
        if not host:
            return "Inform the server IP"

        port = 8899
        #self.add_to_text_box('', "Creating socket")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.add_to_text_box('', "Socket created")
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.settimeout(10)
            #self.add_to_text_box('', "Connecting to {} on port {}".format(host, port))
            s.connect((host, port))
            #self.add_to_text_box('', "connected")
            s.settimeout(None)
        except socket.error as e:
            return "Connection error. Check if server is running: {}".format(e)

        #self.add_to_text_box('', "sending")
        s.sendall(bytes(arg, encoding='UTF-8'))
        #self.add_to_text_box('', "sent")
        #self.add_to_text_box('', "receiving")
        data = s.recv(1024)
        #self.add_to_text_box('', "received")
        s.close()
        answer = data.decode('utf-8')
        print('Answer: ', answer)

        return answer


gui = GUI()
gui.init_gui_tkinter()
