import socket
import multiprocessing
import time
import random
import logging

# Налаштовуємо логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[logging.StreamHandler()]
)

# Серверний процес
def server_process():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 65432))
    server_socket.listen(1)
    logging.info("Сервер запущений і чекає на підключення...")

    conn, addr = server_socket.accept()
    logging.info(f"Підключено до клієнта: {addr}")

    message_count = 0
    while True:
        data = conn.recv(1024)
        if not data:
            logging.info("Клієнт закрив з'єднання.")
            break
        message_count += 1
        received_message = data.decode('utf-8')
        logging.info(f"Сервер отримав: {received_message}")

        # Формуємо відповідь
        response = f"Сервер отримав ваше повідомлення #{message_count}: {received_message}"
        conn.sendall(response.encode('utf-8'))
        time.sleep(random.uniform(0.5, 1.5))  # Випадкова затримка для імітації мережі

    conn.close()
    server_socket.close()
    logging.info("Сервер завершив роботу.")

# Клієнтський процес
def client_process(message_count=5):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    time.sleep(1)  # Чекаємо, поки сервер запуститься
    client_socket.connect(('127.0.0.1', 65432))
    logging.info("Клієнт підключився до сервера.")

    for i in range(message_count):
        message = f"Повідомлення {i + 1} від клієнта"
        logging.info(f"Клієнт надсилає: {message}")
        client_socket.sendall(message.encode('utf-8'))
        data = client_socket.recv(1024)
        logging.info(f"Клієнт отримав: {data.decode('utf-8')}")
        time.sleep(random.uniform(0.5, 1.0))  # Випадкова затримка між повідомленнями

    client_socket.close()
    logging.info("Клієнт завершив роботу.")

# Головна функція
if __name__ == "__main__":
    message_count = 5  # Кількість повідомлень для обміну
    logging.info(f"Запускаємо обмін з {message_count} повідомленнями.")

    # Створюємо процеси
    server = multiprocessing.Process(target=server_process)
    client = multiprocessing.Process(target=client_process, args=(message_count,))

    # Запускаємо процеси
    server.start()
    client.start()

    # Чекаємо завершення процесів
    server.join()
    client.join()
