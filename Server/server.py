# Python program to implement server side of chat room.
import socket
import _thread
import signal


server_listening_port = 55005
server_listening_ip = "" #слушаем на всех интерфейсах
listening_address = (server_listening_ip, server_listening_port)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server = socket.create_server(listening_address)

server.listen(100)

list_of_clients = []
list_of_threads = []

def clientthread(conn, addr):
	conn.send(("Hello! Добро пожаловать в чат, ваш IP:" + addr[0]).encode())

	while True:
			try:
				message = conn.recv(2048).decode()
				if message:
					print (addr[0] + " says: " + message)

					# вызываем функцию бродкаста чтобы отправить
					# сообщение всем
					message_to_send = addr[0] + ": " + message
					broadcast(message_to_send.encode(), conn)

				else:
					#если ТСР разрывается  то сообщение пустое
					remove(conn)
					print (addr[0] + " disconnected")
					break;

			except:
				continue


def broadcast(message, connection):
	for client in list_of_clients:
		if client!=connection:
			try:
				client.send(message)
			except:
				client.close()
				remove(client)


def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)

while True:
	#принимаем входящее сооединение,
	#conn - хранит сокет
	#addr[0] - адрес
	#addr[1] - номер порта
	conn, addr = server.accept()

	#добавляем сокет вновьподключенного клиента в список по которому
	#будет идти бродкаст сообщений
	list_of_clients.append(conn)


	print (addr[0] + " connected")
	

	# создаем отдельный процесс для прослушки новых сообщений
	# на данном сокете
	th = _thread.start_new_thread(clientthread,(conn,addr))
	

conn.close()
server.close()
