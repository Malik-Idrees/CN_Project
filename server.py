import argparse
import os
import socket
import threading
import file_handling

parser = argparse.ArgumentParser()
# verify correct working base directory is provided Or raises NotADirectoryError


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


# command line command to run it : python sample.py -i 5 -n 2 -f 4 -p 100 101 102
parser.add_argument("-i", "--status_interval", metavar="Reporting Interval", type=int,
                    required=True,  help="Time interval For server status reporting in seconds E.g 5(seconds)")
parser.add_argument("-n", "--num_servers", type=int, choices=range(1, 5),
                    required=True, help="Total number of virtual servers E.g 4")
parser.add_argument("-f", "--base_directory", type=dir_path,
                    default=os.getcwd(),  help="Address pointing to the file location")
parser.add_argument("-p", "--server_ports", metavar="", type=int, nargs="*", required=True,
                    help="(‘n’ port numbers, one for each server max=4) E.g 101 102 103 104")

# Although it verifiees input type we still need to convert it into int for usage
args = parser.parse_args()
print(type(args.server_ports))
if len(args.server_ports) != int(args.num_servers):
    raise Exception('The number of ports {} not equal num of servers {} '.format(
        args.server_ports, args.num_servers))

"""
for a in args.__dict__:
        print(str(a) + ": " + str(args.__dict__[a]))
        print("Ports number accessed by variable name ports :{}" .format(
            args.server_ports))
"""

'''
Handling server actionss
'''
HEADER = 8192
NO_OF_PORTS = args.server_ports
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"
FILE = 'code.txt'
# we can make it dynamic by first receiving filename from client and respond if it exists
''' simply sending the data it is passed down '''


def simpleSend(conn, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)
    return ''


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            # print(str(int(msg_length)) + "Length of ifrst message received bu server")#msg is an empty string/byte_array of some length
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                continue
            if msg[:14] == "Receving File":
                with open(FILE) as file:
                    size = os.path.getsize(FILE)
                    # print(size)  # size = os.path.getsize(file) #in bytes
                    msg = "filesize "+str(size)
                    simpleSend(conn, msg)
                    msg_length = conn.recv(HEADER).decode(FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = conn.recv(msg_length).decode(FORMAT)
                    msg = msg.split()

                    # print(type(msg))...its a list
                    data = file_handling.get_file_part(FILE, msg[0], msg[1])
                    print(len(data))
                    endPoint = int(msg[1]) - int(msg[0])
                    i = 0
                    while (i < endPoint):
                        # send_length = str(msg_length).encode(FORMAT)
                        # send_length += b' ' * (HEADER - len(send_length))
                        sendd = data[i:i + 1024] if (i+1024 <
                                                     endPoint) else data[i:endPoint]
                        print(sendd)
                        # conn.send(data[i:i + 1024]) if (i+1024 < endPoint) else conn.send(data[i:endPoint])
                        conn.send(sendd)
                        i += 1024
                        print(f"{addr} sending")
                    # simpleSend(conn, data)
                    connected = False
                    # conn.close()

            # else:
            #     print(f"[{addr}] {msg}")
            #     print("error sending file")
            #     conn.send("error sending indexed data".encode(FORMAT))

            # msg = conn.recv(HEADER).decode(FORMAT)
            # msg_length = int(msg)
            # msg = conn.recv(msg_length).decode(FORMAT)
            # print(f"[{addr}] {msg}")
    print("ending12")
    conn.close()
    return ''


def startserver(SERVER, PORT):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ADDR = (SERVER, PORT)
    server.bind(ADDR)
   # print(f"[LISTENING] Server is listening on {SERVER} port {PORT}")
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
       # print(
        # f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1} for {PORT} ")


threads = []


def start():
    for i in NO_OF_PORTS:
       # print("hehe" + str(threading.activeCount()))
        thread = threading.Thread(target=startserver, args=(SERVER, i))
        thread.start()
        threads.append(thread)
    return ''


for t in threads:
    t.join()
    print("Closing.....")

print("[STARTING] server is starting...")
if __name__ == "__main__":
    start()
