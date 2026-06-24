import socket
import select
import sys
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

SERVER_ADDR = "127.0.0.1", 1234

try:
    client.connect(SERVER_ADDR)
    print("[ЧАТ] Успешное подключение!")
except ConnectionRefusedError:
    print("[ОШИБКА] Сервер не запущен.")
    exit()

client.setblocking(False)

while True:
    readable, _, _ = select.select([client, sys.stdin], [], [], 0)

    for obj in readable:
        
        if obj == client:
            raw_data = client.recv(1024)
            if not raw_data:
                print("\n[ЧАТ] Соединение с сервером потеряно.")
                exit()
            
            print(raw_data.decode("utf-8")) # , end=""


        elif obj == sys.stdin:
            message = sys.stdin.readline()

            if message:
                client.sendall(message.encode("utf-8"))
            else:
                print("[CLIENT] Вы покидаете чат.")
                exit()
    
    time.sleep(0.1)
