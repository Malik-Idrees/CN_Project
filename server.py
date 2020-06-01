import argparse
import os
import socket 
import threading
import file_handling

parser = argparse.ArgumentParser()
#verify correct working base directory is provided Or raises NotADirectoryError
def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

# command line command to run it : python sample.py -i 5 -n 2 -f 4 -p 100 101 102 
parser.add_argument("-i","--status_interval",metavar="Reporting Interval",type=int,required=True,  help="Time interval For server status reporting in seconds E.g 5(seconds)")
parser.add_argument("-n","--num_servers",type=int,choices=range(1,5),required=True, help="Total number of virtual servers E.g 4")
parser.add_argument("-f","--base_directory",type=dir_path,default= os.getcwd(),  help="Address pointing to the file location")
parser.add_argument("-p","--server_ports",metavar="",type=int,nargs="*",required=True,  help="(‘n’ port numbers, one for each server max=4) E.g 101 102 103 104")
#Although it verifiees input type we still need to convert it into int for usage
args = parser.parse_args()
print(type(args.server_ports))
if len(args.server_ports) != int(args.num_servers) :
    raise Exception('The number of ports {} not equal num of servers {} '.format(args.server_ports,args.num_servers))


"""
for a in args.__dict__:
        print(str(a) + ": " + str(args.__dict__[a]))
        print("Ports number accessed by variable name ports :{}" .format(args.server_ports))
"""

'''
Handling server actionss
'''
HEADER = 8192
NO_OF_PORTS = args.server_ports
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"

def simpleSend(conn,msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        print(msg_length)
        if msg_length:
            msg_length = len(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                continue
            if msg[:11]=="Receving File":
                with open("code.txt") as file:
                    size = os.path.getsize(file)
                    msg = "filesize "+str(size)
                    simpleSend(conn,msg)
                    msg_length = conn.recv(HEADER).decode(FORMAT)
                    if msg_length:
                        msg_length = int(msg_length)
                        msg = conn.recv(msg_length).decode(FORMAT)
                        msg.split()
                        data = file_handling.get_file_part(filename,msg[0],msg[0])
                        conn.send(data.encode(FORMAT))
            else:
                print(f"[{addr}] {msg}")
                conn.send("Msg received".encode(FORMAT))

    conn.close()

def startserver(SERVER,PORT):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ADDR = (SERVER, PORT)
    server.bind(ADDR)
    print(f"[LISTENING] Server is listening on {SERVER} port {PORT}")
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1} for {PORT} ")

def start():
    for i in NO_OF_PORTS :
        thread = threading.Thread(target=startserver, args=(SERVER, i))
        thread.start()
        
print("[STARTING] server is starting...")
start()


