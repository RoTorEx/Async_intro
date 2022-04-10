import socket  # Пара через которую осуществляется взаимодедйствие между клинетом и сервером


'''Этот файл никак не отличается от original.py, всё выполняется синхронно.
Этот скрипт с самого начала спроектирован как синхронный'''

'''Чтобы сделать этот код асинхронным, необходимо его переделать, чтобы все функции стали независимыми.
Чтобы каждую из них в любом порядке можно было вызвать тогда, когда мы этого захотим.
Необходимо уменьшить их связанность.'''

# Определение серверного сокете. Будет обслуживать запросы клиента
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Поддержка протокола TCP
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Переиспользование адреса True (1)
server_socket.bind(('localhost', 5001))  # Указываем домен и порт
server_socket.listen()  # Прослушиваем буфер на предмет входящх подключений


# Функция принятия соединения, они будет принимать socket
def accept_connection(server_socket):

    while True:
        print("Before .accept()")  # Метка
        client_socket, addr = server_socket.accept()  # Блокирующая функция
        print("Connection from", addr)
        send_message(client_socket)  # Передача socket'а


# Функция получения от пользователя и отправка ему сообщений
def send_message(client_socket):

    while True:
        print("Before .recv()")  # Метка
        request = client_socket.recv(4096)

        if not request:
            break
        else:
            response = "Hello world\n".encode()
            client_socket.send(response)

    print("Outside inner while loop\n")  # Метка
    client_socket.close()


if __name__ == '__main__':
    accept_connection(server_socket)
