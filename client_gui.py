import tkinter as tk
from tkinter import messagebox
import socket
import threading

window = tk.Tk()
window.title("Cliente")
username = ""

#Aqui você monta a interface de usuário, preste atenção pois o programa simplesmente não funciona sem algumas linhas que estão aqui

topFrame = tk.Frame(window)
lblName = tk.Label(topFrame, text = "Nome:").pack(side=tk.LEFT)
entName = tk.Entry(topFrame)
entName.pack(side=tk.LEFT)
btnConnect = tk.Button(topFrame, text="Conectar", command=lambda : connect())
btnConnect.pack(side=tk.LEFT)
#btnConnect.bind('<Button-1>', connect)
topFrame.pack(side=tk.TOP)

displayFrame = tk.Frame(window)
lblLine = tk.Label(displayFrame, text="------------------------ PEDRA x PAPEL x TESOURA ------------------------").pack()
scrollBar = tk.Scrollbar(displayFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(displayFrame, height=20, width=55)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
tkDisplay.tag_config("tag_your_message", foreground="blue")
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
displayFrame.pack(side=tk.TOP)


bottomFrame = tk.Frame(window)
tkMessage = tk.Text(bottomFrame, height=2, width=55)
tkMessage.pack(side=tk.LEFT, padx=(5, 13), pady=(5, 10))
tkMessage.config(highlightbackground="grey", state="disabled")
tkMessage.bind("<Return>", (lambda event: getChatMessage(tkMessage.get("1.0", tk.END))))
bottomFrame.pack(side=tk.BOTTOM)


def connect():
    global username, client
    if len(entName.get()) < 1:
        tk.messagebox.showerror(title="ERRO!!!", message="Digite seu nome <p. ex. Mario>")
    else:
        username = entName.get()
        connect_to_server(username)


# network client
#Aqui você coloca as mesmas informações que estao nas variaveis de mesmo nome no servidor
client = None
HOST_ADDR = "127.0.0.1"
HOST_PORT = 8080

def connect_to_server(name): ##Esta é a função de conexão, não precisa mudar nada
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
        tk.messagebox.showerror(title="ERRO!!!", message="Não foi possível conectar no host: " + HOST_ADDR + " ona porta: " + str(HOST_PORT) + " Servidor desativado. Tente mais tarde.")


def receive_message_from_server(sck, m): #Esta função serve para tratar as mensagens recebidas do servidor
    while True:
        from_server = sck.recv(4096).decode() #<== A mensagem é recebida aqui, perceba que ela é gravada como uma string na variavel from_server

        if not from_server: break

        # display message from server on the chat window

        # enable the display area and insert the text and then disable.
        # why? Apparently, tkinter does not allow us insert into a disabled Text widget :(
        texts = tkDisplay.get("1.0", tk.END).strip()
        tkDisplay.config(state=tk.NORMAL)
        if len(texts) < 1:
            tkDisplay.insert(tk.END, from_server)
        else:
            tkDisplay.insert(tk.END, "\n\n"+ from_server)

        tkDisplay.config(state=tk.DISABLED)
        tkDisplay.see(tk.END)

        # print("Server says: " +from_server)

    sck.close()
    window.destroy()


def getChatMessage(msg): #Esta função serve para preparar a mensagem que você escreveu na text box para enviar para o servidor

    msg = msg.replace('\n', '')
    texts = tkDisplay.get("1.0", tk.END).strip()

    # enable the display area and insert the text and then disable.
    # why? Apparently, tkinter does not allow use insert into a disabled Text widget :(
    tkDisplay.config(state=tk.NORMAL)
    if len(texts) < 1:
        tkDisplay.insert(tk.END, "Você->" + msg, "tag_your_message") # no line
    else:
        tkDisplay.insert(tk.END, "\n\n" + "You->" + msg, "tag_your_message")

    tkDisplay.config(state=tk.DISABLED)

    send_mssage_to_server(msg) #<== A mensagem é enviada para o servidor aqui

    tkDisplay.see(tk.END)
    tkMessage.delete('1.0', tk.END)


def send_mssage_to_server(msg): #Esta é a função que envia a mensagem para o servidor
    client_msg = str(msg)
    client.send(client_msg.encode()) #<== A Mensagem é enviada aqui
    if msg == "exit":
        client.close()
        window.destroy()
    print("Sending message")


window.mainloop()
