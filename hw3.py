from socket import *
import select
import sys

serverPort = sys.argv[1]
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('',int(serverPort)))

serverSocket.listen(8)
print ('The server is ready to receive')
socketDescriptor = []
serverlist = [serverSocket]
while True:
	try:
		read_ready, write_ready, error_ready = select.select(serverlist, [], [])

		for connect_sckt in read_ready:
			# 새롭게 접속
			if connect_sckt == serverSocket:
				connectionSocket, addr = serverSocket.accept()
				socketDescriptor.append(serverSocket.fileno())
				serverlist.append(connectionSocket)
				print("connection from host %s, port %d, socket %d" %(addr[0],addr[1],connectionSocket.fileno()))

			# 접속된 클라이언트에겍 데이터 받음
			else:
				data = connect_sckt.recv(1024)
				if len(data) > 0: # data가 있으면
					for socketInList in serverlist:
						if socketInList != serverSocket and socketInList != connect_sckt:
							socketInList.send(data)

				else:
					print("Connection Closed %d" %(connect_sckt.fileno()))
					serverlist.remove(connect_sckt)
					connect_sckt.close()
	except KeyboardInterrupt:
		serverSocket.close()

