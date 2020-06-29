def get_file_part(filename, start_index, end_index):
    # print("end:" + end_index + "start:" + start_index)#to check that it receives correct range
    start_index = int(start_index)
    if end_index != ' ':
        end_index = int(end_index)
    else:
        print("error in indexing")

    with open(filename, 'rb') as filepart:
        # print(str(type(start_index)))#just making sure index is an int
        filepart.seek(start_index)
        data = filepart.read(end_index - start_index)
    return data

#


def write_file(path, content):
    with open(path, "wb") as file:
        file.write(content)
        return print("File Saved Successfully")
