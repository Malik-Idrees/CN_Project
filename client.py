import argparse
import os
import ipaddress
import socket
import threading
import file_handling
import time
import math

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
'''
for a in args.__dict__:
        print(str(a) + ": " + str(args.__dict__[a]))
        print("Ports number accessed by variable name ports :{}" .format(
            args.server_ports))
'''

# Throughout usable formats and structuring
HEADER = 8192
NO_OF_PORTS = args.server_ports
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
APPLICATION_DATA = b''
# recvBytes = 0 ...for overall average downloading speed
TIME_PASSED = 0
TIME_FLAG = True


def calcTime(startTime):
    global TIME_PASSED, TIME_FLAG
    TIME_PASSED = time.time() - startTime
    return TIME_PASSED


'''
It sends the Msg-length and then message
'''


def simplesend(client, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def send(client, msg, clientNo):
    global TIME_PASSED, TIME_FLAG, recvBytes
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
                filesize = int(msg[1])
                part = filesize/int(len(NO_OF_PORTS))

                # indexing has been tested and it works fine this way ~fileIndexingTest.py 1ByteLoss!
                part = int(part)
                offset = part * (clientNo-1)
                end = offset + part
                msg = str(offset) + " " + str(end)

                # the msg notifies the server of required btye range
                simplesend(client, msg)

                # receiving file
                readSize = 1024
                startTime = time.time()
                while connected:

                    calcTime(startTime)
                    recvF = client.recv(readSize)

                    if (math.floor(TIME_PASSED) % 2 == 0 and TIME_FLAG == True):
                        print(
                            f"{clientNo} : {(len(data)/1000)/(TIME_PASSED+1) :.2f} kb/s")
                        TIME_FLAG = False

                    if (math.floor(TIME_PASSED) % 2 == 1 and TIME_FLAG == False):
                        os.system('cls' if os.name == 'nt' else 'clear')
                        TIME_FLAG = True

                    if recvF:
                        data += recvF
                        # recvBytes += len(recvF)
                    else:
                        client.close()
                        connected = False
        # need a logic to handle server crashes
        # if len(data) != len(str(end-offset)):
        #     return False
    client.close()
    return data


# we will store our data chunks and later organize it
Dict = {}

'''
Note 1
Could be improved using some pooling or .map() function
to get output in organized form
'''


def connectToServer(SERVER, PORT, clientNo):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ADDR = (SERVER, PORT)
    client.connect(ADDR)
    Dict[clientNo] = send(client, "Receving File", clientNo)
    return ''
    # simplesend(client, "DISCONNECT")


# we will use it to store threads and applying thread .join() to ensure every threads completes before moving forward
threads = []
''' 
Note 2
 it can be improved by making an array that stores connection..
 then looping through the number of connections accepted rather than input to handle load balancing
'''
clientNo = 1
for i in NO_OF_PORTS:
    thread = threading.Thread(target=connectToServer,
                              args=(SERVER, i, clientNo))
    thread.start()
    threads.append(thread)
    clientNo += 1

# making sure every threads completes
for t in threads:
    # print("Waiting for All threads to complete...")
    t.join()

# Organizing the chunks in order from the dictionary
for i in range(len(Dict)):
    i = i+1
    APPLICATION_DATA += Dict.get(i)

# writing all chunks in order to output file
file_handling.write_file(
    "C:\\Users\\user\\Desktop\\CN_Project\\video2.mp4", APPLICATION_DATA)
