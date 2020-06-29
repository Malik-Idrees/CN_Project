import os
size = os.path.getsize("sample.pdf")
size2 = os.path.getsize("code2.txt")
print(type(size))
print("size1" + str(size))
print("size2" + str(size2))


filesize = size
NO_OF_PORTS = 4
part = filesize/NO_OF_PORTS
clientNo = 1
#
part = int(part)
offset = part * (clientNo-1)
end = int(offset) + part
msg = str(offset) + " " + str(end)
print(msg)
