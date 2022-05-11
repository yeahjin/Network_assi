from socket import *
import sys

input_para = sys.argv[1]

serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('',int(input_para)))

serverSocket.listen(1)
print ('The server is ready to receive')

while True:
	connectionSocket, addr = serverSocket.accept()
	recv_socket = ""
	al = []
	cnt = 0
	header_field = 0
	while True:
		sentence = connectionSocket.recv(1)
		if len(sentence) < 1:
			break
		cnt += 1
		if sentence.decode() == "\n":
			header_field += 1
		if cnt <= 4:
			al.append(sentence.decode())
			recv_socket += sentence.decode()
		else:
			al[0], al[1], al[2] = al[1], al[2], al[3]
			al[3] = sentence.decode()
			recv_socket += sentence.decode()
		if al[0] == "\r" and al[1] == '\n' and al[2] == "\r" and al[3] == "\n":
			break
	print(recv_socket)
	filename = recv_socket.split()[1]
	try:
		f = open(filename[1:],'r')
	except FileNotFoundError as e:
		response_message = "HTTP/1.0 404 NOT FOUND\r\nConnection: close\r\nContext-Length: 0\r\nContent-Type: text/html\r\n\r\n"
		connectionSocket.send(response_message.encode())
		print("Server Error : No such file", filename)
	else:
		file_data = f.read()
		f.close()

		response_message = "HTTP/1.0 200 OK\r\nConnection: close\r\nContext-Length: "
		response_message += str(len(file_data))
		response_message += "\r\nContent-Type: text/html\r\n\r\n"

		connectionSocket.send(response_message.encode())
		encode_file = file_data.encode()
		print("header field: %d" %(header_field-2))
		if len(file_data) == len(encode_file):
			print("finish %d %d" % (len(file_data), len(encode_file)))
		connectionSocket.send(encode_file)
		connectionSocket.close()