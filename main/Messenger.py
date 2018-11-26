import socket
from tkinter import *


class GUI:

    def __init__(self):
        self.root = None
        self.text_field = None
        self.text_box = None

    def init_gui_tkinter(self):
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
            return
        elif command == '\exit':
            exit()

        self.add_to_text_box(command, self.start_messenger(command))

    def add_to_text_box(self, command, answer):
        self.text_box.insert(END, "{}: {}\n".format(command, answer))

    def start_messenger(self, arg):
        host = socket.gethostname()
        port = 8899
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((host, port))
        except socket.error:
            return "Connection error. Check if server is running."

        s.sendall(bytes(arg, encoding='UTF-8'))
        data = s.recv(1024)
        s.close()
        answer = data.decode('utf-8')
        print('Answer: ', answer)

        return answer


gui = GUI()
gui.init_gui_tkinter()
