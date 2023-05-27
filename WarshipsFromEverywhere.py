import socket
import time
import os

os.chdir(os.path.split(os.path.realpath(__file__))[0])

config_file = open("configs")
config = eval("".join(config_file.readlines()))
# print(config)
SERVER_ADDRESS = (config["IP"], config["HOST"])

while True:
    # 创建 TCP 客户端套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # 尝试连接到服务器
        client_socket.connect(SERVER_ADDRESS)
        print(f"Connected to server {SERVER_ADDRESS}")
        break
    except Exception as e:
        print(e)
        print("Failed to connect to the server, retry in 5 seconds...")
        time.sleep(5)
# 登陆
for i in range(3):
    ipt = input(client_socket.recv(1024).decode('utf-8')).encode('utf-8')
    if not ipt:
        print("Good bye")
        client_socket.close()
        exit()
    client_socket.sendall(ipt)
print(client_socket.recv(1024).decode('utf-8'))
try:
    client_socket.sendall(b"__KICKED__")
    client_socket.recv(1024)
# except Exception as e:
except OSError:
    # print(e)
    client_socket.close()
    exit()

# 不断从标准输入读取用户输入并发送给服务器
while True:
    message = input(client_socket.recv(1024).decode('utf-8'))
    if not message:
        print("Good bye")
        break
    try:
        # 发送数据到服务器
        client_socket.sendall(message.encode('utf-8'))
        # 接收服务器返回的数据并打印
        data = client_socket.recv(1024)
        print(data.decode('utf-8'))
        client_socket.sendall(b'Null')
        insider_data = client_socket.recv(1024)
        client_socket.sendall(insider_data)
        if insider_data == b"__KEEP_WAITING__":
            data = client_socket.recv(1024)  # Waiting for matching
            print(data.decode('utf-8'))
            data = client_socket.recv(1024)  # Matching finished
            print(data.decode('utf-8'))
    except socket.error as e:
        print("Socket error:", e)
        break
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        break

# 关闭客户端套接字
client_socket.close()
