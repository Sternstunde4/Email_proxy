import socket
import base64
import ssl
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ssl import SSLContext
import os

Contacts = []
Drafts = []
Sent = []
Trash = []


def contacts():
    if (len(Contacts) == 0):
        print("There is nothing here!")
    else:
        for i in range(len(Contacts)):
            print("Contact", i+1, '\t')
            print(Contacts[i], '\n')


def sent():
    if (len(Sent) == 0):
        print("There is nothing here!")
    else:
        for i in range(len(Sent)):
            print("Sent Email\t", i+1, '\t')
            print(Sent[i], '\n')
    print("Whether to delete?Y/N")
    op3 = input()
    if(op3 == 'Y'):
        num = input("Email to delete:")
        num = int(num)
        Trash.append(Sent[num-1])
        Sent.pop(num-1)


def drafts():
    if (len(Drafts) == 0):
        print("There is nothing here!")
    else:
        for i in range(len(Drafts)):
            print("Draft\t", i+1, '\t')
            print(Drafts[i], '\n')
    print("Whether to delete?Y/N")
    op3 = input()
    if (op3 == 'Y'):
        num = input("Email to delete:")
        num = int(num)
        Trash.append(Sent[num - 1])
        Sent.pop(num - 1)


def trash():
    if (len(Trash) == 0):
        print("There is nothing here!")
    else:
        for i in range(len(Trash)):
            print("Trash\t", i+1, '\t')
            print(Trash[i], '\n')


