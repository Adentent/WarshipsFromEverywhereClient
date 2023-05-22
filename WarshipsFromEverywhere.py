# TODO: 进入先登录
# TODO: 服务端处理数据功能完善

from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
from queue import Queue


request_queue = Queue()
configs_file = open("configs")
configs = eval("".join(configs_file.readlines()))
# print(configs) # examples -> 'IP': 'localhost'


def mainThread():
    while True:
        request = input(">>> ")
        request_queue.put(request)
        request_queue.join()
        if not request:
            while True:
                if request_queue.get() == "__STOP_FINISH__":
                    request_queue.task_done()
                    return


def tcpConnectionThread():
    tcp_socket = socket(AF_INET, SOCK_STREAM)
    server_addr = (configs['IP'], configs['HOST'])
    tcp_socket.connect(server_addr)
    while True:
        send_data = request_queue.get()
        tcp_socket.send(send_data.encode('utf-8'))
        recv_data = tcp_socket.recv(1024)
        if not send_data:
            request_queue.task_done()
            break
        print(recv_data.decode('utf-8'))
        request_queue.task_done()
    tcp_socket.close()
    request_queue.put("__STOP_FINISH__")
    request_queue.join()
    return


if __name__ == "__main__":
    main = Thread(target=mainThread, name='main')
    connection = Thread(target=tcpConnectionThread, name='connection')
    main.start()
    connection.start()
