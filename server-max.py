import socket
import select
import time

import users_db

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

ADDR = "127.0.0.1", 1234

server_socket.bind(ADDR)
server_socket.listen()
server_socket.setblocking(False)  # Делаем серверный сокет неблокирующим

# sockets_list = [server_socket]

# not_registred_clients: list[tuple: str, int] = []
# clients: dict[str, dict[str, str]] = {}

all_users: dict[int: dict[str, str]] = {}
active_sessions: dict[socket.socket, int] = {}

def add_user():



def new_connect(server_socket):
    client_socket, client_address = server_socket.accept()
    client_socket.setblocking(False)
    sockets_list.append(client_socket)
    not_registred_clients.append(client_address)
    return client_address



print(f"[SERVER] Чат-сервер запущен на {ADDR[0]}:{ADDR[1]}")

while True:
    readable, _, _ = select.select(sockets_list, [], [], 0)

    for notified_socket in readable:
        
        # новое подключение
        if notified_socket == server_socket:
            client_address = new_connect(server_socket)
            print(f"[SERVER] Новое подключение с адреса {client_address}")

        # сообщение
        else:
            raw_data = notified_socket.recv(1024)
            
            # leave
            if not raw_data:
                nickname = clients.get(notified_socket, "Аноним")
                print(f"[SERVER] Пользователь {nickname} покинул чат.")    
                sockets_list.remove(notified_socket)
                # if notified_socket in clients_names:
                    # del clients_names[notified_socket]
                notified_socket.close()
                continue

            message = raw_data.decode("utf-8").strip()

            # чат
            if notified_socket in clients:
                nickname = clients[notified_socket]
                formatted_message = f"{nickname}: {message}"
                print(f"[CHAT] {formatted_message}")
                for client_socket in clients:
                    if client_socket != notified_socket:
                        client_socket.sendall((formatted_message).encode("utf-8"))

            # регистрация
            else:
                clients[notified_socket] = message
                print(f"[SERVER] Клиент {notified_socket.getpeername()} установил ник: {message}")
                welcome_msg = f"[СЕРВЕР]: {message} вошел в чат!"
                for client in clients:
                    if client != notified_socket:
                        client.sendall(welcome_msg.encode("utf-8"))

    time.sleep(0.1)
