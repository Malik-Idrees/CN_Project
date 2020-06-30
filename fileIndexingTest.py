import os
file1 = "video.mp4"
file2 = "video2.mp4"
# size in bytes
size = os.path.getsize(file1)
size2 = os.path.getsize(file2)

'''
The logic for file transfer between client and server load balancing using indexing
no decimal parts are lost as these are converted to int cutting the decimal part
thus 1st msg end and 2nd msg start are same i.e
msg 1 : if range 0-78.5 is converted to 0-78
then msg 2 : range 78.5 - 157 converted to 78-157 i.e from 79 to 157
f.seek(78) will start reading from 79 upto 157
'''

if __name__ == "__main__":
    print("size1 : " + str(size))
    print("size2 : " + str(size2))
# Testing file indexing method
    filesize = size
    NO_OF_PORTS = 4
    part = filesize/NO_OF_PORTS
    print(f"part : {part}")

    clientNo = 1
    for i in range(NO_OF_PORTS):
        offset = part * (clientNo-1)
        print(f"{clientNo} offset{offset}")
        end = offset + part
        print(f"{clientNo} end{end}")
        msg = str(offset) + " " + str(end)
        print(f'{clientNo}   #{msg}')
        clientNo += 1
    if (size == int(end)):
        print("Whole file will be transfered correctly")
