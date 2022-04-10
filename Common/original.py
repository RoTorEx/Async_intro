import socket  # Пара через которую осуществляется взаимодедйствие между клинетом и сервером


'''Запускаем скрипт имитируя сервер. Через команду "nc localhost 5001" подключаемся к серверу имитируя клиент.
При наличии более одного клиента сервер будет рабоать только с первым подключившимся клиентом клиентом,
потому что запираемся внутри цикла, и прибив первого клиента идёт переход на уровень выше и приём от второго клиента'''


# Будет обслуживать запросы клиента
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Поддержка протокола TCP
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Переиспользование адреса True (1)
server_socket.bind(('localhost', 5001))  # Указываем домен и порт
server_socket.listen()  # Прослушиваем буфер на предмет входящх подключений

while True:
    print("Before .accept()")
    client_socket, addr = server_socket.accept()  # Блокирующая функция
    print("Connection from", addr)

    while True:
        print("Before .recv()")
        request = client_socket.recv(4096)

        if not request:
            break
        else:
            response = "Hello world\n".encode()
            client_socket.send(response)

    print("Outside inner while loop")
    client_socket.close()
