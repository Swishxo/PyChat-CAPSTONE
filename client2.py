"""
This is a client # 2
"""


import socket
import threading
import tkinter
from tkinter import simpledialog
from tkinter import scrolledtext

PORT = 8380
SERVER = "192.168.1.221"
ADDRESS = (SERVER, PORT)


class Client:

    def __init__(self, host, port):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        # message box
        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring("Username", "Enter a username", parent=msg)

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.guiloop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def guiloop(self):
            self.win = tkinter.Tk()

            self.chat_label = tkinter.Label(self.win, text="chat")
            self.chat_label.config(font=("Times", 14))
            self.chat_label.pack()

            # text scrolls down like a chat box
            self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
            self.text_area.pack()
            # stop user from directly entering text in window
            self.text_area.config(state='disable')

            self.msg_label = tkinter.Label(self.win, text="Message: ")
            self.msg_label.config(font=("Times", 14))
            self.msg_label.pack()

            self.input_area = tkinter.Text(self.win)
            self.input_area.pack()

            self.send_button = tkinter.Button(self.win, text="SEND", command=self.write)
            self.send_button.config(font=("Arial", 12))
            self.send_button.pack()

            self.gui_done = True

            self.win.protocol("WM_DELETE_WINDOW", self.stop)

            self.win.mainloop()


    # close window
    def stop(self):
        self.running = False
        self.win.destroy()
        self.win.close()
        exit(0)

    # send message
    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    # receive messages
    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024)
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("error")
                self.sock.close()
                break


client = Client(SERVER, PORT)



