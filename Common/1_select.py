import socket  # Пара через которую осуществляется взаимодедйствие между клинетом и сервером
from select import select

from nbformat import read  # Системая функция которая смотрит изменения состатония переданных файловых объектов


'''В unix системах всё является файлами, так же как всё объектами в Python. То есть от флешки до часов – всё файлы'''

'''Обеспечиваем низкую связанность и управления двумя функциями происходит в event_loop. Теперь код асинхронный.
Две рабочие функции стали независимыми и их можно вызывать в любом порядке, когда это необходимо.
Вызвом этих функций управляет event_loop().

Функция select делает выборку из списков на предмет готовы ли объекты, либо нет.
Если они готовы, то создаются соответствующие списки. То есть мы прокручиваем список готовых объектов.
Если это серверный сокет, то передаём на подключение, если клиентский – то передаём в send_message

Асинхронность без event_loop() невозможна, но и остальная программа должна быть спроектирована правильным образом'''


# Переменная мониторинга
to_monitor = []

# Определение серверного сокете. Будет обслуживать запросы клиента
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Поддержка протокола TCP
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Переиспользование адреса True (1)
server_socket.bind(('localhost', 5001))  # Указываем домен и порт
server_socket.listen()  # Прослушиваем буфер на предмет входящх подключений


# Функция принятия соединения, они будет принимать socket. Серверный socket
def accept_connection(server_socket):

    print("Before .accept()")  # Метка
    client_socket, addr = server_socket.accept()  # Блокирующая функция
    print("Connection from", addr)

    to_monitor.append(client_socket)


# Функция получения от пользователя и отправка ему сообщений
def send_message(client_socket):

    print("Before .recv()")  # Метка
    request = client_socket.recv(4096)

    if request:
        response = "Hello world\n".encode()
        client_socket.send(response)
    else:
        print("Outside inner while loop\n")  # Метка
        client_socket.close()


# Функция распределяющий механиз, которая будет определять и вызывать готовые сокеты
def event_loop():

    while True:
        '''В функцию fileno() передаётся 3 списка:
        объекты за коториыми нужно наблюдать, когда они станут достпны для чтения;
        -//-, когда они доступны для записи;
        -//-, у которых мы ожидаем какие-то ошибки.
        Возвращает те же объекты, когда они станут доступны'''

        # Мониторим список доступных объектов для чтения и две буферные переменные которые не нужны (на запись и ошибки)
        ready_to_read, _, _ = select(to_monitor, [], [])  # read, write, errors

        # Обработка списка с объектами, как только они появляются
        for sock in ready_to_read:
            # Если сокет является серверным, то вызываем accept_connection и передаём сокет, элемент списка
            if sock is server_socket:
                accept_connection(sock)
            else:
                send_message(sock)


if __name__ == '__main__':
    to_monitor.append(server_socket)
    event_loop()