def send():
    msg = "\r\n I love computer networks!"
    endMsg = "\r\n.\r\n"
    # 选择QQ邮件服务器
    mailServer = "smtp.qq.com"
    # 发送方地址和接收方地址
    fromAddress = "2917837989@qq.com"
    n = input("Number of recipient:")
    n = int(n)
    toAddress = [0 for i in range(n)]
    for i in range(n):
        toAddress[i] = input("Recipient" + str(i + 1) + ":")
        Contacts.append(toAddress[i])  # 发送过邮件的接收方都列入通讯录
    # 发送方，验证信息，由于邮箱输入信息会使用base64编码，因此需要进行编码
    username = "2917837989@qq.com"  # 输入自己的用户名对应的编码
    password = "llnnipaikvbbddge"  # 开启SMTP服务时的授权码
    login_username = base64.b64encode(username.encode()).decode() + '\r\n'
    login_password = base64.b64encode(password.encode()).decode() + '\r\n'

    # 创建客户端套接字socket并建立TCP连接
    serverPort = 465  # SMTP使用587号端口
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket = SSLContext(ssl.PROTOCOL_TLS).wrap_socket(clientSocket)
    clientSocket.connect((mailServer, serverPort))  # connect只能接收一个参数
    # 从客户套接字中接收信息
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if '220' != recv[:3]:
        print('220 reply not received from server.')

    # 发送 HELO 命令并且打印服务端回复
    # 开始与服务器的交互，服务器将返回状态码250,说明请求动作正确完成
    heloCommand = 'HELO Christine\r\n'
    clientSocket.send(heloCommand.encode())  # 随时注意对信息编码和解码
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)
    if '250' != recv1[:3]:
        print('250 reply not received from server.')

    # 发送"AUTH LOGIN"命令，验证身份.服务器将返回状态码334（服务器等待用户输入验证信息）
    loginCommand = 'AUTH LOGIN\r\n'
    clientSocket.sendall(loginCommand.encode())
    recv2 = clientSocket.recv(1024).decode()
    print(recv2)
    if '334' != recv2[:3]:
        print('334 reply not received from server.')

    # 发送验证信息,若权限验证失败，返回535
    clientSocket.sendall(login_username.encode())
    recvName = clientSocket.recv(1024).decode()
    print(recvName)
    if '535' == recvName[:3]:
        print('535 Login username wrong')

    clientSocket.sendall(login_password.encode())
    recvPass = clientSocket.recv(1024).decode()
    print(recvPass)
    # 如果用户验证成功，服务器将返回状态码235
    if '235' != recvPass[:3]:
        print('235 reply not received from server')

    # TLS加密，将应用层的报文进行加密后再交由TCP进行传输
    temp = 'STARTTLS\r\n'
    print(temp)
    clientSocket.send(temp.encode())
    recv = clientSocket.recv(1024).decode()
    print(recv)

    # 再次发送 HELO 命令并且打印服务端回复，服务器忘记了在STARTTLS之前发生的任何事情
    # 开始与服务器的交互，服务器将返回状态码250,说明请求动作正确完成
    heloCommand = 'HELO Christine\r\n'
    clientSocket.send(heloCommand.encode())  # 随时注意对信息编码和解码
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)
    if '250' != recv1[:3]:
        print('250 reply not received from server.')

    for i in range(n):
        # TCP连接建立好之后，通过用户验证就可以开始发送邮件。邮件的传送从MAIL命令开始，MAIL命令后面附上发件人的地址。
        # 发送 MAIL FROM 命令，并包含发件人邮箱地址
        mailFrom = 'MAIL FROM: <' + fromAddress + '>\r\n'
        clientSocket.sendall(mailFrom.encode())
        recvFrom = clientSocket.recv(1024).decode()
        print(recvFrom)
        if '250' != recvFrom[:3]:
            print('250 reply not received from server')  # SMTP服务器已准备好接收邮件
        # 接着SMTP客户端发送一个或多个（单发或群发）RCPT (收件人recipient)命令，格式为RCPT TO: <收件人地址>。
        # 发送 RCPT TO 命令，并包含收件人邮箱地址，返回状态码 250（要求的邮件操作已完成）
        rcptTo = 'RCPT TO: <' + toAddress[i] + '>\r\n'
        clientSocket.sendall(rcptTo.encode())
        recvTo = clientSocket.recv(1024).decode()  # 注意TCP使用sendall和recv,UDP使用sendto，recvfrom
        print(recvTo)
        if '250' != recvTo[:3]:
            print('250 reply not received from server')  # SMTP服务器有这个用户
        op4 = int(input("which type of message do you want to send?1.text\t2.image attachment\t3.text attachment"))
        if (op4 == 1):
            # 编辑邮件信息，发送数据
            subject = "I love computer networks!"
            contentType = "text/plain"
            message1 = 'from:' + fromAddress + '\r\n'
            message1 += 'to:' + toAddress[i] + '\r\n'
            message1 += 'subject:' + subject + '\r\n'
            message1 += 'Content-Type:' + contentType + '\t\n'
            message1 += '\r\n' + msg
            print("Are you sure to send it to", toAddress[i], "?Y/N")
            sendOrNot = input()
            if (sendOrNot == 'Y'):
                flag = 0
                for j in range(len(Contacts)):
                    if (toAddress[i] == Contacts[j]):  # 若通讯录中已有该接收者则不再重复添加
                        flag = 1
                if (flag == 0): Contacts.append(toAddress[i])  # 发送过邮件的接收者都列入通讯录
                # 发送 DATA 命令，表示即将发送邮件内容。服务器将返回状态码354（开始邮件输入，以"."结束）
                data = 'DATA\r\n'
                clientSocket.send(data.encode())
                recvData = clientSocket.recv(1024).decode()
                print(recvData)
                if '354' != recvData[:3]:
                    print('354 reply not received from server')  # SMTP服务器同意传输
                Sent.append(message1)  # 已发送的邮件加入Sent
                clientSocket.sendall(message1.encode())
                # 以"."结束。请求成功返回 250
                clientSocket.sendall(endMsg.encode())
                recvEnd = clientSocket.recv(1024).decode()
                print(recvEnd)
                if '250' != recvEnd[:3]:
                    print('250 reply not received from server')
            else:  # 未发送的邮件进入Drafts
                Drafts.append(message1)
        elif(op4 == 2):
            subject = 'This is a image attachment test!'
            message2 = MIMEMultipart()
            message2['Subject'] = subject
            message2['From'] = fromAddress
            message2['To'] = toAddress[i]
            message2.attach(MIMEText('Image of Fudan is attached', 'plain', 'utf-8'))
            # 创建图片附件
            img_file = open(os.getcwd() + "/Fudan.png", 'rb').read()
            msg_img = MIMEImage(img_file)
            msg_img.add_header('Content-Disposition', 'attachment', filename="Fudan.png")
            msg_img.add_header('Content-ID', '<0>')
            message2.attach(msg_img)
            print("Are you sure to send it to", toAddress[i], "?Y/N")
            sendOrNot = input()
            if (sendOrNot == 'Y'):
                flag = 0
                for j in range(len(Contacts)):
                    if (toAddress[i] == Contacts[j]):  # 若通讯录中已有该接收者则不再重复添加
                        flag = 1
                if (flag == 0): Contacts.append(toAddress[i])  # 发送过邮件的接收者都列入通讯录
                # 发送 DATA 命令，表示即将发送邮件内容。服务器将返回状态码354（开始邮件输入，以"."结束）
                data = 'DATA\r\n'
                clientSocket.send(data.encode())
                recvData = clientSocket.recv(1024).decode()
                print(recvData)
                if '354' != recvData[:3]:
                    print('354 reply not received from server')  # SMTP服务器同意传输
                Sent.append(message2)  # 已发送的邮件加入Sent
                clientSocket.sendall(message2.as_string().encode())
                # 以"."结束。请求成功返回 250
                clientSocket.sendall(endMsg.encode())
                recvEnd = clientSocket.recv(1024).decode()
                print(recvEnd)
                if '250' != recvEnd[:3]:
                    print('250 reply not received from server')
            else:  # 未发送的邮件进入Drafts
                Drafts.append(message2)
        else:
            subject = 'This is a text attachment test!'
            message3 = MIMEMultipart()
            message3['Subject'] = subject
            message3['From'] = fromAddress
            message3['To'] = toAddress[i]
            message3.attach(MIMEText('A txt file is attached', 'plain', 'utf-8'))
            # 创建txt附件
            filename = 'test.txt'
            with open(filename, 'rb') as f:
                attachfile = MIMEApplication(f.read())
            attachfile.add_header('Content-Disposition', 'attachment', filename=filename)
            message3.attach(attachfile)
            print("Are you sure to send it to", toAddress[i], "?Y/N")
            sendOrNot = input()
            if (sendOrNot == 'Y'):
                flag = 0
                for j in range(len(Contacts)):
                    if (toAddress[i] == Contacts[j]):  # 若通讯录中已有该接收者则不再重复添加
                        flag = 1
                if (flag == 0): Contacts.append(toAddress[i])  # 发送过邮件的接收者都列入通讯录
                # 发送 DATA 命令，表示即将发送邮件内容。服务器将返回状态码354（开始邮件输入，以"."结束）
                data = 'DATA\r\n'
                clientSocket.send(data.encode())
                recvData = clientSocket.recv(1024).decode()
                print(recvData)
                if '354' != recvData[:3]:
                    print('354 reply not received from server')  # SMTP服务器同意传输
                Sent.append(message3)  # 已发送的邮件加入Sent
                clientSocket.sendall(message3.as_string().encode())
                # 以"."结束。请求成功返回 250
                clientSocket.sendall(endMsg.encode())
                recvEnd = clientSocket.recv(1024).decode()
                print(recvEnd)
                if '250' != recvEnd[:3]:
                    print('250 reply not received from server')
            else:  # 未发送的邮件进入Drafts
                Drafts.append(message3)


    # 发送"QUIT"命令，断开和邮件服务器的连接
    quit = 'QUIT\r\n'
    clientSocket.sendall(quit.encode())
    recvQuit = clientSocket.recv(1024).decode()
    print(recvQuit)
    if '221' != recvQuit[:3]:
        print('221 reply not received from server.')
    clientSocket.close()


def home():
    print("What do you want to do?")
    options = ["Send", "Trash", "Drafts", "Sent", "Contacts"]
    for i in range(5):
        print(i+1, options[i], '\t')
    op = input("Your option:")
    op = int(op)
    if op == 1:
        send()
    elif op == 2:
        trash()
    elif op == 3:
        drafts()
    elif op == 4:
        sent()
    else:
        contacts()
    print("What do you want to do next?\n")
    print("1.back to home\t2.leave\n")
    op1 = input()
    op1 = int(op1)
    if op1 == 1:
        home()
    else:
        print("Goodbye Christine!")


print("welcome Christine!\n")
home()
