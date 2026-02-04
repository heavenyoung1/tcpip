import socket
import sys

HOST = '127.0.0.1'
PORT=65432

# Создаём TCP сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Подключаемся к серверу
    # Здесь происходит TCP three-way handshake (SYN, SYN-ACK, ACK)
    # Вот тут ничего не понятно что это -> TCP three-way handshake (SYN, SYN-ACK, ACK)
    print(f'[*] Подключение к серверу {HOST}:{PORT}...')
    client_socket.connect((HOST, PORT))
    print('[+] Успешно подключено!')

    while True:
        # Читаем сообщение от пользователя
        message = input('\nВведите сообщение (или "quit" для выхода): ')

        if message.lower() == 'quit':
            print('[*] Завершение работы...')
            break

        # Отправляем сообщение серверу
        # encode() преобразует строку в байты
        client_socket.sendall(message.encode('utf-8'))
        print(f'[>] Отправлено: {message}')

        # Получаем ответ от сервера
        data = client_socket.recv(1024)
        response = data.decode('utf-8')
        print(f'[<] Получен ответ: {response}')
        
except ConnectionRefusedError:
    print('[!] Ошибка: сервер не доступен. Убедитесь что сервер запущен.')
except Exception as e:
    print(f'[!] Ошибка: {e}')
finally:
    # Закрываем соединение
    # Здесь происходит TCP connection termination (FIN, ACK, FIN, ACK)
    client_socket.close()
    print('[*] Соединение закрыто')



