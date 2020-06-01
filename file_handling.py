def get_file_part(filename,start_index,end_index):
    with open(filename) as filepart:
        filepart.seek(start_index)
        data = file.read(end_index - start_index)
    return data

def write_file(path,content):
    with open(path,"wb") as file:
        file.write(content)
    return print("File Saved Successfully")

