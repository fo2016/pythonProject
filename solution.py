from socket import *


def smtp_client(port=1025, mailserver='127.0.0.1'):
    msg = "\r\n My message"
    endmsg = "\r\n.\r\n"

    # Choose a mail server (e.g. Google mail server) if you want to verify the script beyond GradeScope

    # Create socket called clientSocket and establish a TCP connection with mailserver and port

    # Fill in start
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((mailserver, port))

    # Fill in end

    recv = clientSocket.recv(1024).decode()
    # print(recv)

    if recv[:3] != '220':
        print('220 reply not received from server.')

    # Send HELO command and print server response.
    heloCommand = 'HELO Alice\r\n'
    clientSocket.send(heloCommand.encode())
    recv1 = clientSocket.recv(1024).decode()

    if recv1[:3] != '250':
        print('250 reply not received from server.')

    # Send MAIL FROM command and print server response.
    # Fill in start
    mailfrom = "MAIL FROM: <fantortiz@gmail.com>\r\n"
    clientSocket.send(mailfrom.encode())
    recv2 = clientSocket.recv(1024).decode()
    # print(recv2)
    # Fill in end

    # Send RCPT TO command and print server response.
    # Fill in start
    mailto = "RCPT TO: <felix.ortiz@faosystems.com>\r\n"
    clientSocket.send(mailto.encode())
    recv3 = clientSocket.recv(1024).decode()
    # print(recv3)
    # Fill in end

    # Send DATA command and print server response.
    # Fill in start
    data = "DATA\r\n"
    clientSocket.send(data.encode())
    recv4 = clientSocket.recv(1024).decode()
    # print(recv4)
    # Fill in end

    # Send message data.
    # Fill in start
    msg = "Hello, this is a reminder that your vacation date is fast approaching.\r\n"
    clientSocket.send(msg.encode())
    # Fill in end

    # Message ends with a single period.
    # Fill in start
    msg = "\r\n.\r\n"
    clientSocket.send(msg.encode())
    recv5 = clientSocket.recv(1024).decode()
    # print(recv5)
    # Fill in end

    # Send QUIT command and get server response.
    # Fill in start
    msg = "QUIT\r\n"
    clientSocket.send(msg.encode())
    recv6 = clientSocket.recv(1024).decode()
    # print(recv6)
    # Fill in end


if __name__ == '__main__':
    smtp_client(1025, '127.0.0.1')