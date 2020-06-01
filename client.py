import argparse
import os
import ipaddress
import socket
import threading

parser = argparse.ArgumentParser()

#verify correct working base directory is provided
def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)
#validates ip address
def ip(string):
    try:
        ip_addr = ipaddress.ip_address(string)
    except:
        print("Please Provide Valid Ip Address")
# command line command to run it : python sample.py -i 5 -n 2 -f 4 -p 100 101 102 
parser.add_argument("-i","--status_interval",metavar="Reporting Interval",type=int,required=True,  help="Time interval between metric reporting in seconds E.g 5(seconds)")
parser.add_argument("-o","--output_directory",type=dir_path,default= os.getcwd(),  help="path of output directory")
parser.add_argument("-a","--ipaddr",type=ip,required=True, help="IP address of server")
parser.add_argument("-p","--server_ports",metavar="",type=int,nargs="+",required=True,  help="List of port numbers (one for each server) E.g 101 102 103 104")
#Although it verifiees input type we still need to convert it into int for usage

args = parser.parse_args()


''' for a in args.__dict__:
        print(str(a) + ": " + str(args.__dict__[a]))
        print("Ports number accessed by variable name ports :{}" .format(args.server_ports))'''

HEADER = 8192
NO_OF_PORTS = args.server_ports
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
APPLICATION_DATA = ""

def simplesend(client,msg):
    print(msg)
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    a = client.send(send_length)
    client.send(message)
    msg = client.recv(1024)
    print(msg.decode(FORMAT) + str(a) + ": Empty")

def send(client,msg,clientNo):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    connected = True
    data=""
    while connected:
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = len(msg_length)
            msg = client.recv(msg_length).decode(FORMAT)
            if msg[:8]=="filesize":
                msg.split(" ")
                filesize=int(msg[1])
                part = filesize/int(NO_OF_PORTS)
                
                print(part,clientNo,client)

                offset = b' ' * part * (clientNo-1)
                end = offset + part 
                msg = str(offset) +" "+ str(end) 
               
                print(msg)
            
                client.simplesend(msg)
                #receiving file
                while connected:
                    msg_length = client.recv(HEADER).decode(FORMAT)
                    msg = conn.recv(msg_length).decode(FORMAT)
                    if msg_length:
                        data= data + msg
                    if msg == DISCONNECT_MESSAGE:
                        connected = False
                        return data
        if len(data) == len(str(end-offset)):
                        connected = False
                        return data
        connected = False
        #just printing for now later store it in dictionary//array to gather all dataprts
        print(data)
        conn.send("Msg received".encode(FORMAT))
        return ""
        

        
    conn.close()

    print(client.recv(2048).decode(FORMAT))

def connectToServer(SERVER,PORT,clientNo):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ADDR = (SERVER, PORT)
    client.connect(ADDR)
    client.send("Hello i m error".encode(FORMAT))
    simplesend(client,f"Server {clientNo} connected")
    send(client,"Receving File",clientNo)
   # send(client,f"    ")
    simplesend(client,"DISCONNECT")
clientNo = 1
for i in NO_OF_PORTS :
    thread = threading.Thread(target=connectToServer, args=(SERVER, i,clientNo))
    thread.start()
    clientNo+=1