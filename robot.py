#O funcionamento do robô é muito parecido com o do cliente humano,
#a diferênça é que ele toma uma ação automaticamente depois de receber uma mensagem





import tkinter as tk
from tkinter import messagebox
import socket
import threading

window = tk.Tk()
window.title("Robo")
username = "Robo" ##Aqui você coloca o nome de usuário


topFrame = tk.Frame(window)
lblName = tk.Label(topFrame, text = "Nome:").pack(side=tk.LEFT)
entName = tk.Entry(topFrame)
entName.pack(side=tk.LEFT)
btnConnect = tk.Button(topFrame, text="Conectar", command=lambda : connect())
btnConnect.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP)

displayFrame = tk.Frame(window)
lblLine = tk.Label(displayFrame, text="Dê um nome ao seu Robo").pack()
bottomFrame = tk.Frame(window)
tkMessage = tk.Text(bottomFrame, height=2, width=55)
tkMessage.bind("<Return>", (lambda event: getChatMessage(tkMessage.get("1.0", tk.END))))
bottomFrame.pack(side=tk.BOTTOM)

# network client
client = None
HOST_ADDR = "127.0.0.1" ##Aqui é o ip do servidor
HOST_PORT = 8080 ##Aqui é a porta em que você quer que o serviço rode

def connect(): ##Diferente do cliente humano, não precisamos tratar o nome de usuário do robô pois ele será sempre o mesmo
    global username, client
    connect_to_server(username)


def connect_to_server(name): #Esta é a função que conecta ao servidor, não precisa mexer nada aqui
    global client, HOST_PORT, HOST_ADDR
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST_ADDR, HOST_PORT))
        client.send(name.encode()) # Send name to server after connecting

        entName.config(state=tk.DISABLED)
        btnConnect.config(state=tk.DISABLED)
        tkMessage.config(state=tk.NORMAL)

        # start a thread to keep receiving message from server
        # do not block the main thread :)
        threading._start_new_thread(receive_message_from_server, (client, "m"))
    except Exception as e:
        tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + HOST_ADDR + " on port: " + str(HOST_PORT) + " Server may be Unavailable. Try again later")


def receive_message_from_server(sck, m): #Esta é a função que recebe as mensagens do servidor
    while True:
        #Coloque o funcionamento do robô a partir daqui
        from_server = sck.recv(4096).decode() #Assim como no cliente humano, a mensagem é recebida e é gravada como uma string

        if not from_server: break #Tratamento de erros

        if("pedra" in from_server):
            send_mssage_to_server("PAPEL ")
        if("papel" in from_server):
            send_mssage_to_server("TESOURA ")
        if("tesoura" in from_server):
            send_mssage_to_server("PEDRA ")

        #PARE === Este é o limite do funcionamento do robô === PARE
    sck.close()
    window.destroy()


def getChatMessage(msg):

    msg = msg.replace('\n', '')

    send_mssage_to_server(msg)



def send_mssage_to_server(msg):
    client_msg = str(msg)
    client.send(client_msg.encode())
    if msg == "exit":
        client.close()
        window.destroy()
    print("Sending message")


window.mainloop()
