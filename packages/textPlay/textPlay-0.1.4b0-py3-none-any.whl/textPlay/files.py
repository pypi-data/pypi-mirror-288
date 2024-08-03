'''
# Manipulate between Files creation, deletion, read, write and more
'''

import os

USER = os.path.expanduser("~/")

def crt_dir(folder_name: str, exist= True):
    os.makedirs(folder_name, exist_ok= exist)

def del_file(file_name):
    os.remove(file_name)

def del_folder(file_name):
    os.rmdir(file_name)

def rename_folder(old_fld, new_fld):
    os.rename(old_fld, new_fld)

def move_folder(old_fld, new_fld):
    os.rename(old_fld, new_fld)

def list_dir(dir):
    return os.listdir(dir)

def write_file(file_name, content='', tell_me= False):
    if content == '':
        with open(file_name, 'w') as fh:
            pass
    else:
        with open(file_name, 'w') as fh:
            fh.write(content)

    if tell_me:
        print("File Written sucessfully")


def read_file(file_name):
    with open(file_name, 'w') as fh:
        read = fh.read()
        return read
            