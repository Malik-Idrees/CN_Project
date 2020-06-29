import argparse
import os
import ipaddress
import socket
import threading
import file_handling

parser = argparse.ArgumentParser()

# verify correct working base directory is provided


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)
# validates ip address


def ip(string):
    try:
        ip_addr = ipaddress.ip_address(string)
    except:
        print("Please Provide Valid Ip Address")


# command line command to run it : python sample.py -i 5 -n 2 -f 4 -p 100 101 102
parser.add_argument("-i", "--status_interval", metavar="Reporting Interval", type=int,
                    required=True,  help="Time interval between metric reporting in seconds E.g 5(seconds)")
parser.add_argument("-o", "--output_directory", type=dir_path,
                    default=os.getcwd(),  help="path of output directory")
parser.add_argument("-a", "--ipaddr", type=ip,
                    required=True, help="IP address of server")
parser.add_argument("-p", "--server_ports", metavar="", type=int, nargs="+", required=True,
                    help="List of port numbers (one for each server) E.g 101 102 103 104")
# Although it verifiees input type we still need to convert it into int for usage

args = parser.parse_args()

# just to make sure argument parsing is working
''' for a in args.__dict__:
        print(str(a) + ": " + str(args.__dict__[a]))
        print("Ports number accessed by variable name ports :{}" .format(args.server_ports))'''
# Throughout usable formats and structuring
HEADER = 8192
NO_OF_PORTS = args.server_ports
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
APPLICATION_DATA = b''

# this simply send the message to server


def simplesend(client, msg):
    #print("Byte range we are asking"+msg)
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    # just for testing connectivity
    # msg = client.recv(1024)
    # print(msg.decode(FORMAT) + " ending...")
    # print("msg: "+msg.decode(FORMAT))
    # file_handling.write_file("C:\\Users\\user\\Desktop\\CN_Project\\code2.txt", msg)
    # print("done")


def send(client, msg, clientNo):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    connected = True
    data = b''
    while connected:
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = len(msg_length)
            msg = client.recv(msg_length).decode(FORMAT)
            if msg[:8] == "filesize":  # size in bytes

                msg = msg.split(' ')

                # print(type(msg)) splitting to get start and end of index #print(str(msg_length) + 'hello')
                #print("receiving file size in bytes")
                # print("File_size:"+str(filesize))
                # print("Ports :"+str(len(NO_OF_PORTS)))
                #print(part, clientNo, client)
                #print(str(type(part)) + 'part type')

                filesize = int(msg[1])
                part = filesize/int(len(NO_OF_PORTS))

                #print(f"line {clientNo} will download {part} Bytes")
                # we can improve the divisioning using ceil like before calculating offset..cuz we need int
                # thus for now its int but if its float it will cause an error

                part = int(part)
                offset = part * (clientNo-1)
                end = offset + part
                msg = str(offset) + " " + str(end)

                # print("clientNo"+str(clientNo) + "msg" + msg)#the msg tells which byte range it needs to server
                # Telling server the byte range we need

                simplesend(client, msg)
                # receiving file
                i = 1
                while connected:
                    # msg_length = client.recv(HEADER).decode(FORMAT)
                    # if msg_length:
                    #     msg_length = len(msg_length)
                    #     msg = client.recv(msg_length).decode(FORMAT)

                    #recvF = client.recv(1024).decode(FORMAT)
                    recvF = client.recv(1024)
                    print(clientNo)
                    if recvF:
                        data += recvF
                    else:
                        client.close()
                        connected = False
                        print("ended")
                    # msg_length = client.recv(HEADER).decode(FORMAT)
                    # msg_length = len(msg_length)
                    #     # for now we are setting it to chunk size but we can use while loop to read it in smaller chunks
                    #     # or changing server such that it sends that in chunks and in every loop we check it.and changed connected behaviour we different statements
                    # msg = client.recv(msg_length).decode(FORMAT)
                    # if msg_length:
                    #     data = data + msg
                    #     connected = False
                    # if msg == DISCONNECT_MESSAGE:
                    #     connected = False
                    #     return data

        # if len(data) == len(str(end-offset)):
        #     connected = False
        # return data
        # connected = False
        #client.send('""+clientNo + " Msg Received...Ending"'.encode(FORMAT))
        #print(f'{clientNo}done with data recving')
        #simplesend(client, DISCONNECT_MESSAGE)
    client.close()
    return data


# For now using it to arrange our chunks of data
Dict = {}

''' we could return every threads data if there is any .map() function 
to get output in organized form'''


def connectToServer(SERVER, PORT, clientNo):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ADDR = (SERVER, PORT)
    client.connect(ADDR)
    Dict[clientNo] = send(client, "Receving File", clientNo)
    return ''

    # client.send("Hello i m error".encode(FORMAT))
    # simplesend(client, f"Server {clientNo} connected {dummy} ")
    # print("dictionary length" + str(len(Dict)))# print(Dict)
    # simplesend(client, "DISCONNECT")


# we will use it to store threads and applying thread .join() to ensure every threads completes/crashes before moving forward
threads = []

# depending upon ports it receives the data through data handling
# it can be improved by making an array that stores connection..then looping through them
clientNo = 1
for i in NO_OF_PORTS:
    thread = threading.Thread(target=connectToServer,
                              args=(SERVER, i, clientNo))
    thread.start()
    threads.append(thread)
    clientNo += 1

# making sure every threads completes
for t in threads:
    print("Waiting for All threads to complete...")
    t.join()

# Organizing the chunks in order
for i in range(len(Dict)):
    i = i+1
    print(i)
    print(type(Dict.get(i)))
    APPLICATION_DATA += Dict.get(i)

# writing all chunks in order to output file
file_handling.write_file(
    "C:\\Users\\user\\Desktop\\CN_Project\\code2.txt", APPLICATION_DATA)
