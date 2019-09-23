#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
import user_reg_login
import json

def user_service_thread(sock_conn, client_addr):
    '''
    函数功能:用来处理各个用户的登录注册请求
    '''
    try:
        while True:
            data_len = sock_conn.recv(15).decode().rstrip()
            if len(data_len) > 0:
                data_len = int(data_len)

                recv_size = 0
                json_data = b""
                while recv_size < data_len:
                    tmp = sock_conn.recv(data_len - recv_size)
                    if not tmp:
                        break
                    json_data += tmp
                    recv_size += len(tmp)
                
                json_data = json_data.decode()
                req = json.loads(json_data)

                if req["op"] == 1:
                    # 登录校验
                    rsp = {"op": 1, "error_code": 0}

                    if not user_reg_login.check_user_name(req["args"]["uname"]):
                        rsp["error_code"] = 1
                    
                    rsp = json.dumps(rsp).encode()
                    data_len = "{:<15}".format(len(rsp)).encode()
                    sock_conn.send(data_len)
                    sock_conn.send(rsp)
                    
                elif req["op"] == 2:
                    # 用户注册
                    rsp = {"op": 2, "error_code": 0}
                    if not user_reg_login.user_reg(req["args"]["uname"], req["args"]["password"], req["args"]["phone"], req["args"]["email"]):
                        # 注册失败
                        rsp["error_code"] = 1

                    rsp = json.dumps(rsp).encode()
                    data_len = "{:<15}".format(len(rsp)).encode()
                    sock_conn.send(data_len)
                    sock_conn.send(rsp)                       

                # elif req["op"] == 3:
                #     # 校验用户名是否存在
                #     rsp = {"op": 3, "error_code": 0}

                #     ret = user_reg_login.check_user_name(req["args"]["uname"])
                #     if ret == 2:
                #         rsp["error_code"] = 1
                    
                #     rsp = json.dumps(rsp).encode()
                #     data_len = "{:<15}".format(len(rsp)).encode()
                #     sock_conn.send(data_len)
                #     sock_conn.send(rsp)            
            else:
                break
    finally:
        sock_conn.close()

           
def client_chat(sock_conn, client_addr):
    '''
        用来接收来自各个客户端的消息,并将其转发到其他客户端
    '''
    try:
        while True:
            msg_len_data = sock_conn.recv(15)  # 接收定长包头
            if not msg_len_data:
                break

            msg_len = int(msg_len_data.decode().rstrip())  # 获得接收到的消息长度
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
        client_socks.remove((sock_conn, client_addr))
        sock_conn.close()


sock_listen1 = socket.socket()    # 创建响应登录注册的套接字
sock_listen1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_listen1.bind(("127.0.0.1", 9999))
sock_listen1.listen(10)

client_socks = []

while True:
    sock_conn, client_addr = sock_listen1.accept()
    client_socks.append((sock_conn, client_addr))
    threading.Thread(target=user_service_thread, args=(sock_conn,client_addr)).start()
    threading.Thread(target=client_chat, args=(sock_conn, client_addr)).start()








