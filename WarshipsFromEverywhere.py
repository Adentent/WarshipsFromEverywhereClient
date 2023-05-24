import socket
import time

config_file = open("configs")
config = eval("".join(config_file.readlines()))
print(config)
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
client_socket.sendall(input(client_socket.recv(1024).decode('utf-8')).encode('utf-8'))
client_socket.sendall(input(client_socket.recv(1024).decode('utf-8')).encode('utf-8'))
client_socket.sendall(input(client_socket.recv(1024).decode('utf-8')).encode('utf-8'))
print(client_socket.recv(1024).decode('utf-8'))
# FIXME: 被踢出后还可再发送一条消息
#        解决方案: 直接向服务器验证可用性(1.发送一个请求;2.使用现有函数)

# 不断从标准输入读取用户输入并发送给服务器
while True:
    message = input("Enter message to send: ")
    if not message:
        break
    try:
        # 发送数据到服务器
        client_socket.sendall(message.encode('utf-8'))
        # 接收服务器返回的数据并打印出来
        data = client_socket.recv(1024)
        print(f"Received {data.decode('utf-8')}")
    except socket.error as e:
        print("Socket error:", e)
        break
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        break

# 关闭客户端套接字
client_socket.close()
