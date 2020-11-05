import argparse
import os
import socket
import threading
import file_handling

parser = argparse.ArgumentParser()
# verify correct working base directory is provided Or raises NotADirectoryError


def file_path(string):
    if os.path.isfile(string):
        return string
    else:
        raise argparse.ArgumentTypeError(
            "{0} file does not exist".format(string))


# command line command to run it : server.py -n 4  -p 10002 10003 10004 10005 -i 2
parser.add_argument("-i", "--status_interval", metavar="Reporting Interval", type=int,
                    required=True,  help="Time interval For server status reporting in seconds E.g 5(seconds)")
parser.add_argument("-n", "--num_servers", type=int, choices=range(1, 5),
                    required=True, help="Total number of virtual servers E.g 4")
parser.add_argument("-f", "--output_file_path", type=file_path,
                    default=os.getcwd(),  help="Address to the file location that client will download")
parser.add_argument("-p", "--server_ports", metavar="", type=int, nargs="*", required=True,
                    help="(‘n’ port numbers, one for each server max=4) E.g 101 102 103 104")

# Although it verifiees input type we still need to convert it into int for usage
args = parser.parse_args()
if len(args.server_ports) != int(args.num_servers):
    raise Exception('The number of ports {} not equal num of servers {} '.format(
        args.server_ports, args.num_servers))

"""                        To test argparse module
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
FILE = args.output_file_path
#FILE = 'video.mp4'
# we can make it dynamic by first receiving filename from client and respond if it exists!

''' 
It sends the Msg-length and then message  
'''


def simpleSend(conn, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)
    return ''


''' This function is invoked whenever a client connects & sends the requested bytes'''


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            # Length Empty String/Byte_array of length L
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                continue
            if msg[:14] == "Receving File":
                with open(FILE) as file:
                    size = os.path.getsize(FILE)
                    # Size in bytes
                    msg = "filesize "+str(size)
                    # sending file size to connected client
                    simpleSend(conn, msg)
                # here we are receiving the byte range required by client
                    msg_length = conn.recv(HEADER).decode(FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = conn.recv(msg_length).decode(FORMAT)
                    msg = msg.split()
                    msg[0] = int(msg[0])
                    msg[1] = int(msg[1])
                    # received message is a string msg[0] start and msg[1] represent end of byte range
                    data = file_handling.get_file_part(FILE, msg[0], msg[1])
                    endPoint = msg[1] - msg[0]
                    # sending the requested byte range
                    i = 0
                    readSize = 1024
                    while (i < endPoint):
                        sendd = data[i:i + readSize] if (i+readSize <
                                                         endPoint) else data[i:endPoint]
                        conn.send(sendd)
                        i += 1024
                    connected = False
            # disconnect message
            # msg = conn.recv(HEADER).decode(FORMAT)
            # msg_length = int(msg)
            # msg = conn.recv(msg_length).decode(FORMAT)
            # print(f"[{addr}] {msg}")

    conn.close()
    return ''


# keeps track of threads sending data
threads = []


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
        threads.append(thread)


def start():
    for i in NO_OF_PORTS:
        thread = threading.Thread(target=startserver, args=(SERVER, i))
        thread.start()
        # threads.append(thread)
    return ''


# makes sure started threads completes their task
for t in threads:
    t.join()

print("[STARTING] .....")
print("Server IP " + socket.gethostbyname(socket.gethostname()))
if __name__ == "__main__":
    start()
