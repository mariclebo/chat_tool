#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import socket
import threading
import tkinter as Tk
import tkinter.messagebox
import user_reg_login as jy


def main():
    global sock
    sock = socket.socket()
    sock.connect(("127.0.0.1", 9999))
    try:
        mainWnd = Tk.Tk()

        mainWnd.title("奇迹用户登录")

        mainWnd.geometry("400x300+600+300")   # 定义窗口大小和位置
        # 禁止改变窗口大小
        mainWnd.resizable(width=False, height=False)
        # mainWnd.maxsize(400, 300)
        # mainWnd.minsize(400, 300)
    
        #窗口背景
        canvas = Tk.Canvas(mainWnd, height=400, width=400)
        image_file = Tk.PhotoImage(file=r"C:\\Users\\Administrator\\Desktop\\Python实用工具\\chat_tool\\images\\login_background.gif")
        image = canvas.create_image(0, 0, anchor='nw', image=image_file)
        canvas.pack(side='top')

        # 使用Label方法生成标签
        Tk.Label(mainWnd, text="奇迹之家", bg="pink", fg="green", font=("草书", 18)).place(x=150, y=40)
        Tk.Label(mainWnd, text="用户名:", bg="pink", fg="red", font=("宋体", 15)).place(x=30 , y=100)
        Tk.Label(mainWnd, text="密码:", bg="pink", fg="red", font=("宋体", 15)).place(x=30, y=170)

        # 使用Entry方法生成输入框
        userName_box = Tk.Entry(mainWnd)
        userName_box.place(x=120, y=100, width=230, height=30)

        password_box = Tk.Entry(mainWnd)
        password_box.place(x=120, y=170, width=230, height=30)

        global loginUname, loginpassword
        loginUname = userName_box.get()
        loginpassword = password_box.get()


        # 使用Buttun方法生成按钮
        btnLogin = Tk.Button(mainWnd, text="sign in", command=chat_sign_in_send)
        btnLogin.place(x=160, y=240, width=50)

        btnReg = Tk.Button(mainWnd, text="sign up", command=chat_sign_up)
        btnReg.place(x=260, y=240, width=50)

        mainWnd.mainloop()
    finally:
        mainWnd.destroy()


def chat_sign_up():
    try:
        wind = Tk.Tk()

        wind.title("奇迹用户注册")

        wind.geometry("500x500+550+200")
        wind.resizable(width=False, height=False)

        # canvas = Tk.Canvas(wind, height=2500, width=2500)
        # image_file = Tk.PhotoImage(file="D:\python学习笔记\Python高级\day41\chat_tool\img2.gif")
        # image = canvas.create_image(0, 0, anchor='nw', image=image_file)
        # canvas.pack(side='top')

        Tk.Label(wind, text="用户名:", bg="pink", fg="red", font=("宋体", 15)).place(x=50, y=100)
        Tk.Label(wind, text="密码:", bg="pink", fg="red", font=("宋体", 15)).place(x=50, y=170)
        Tk.Label(wind, text="手机号码:", bg="pink", fg="red", font=("宋体", 15)).place(x=50 , y=240)
        Tk.Label(wind, text="邮箱:", bg="pink", fg="red", font=("宋体", 15)).place(x=50, y=310)

        userName_box = Tk.Entry(wind)
        userName_box.place(x=160, y=100, width=230, height=30)

        password_box = Tk.Entry(wind)
        password_box.place(x=160, y=170, width=230, height=30)

        phone_box = Tk.Entry(wind)
        phone_box.place(x=160, y=240, width=230, height=30)

        email_box = Tk.Entry(wind)
        email_box.place(x=160, y=310, width=230, height=30) 

        global clientUname, clientpassword, clientPhone, clientEmail
        clientUname = userName_box.get()
        clientpassword = password_box.get()
        clientPhone = phone_box.get()
        clientEmail = email_box.get()

        btncommit = Tk.Button(wind, text="sign up", command=chat_sign_up_send)
        btncommit.place(x=240, y=380, width=50)
        wind.mainloop()
    finally:
        wind.destroy()


