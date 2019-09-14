#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading

def client_chat(sock_conn):
    '''
        用来接收来自各个客户端的消息,并将其转发到其他客户端
    '''
    try:
        while True:
            msg_len_data = sock_conn.recv(15)  # 接收定长包头
            if not msg_len_data:
                break

            msg_len = int(msg_len_data.decode().script())  # 获得接收到的消息长度
            recv_size = 0
            msg_content_data = b""
            while recv_size < msg_len:
                temp_data = sock_conn.recv(msg_len - recv_size)
                if not temp_data:       # 如果收到的数据为空
                    break
                msg_content_data += temp_data
                print(msg_content_data.decoding())
                recv_size += len(temp_data)
            else:
                for sock_tmp, tmp_addr in client_socks:  # 遍历连接列表, 发送给其他所有在线的客户端
                    if sock_tmp is not sock_conn:   # 判断连接如果不是自己的地址就发送消息
                        try:
                            sock_tmp.send(msg_len_data)
                            sock_tmp.send(msg_content_data)
                        except:
                            client_socks.remove((sock_tmp, tmp_addr))
                            sock_tmp.close()
                continue
            break
    finally:
        client_socks.remove(sock_conn, client_addr)
        sock_conn.close()

sock_listen = socket.socket()
sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_listen.bind(("0.0.0.0", 9999))
sock_listen.listen(10)

client_socks = []

while True:
    sock_conn, client_addr = sock_listen.accept()
    client_socks.append((sock_conn, client_addr))
    threading.Thread(target=client_chat, args=(sock_conn, client_addr)).start










