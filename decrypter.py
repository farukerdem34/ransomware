import os
from cryptography.fernet import Fernet


def get_files():
    files = []
    non_encrptfiles = ["encrpyter.py","LICENCE","README.md"]
    for file in os.listdir():
        if file in non_encrptfiles:
            continue 
            # Do not encrypt these files.
        if os.path.isfile(file):
            files.append(file) 
            #Do not add if this is a directory, only if a file.
    return files

def decrypt_files(files,key=None):
    key = str(input("ENTER KEY: "))
    for file in files:
        with open(file,"rb") as the_file:
            contents = the_file.read()
        contents_decrypted = Fernet(key).decrypt(contents)
        with open(file,"wb") as the_file:
            the_file.write(contents_decrypted)

decrypt_files(get_files())