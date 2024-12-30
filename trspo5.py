import socket
import multiprocessing
import time

# Серверний процес
def server_process():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 65432))
    server_socket.listen(1)
    print("Сервер запущений і чекає на підключення...")

    conn, addr = server_socket.accept()
    print(f"Підключено до клієнта: {addr}")

    for _ in range(5):  # Сервер отримує і відповідає 5 разів
        data = conn.recv(1024)
        if not data:
            break
        print(f"Сервер отримав: {data.decode('utf-8')}")
        response = f"Сервер отримав ваше повідомлення: {data.decode('utf-8')}"
        conn.sendall(response.encode('utf-8'))
        time.sleep(1)  # Імітація затримки відповіді

    conn.close()
    server_socket.close()
    print("Сервер завершив роботу.")

# Клієнтський процес
def client_process():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    time.sleep(1)  # Чекаємо, поки сервер запуститься
    client_socket.connect(('127.0.0.1', 65432))
    print("Клієнт підключився до сервера.")

    for i in range(5):  # Клієнт відправляє 5 повідомлень
        message = f"Повідомлення {i+1} від клієнта"
        print(f"Клієнт надсилає: {message}")
        client_socket.sendall(message.encode('utf-8'))
        data = client_socket.recv(1024)
        print(f"Клієнт отримав: {data.decode('utf-8')}")
        time.sleep(1)  # Затримка між повідомленнями

    client_socket.close()
    print("Клієнт завершив роботу.")

# Головна функція
if __name__ == "__main__":
    # Створюємо процеси
    server = multiprocessing.Process(target=server_process)
    client = multiprocessing.Process(target=client_process)

    # Запускаємо процеси
    server.start()
    client.start()

    # Чекаємо завершення процесів
    server.join()
    client.join()
