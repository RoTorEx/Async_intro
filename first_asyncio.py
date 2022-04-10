import asyncio
from time import sleep


async def f():  # Функция асинхронная
    while True:
        print("f() func")
        await asyncio.sleep(5)  # спим 2 секунд


async def g():
    while True:
        print("g() func")
        await asyncio.sleep(2)  # спим 2 секунд
        print("Done...\n")
    # yield from -> await
    # await g_help()
    # print(g_help())


# async def main():
#     '''Тут мы создали подзадачи, как оыбчные функции, а для верной асинхронности нужно создавать таски'''
#     await g()  # Функции должны быть асинхронными, функция g() тут сопрограмма
#     await f()  # Запускает функции и ждёт результата


async def main():
    '''При такой структуре мы имеем две задача, а не задачу g() в задачи main().
    Но без блокирующей функции функция g() не выведет g_function(), для этого нужнен метод run_forever.
    Без него отработает функция main() и завершится программа'''
    main_loop.create_task(g())  # Создадим таск g()
    main_loop.create_task(g())  # Создадим таск f()
    # await f()  # Тут f() это подзадача


'''Пока main работает, мы запускаем g(), идём в g() выполянем какой-то код,
потом запускаем функцию f(). Принцип выполения как и у обычных функций'''
main_loop = asyncio.get_event_loop()  # Создаёт новый или берёт существующий
main_loop.run_until_complete(main())
main_loop.run_forever()  # Для реализации второго принта в g(), то есть для завершения всех активных задач

# main_loop = asyncio.new_event_loop()  # Создаёт новый event loop
# main_loop = asyncio.get_event_loop()  # Создаёт новый или берёт существующий
# main_loop.run_until_complete(main())  # Функция запускает задачу и event loop рабоатет пока не выполнит задачу
# main_loop.run_forever()  # Блокирующая функция для циклов, цикл будет бесконечным
# main_loop.run_in_executor()  # Функция для потоков
