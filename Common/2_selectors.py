import socket  # Пара через которую осуществляется взаимодедйствие между клинетом и сервером
import selectors


'''В итерпритаторе пишем: selectors.DefaultSelector() и получаем нашу
функцию для работы <selectors.KqueueSelector at 0x1070ff100>

Регистриуем сокеты вместе с сопровождающими данными. Использовали два компонента сокеты и связанные с ним функции
В event_loop получаем какой то кортеж для работы данных'''


selector = selectors.DefaultSelector()


# Определение серверного сокете. Будет обслуживать запросы клиента
def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Поддержка протокола TCP
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Переиспользование адреса True (1)
    server_socket.bind(('localhost', 5001))  # Указываем домен и порт
    server_socket.listen()  # Прослушиваем буфер на предмет входящх подключений

    # Функция register принимает 3 аругмента: серверный сокет, events, любые связанные данные, тут объект функции
    selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connection)


# Функция принятия соединения, они будет принимать socket. Серверный socket
def accept_connection(server_socket):

    client_socket, addr = server_socket.accept()  # Блокирующая функция
    print("Connection from", addr)
    selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=send_message)


# Функция получения от пользователя и отправка ему сообщений
def send_message(client_socket):

    request = client_socket.recv(4096)

    if request:
        response = "Hello world\n".encode()
        client_socket.send(response)
    else:
        selector.unregister(client_socket)
        # print("Outside inner while loop\n")  # Метка
        client_socket.close()


# Функция распределяющий механиз, которая будет определять и вызывать готовые сокеты
def event_loop():

    while True:

        events = selector.select()  # (key, events)

        # SelectroKey
        # fileobj
        # events
        # data

        for key, _ in events:
            callback = key.data
            callback(key.fileobj)


if __name__ == '__main__':
    server()
    event_loop()
