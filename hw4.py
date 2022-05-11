import socket
import sys
import threading
import time
import select
import signal


def send(sock):
    while True:
        print(user_name + ">")
        sendMsg = input()

        if sendMsg == "@quit":
            sock.send(user_name.encode() + " : ".encode() + sendMsg.encode())
            sock.close()
            break
        sock.send(user_name.encode() + " : ".encode() + sendMsg.encode())


def receive(sock):
    while True:
        recvMsg = sock.recv(1024)
        msg = recvMsg.decode()
        if "@quit" in msg:
            break
        print(msg)


if __name__ == '__main__':
    server_port = int(sys.argv[1])
    user_name = sys.argv[2]
    server_host = '127.0.0.1'
    print(user_name + ">")
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((server_host,server_port))
    server_sock.listen(1)

    wait_list = [server_sock,sys.stdin]
    read_ready, write_ready, error_ready = select.select(wait_list, [], [])

    for distinguish_server in read_ready:
        if distinguish_server == server_sock:
            connectionSocket, addr = server_sock.accept()
            print('connection from host %s, port%s, socket %s' % (addr[0],addr[1],connectionSocket.fileno()))
            signal.signal(signal.SIGPIPE, signal.SIG_IGN)

            sender = threading.Thread(target=send, args=(connectionSocket,))
            receiver = threading.Thread(target=receive, args=(connectionSocket,))

            sender.setDaemon(True)
            receiver.setDaemon(True)
            sender.start()
            receiver.start()

            while True:
                time.sleep(1)
                if sender.is_alive() == False:
                    break
                if receiver.is_alive() == False:
                    print('Connection Closed : %d' % (connectionSocket.fileno()))
                    break

        else:
            client_input = input()
            client_inputList = client_input.split(' ')
            client_Port = int(client_inputList[2])
            client_host = client_inputList[1]

            clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientsock.connect((client_host,client_Port))

            sender = threading.Thread(target=send, args=(clientsock,))
            receiver = threading.Thread(target=receive, args=(clientsock,))
            sender.setDaemon(True)
            receiver.setDaemon(True)
            sender.start()
            receiver.start()


            while True:
                time.sleep(1)
                if receiver.is_alive() == False:
                    break
                if sender.is_alive() == False:
                    breaker = False
                    break