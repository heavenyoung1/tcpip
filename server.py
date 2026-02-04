import socket
import sys

HOST = '192.168.31.194'
PORT=65432

# Создаём TCP сокет
# socket.AF_INET - используем IPv4
# socket.SOCK_STREAM - TCP протокол (для UDP было бы SOCK_DGRAM)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Опция SO_REUSEADDR позволяет быстро перезапускать сервер
# Без неё пришлось бы ждать ~1 минуту после закрытия
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


try:
    # Привязываем сокет к адресу и порту
    server_socket.bind((HOST, PORT))
    print(f'Сервер запущен на {HOST}:{PORT}')

    # Переводим сокет в режим прослушивания
    # Параметр 5 - максимальная очередь ожидающих подключений
    server_socket.listen(5)
    print('[*] Ожидание подключений...')

    while True:
        # accept() блокирует выполнение до прихода нового подключения
        # Возвращает новый сокет для общения с клиентом и адрес клиента
        client_socket, client_address = server_socket.accept()
        print(f'[+] Подключился клиент: {client_address}')

        try:
            while True:
                # Получаем данные от клиента (максимум 1024 байта за раз)
                data = client_socket.recv(1024)

                if not data:
                    print(f'[-] Клиент {client_address} отключился')
                    break

                # Декодируем полученные байты в строку
                message = data.decode('utf-8')
                print(f'[<] Получено от {client_address}: {message}')

                client_socket.sendall(data)
                print(f'[>] Отправлено обратно: {message}')

        except Exception as e:
            print(f'[!] Ошибка при работе с клиентом: {e}')
        finally:
            # Закрываем соединение с клиентом
            client_socket.close()
            
except KeyboardInterrupt:
    print('\n[*] Сервер остановлен пользователем')
except Exception as e:
    print(f'[!] Ошибка сервера: {e}')
finally:
    # Закрываем серверный сокет
    server_socket.close()
    print('[*] Сервер завершил работу')