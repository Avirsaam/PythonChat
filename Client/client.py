import socket
import sys
import select
from time import sleep

if len(sys.argv) != 3:
	print ("Введите, IP address, port number в качестве параметров")
	exit()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_IP_address = str(sys.argv[1])
server_listening_port = int(sys.argv[2])
server.connect((server_IP_address, server_listening_port))

while True:
    
	sleep(0.05);
	# содержит список всех потоков ввода
	input_streams = [sys.stdin, server]

	
	#select.select возвращает поток готовый для чтения из переданного списка потоков
    #если это сокет - то печатаем сообщение от сервера,
    #если это консоль - то отправляем сообщение на сервер

    
	read_ready,write_ready, error_thrown = select.select(input_streams,[],[])

	for socks in read_ready:
		if socks == server:
			message = socks.recv(2048)
			print (message.decode())
		else:
			message = sys.stdin.readline()
			server.send(message.encode())
			sys.stdout.write("<You>")
			sys.stdout.write(message)
			sys.stdout.flush()
server.close()
