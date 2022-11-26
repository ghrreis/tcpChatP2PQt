from PyQt5.QtWidgets import *
from PyQt5 import uic
import socket
import random
import time
import threading

# name = StringVar()  # Variável para receber o nome do usuário


class WinChat(QMainWindow):

    port = random.randint(10000, 11000)  # Gera um valor aleatório entre 10.000 e 11.000 que será utilizado para criar porta de conexão entre os peers
    ip = "0.0.0.0"  # Aceita conexão de qualquer origem
    target_port = 9999  # Porta de conexão com o servidor
    target_host = ""  # Variável para guardar o endereço do servidor que possui os usuários on-line

    def __init__(self, trgtHost):

        super(WinChat, self).__init__()
        uic.loadUi("winChat.ui", self)
        self.show()
        self.pbSendName.clicked.connect(lambda: self.__cmdSendName(self.leName.text()))
        self.pbSendMessage.clicked.connect(lambda: self.__cmdSendMsg(self.lwOnlineUsers.currentItem().text()))
        # self.lwOnlineUsers.itemClicked.connect(lambda: self.__cmdSendMsg(self.lwOnlineUsers.currentItem().text()))

        self.target_host = trgtHost # Recebe IP do servidor passado como parâmetro para buscar a lista de usuários on-line
        print(self.target_host)
        # Cria uma thread passando como parâmetros a função handleRequestUsers
        client_handler = threading.Thread(target=self.__handleRequestUsers)
        client_handler.start()  # Inicia a thread

        # Cria uma thread passando como parâmetros a função peerServer
        peerS = threading.Thread(target=self.__peerServer)
        peerS.start()  # Inicia a thread


    def message(self, txt):
        msg = QMessageBox()
        msg.setText(txt)
        msg.exec_()

    # Função para enviar (cadastrar) o nome, IP e porta do peer no servidor que possui a lista de usuários online
    def __cmdSendName(self, name):
        # Cria socket utilizando protocolo IPv4 e protocolo TCP
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Conecta a um socket remoto (servidor) passando os parâmetros host, porta
        client.connect((self.target_host, self.target_port))
        # Envia conjunto de bytes (mensagens) para o socket remoto (servidor)
        client.send(str.encode("0:"+name+":"+str(self.port)))

    # Função para requisitar ao servidor a lista de usuários online
    def __handleRequestUsers(self):
        while True:
            time.sleep(10)  # Faz a requisição a cada 30s
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria socket utilizando protocolo IPv4 e protocolo TCP
            client.connect((self.target_host, self.target_port))  # Conecta a um socket remoto (servidor) passando os parâmetros host, porta
            client.send(str.encode("1:"))  # Envia conjunto de bytes (mensagens) para o socket remoto (servidor)
            request = client.recv(8192)  # Recebe a lista de usuários online
            listUsers = str(request, "utf-8").split("@")  # Separa a lista de usuários que estão concatenados pelo @
            print(listUsers)  # Imprime a lista de usuários
            self.lwOnlineUsers.clear()
            for user in listUsers:  # Laço para armazenar a nova lista de usuários online
                if user != "":
                    # Adiciona cada usuário online no final da Listbox
                    self.lwOnlineUsers.addItem(user)

    # Função para criar servidor que receberá msgs dos peers
    def __peerServer(self):
        global messagePeer  # Variável para receber a mensagem de um peer
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria socket utilizando protocolo IPv4 e protocolo TCP
        server.bind((self.ip, self.port))  # Atribui ao socket endereço e porta de conexão
        server.listen(5)  # Define que o servidor está pronto para receber conexões com no máximo 5
        print("[*] Listening on", self.ip, ":", self.port)  # Imprime os endereços IP e Porta que o servidor está sendo executado

        while True:
            # Bloqueia o serviço até receber um pedido de conexão com os valores de conexão (socket cliente) e endereço
            client, addr = server.accept()
            print("[*] Accepted connection from:", addr[0], ":", addr[1])  # Imprime os endereços IP e Porta respectivamente
            request = client.recv(8192)  # Recebe dados do socket remoto em um determinado tamanho de buffer
            self.lwReceivedMessages.addItem(str(request, "utf-8").split(":")[0])  # Atribui a msg recebida de um peer lwReceivedMessages
            client.close()  # Fecha conexão com o peer

    # Função para enviar msg ao peer selecionado na Listbox de usuários online
    def __cmdSendMsg(self, selection):
        dstIP = str(selection).split(":")[1]  # Atribui o endereço IP do peer remoto à variável dstIP
        dstPort = str(selection).split(":")[2]  # Atribui a porta do peer remoto à variável dstPort
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria socket utilizando protocolo IPv4 e protocolo TCP
        client.connect((dstIP, int(dstPort)))  # Conecta a um socket remoto (peer) passando os parâmetros host, porta
        client.send(str.encode(self.leName.text() + " -> " + self.leMessage.text()))  # Envia conjunto de bytes (mensagens) para o socket remoto (peer)
