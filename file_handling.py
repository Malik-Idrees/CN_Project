'''
It provides specific byte range of a file
'''


def get_file_part(filename, start_index, end_index):
    # print("end:" + end_index + "start:" + start_index)
    # print(str(type(start_index)))#just making sure index is an int
    with open(filename, 'rb') as filepart:
        filepart.seek(start_index)
        data = filepart.read(end_index - start_index)
    return data


'''
writes output file from binary data
'''


def write_file(path, content):
    with open(path, "wb") as file:
        file.write(content)
        return print("File Saved Successfully")