def chat_frame():
    mainWnd = Tk.Tk()
    mainWnd.title("奇迹之家聊天室")

    global chat_record_box
    chat_record_box = Tk.Text(mainWnd)
    chat_record_box.configure(state=Tk.DISABLED)
    chat_record_box.pack(padx=10, pady=10)

    global chat_msg_box
    chat_msg_box = Tk.Text(mainWnd)
    chat_msg_box.configure(width=65, height=5)
    chat_msg_box.pack(side=Tk.LEFT, padx=10, pady=10)

    send_msg_btn = Tk.Button(mainWnd, text="发 送", command=on_send_msg)
    send_msg_btn.pack(side=Tk.RIGHT, padx=10, pady=10, ipadx=15, ipady=15)
    threading.Thread(target=recv_chat_msg).start()
    mainWnd.mainloop()


def chat_sign_in_send():
    req= {"op":1,"args":{"uname":loginUname,"password":loginpassword}}
    req= json.dumps(req)
    data_top="{:<15}".format(len(req)).encode()
    sock.send(data_top)
    sock.send(req.encode())
    chat_sign_in_recv()


def chat_sign_in_recv():
    data_len = sock.recv(15).decode().rstrip()
    if len(data_len) > 0:
        data_len = int(data_len)

        recv_size = 0
        json_data = b""
        while recv_size < data_len:
            tmp = sock.recv(data_len - recv_size)
            if tmp == 0:
                break
            json_data += tmp
            recv_size += len(tmp)

        json_data = json_data.decode()
        rsp = json.loads(json_data)
        if rsp["error_code"]==0:
            Tk.messagebox.showerror("登录成功!")
            chat_frame()
        else:
            Tk.messagebox.showerror("登录失败!")


def chat_sign_up_send():
    req= {"op":2,"args":{"uname":clientUname,"password":clientpassword,"phone":clientPhone,"email":clientEmail}}
    req= json.dumps(req)
    data_top="{:<15}".format(len(req)).encode()
    sock.send(data_top)
    sock.send(req.encode())
    chat_sign_up_recv()


def chat_sign_up_recv():
    while True:
        data_len = sock.recv(15).decode().rstrip()
        if len(data_len) > 0:
            data_len = int(data_len)

            recv_size = 0
            json_data = b""
            while recv_size < data_len:
                tmp = sock.recv(data_len - recv_size)
                if tmp == 0:
                    break
                json_data += tmp
                recv_size += len(tmp)

            json_data = json_data.decode()
            rsp = json.loads(json_data)
            if rsp["error_code"]==0:
                Tk.messagebox.showerror('注册成功')
                main()
            else:
                Tk.messagebox.showerror('注册失败')


def on_send_msg():
    '''
    函数功能:发送聊天内容
    '''
    nick_name = "qjb"
    chat_msg = chat_msg_box.get(1.0, "end")
    if chat_msg == "\n":
        return

    chat_data = nick_name + ":" + chat_msg
    chat_data = chat_data.encode()
    data_len = "{:<15}".format(len(chat_data)).encode()

    try:
        sock.send(data_len)
        sock.send(chat_data)
    except:
        # sock.close()
        Tk.messagebox.showerror("温馨提示", "发送消息失败，请检查网络连接！")
    else:
        chat_msg_box.delete(1.0, "end")
        chat_record_box.configure(state=Tk.NORMAL)
        chat_record_box.insert("end", chat_data.decode() + "\n")
        chat_record_box.configure(state=Tk.DISABLED)


def recv_chat_msg():
    global sock

    while True:
        try:
            while True:
                msg_len_data = sock.recv(15)
                if not msg_len_data:
                    break

                msg_len = int(msg_len_data.decode().rstrip())
                recv_size = 0
                msg_content_data = b""
                while recv_size < msg_len:
                    tmp_data = sock.recv(msg_len - recv_size)
                    if not tmp_data:
                        break
                    msg_content_data += tmp_data
                    recv_size += len(tmp_data)
                else:
                    # 显示
                    chat_record_box.configure(state=Tk.NORMAL)
                    chat_record_box.insert("end", msg_content_data.decode() + "\n")
                    chat_record_box.configure(state=Tk.DISABLED)
                    continue
                break
        finally:
                sock.close()
                sock = socket.socket()
                sock.connect(("127.0.0.1", 9999))


if __name__ == "__main__":
    main()

