import os
from cryptography.fernet import Fernet

# Load the encryption key from the 'Ransome.key' file
def load_key():
    with open('Ransome.key', 'rb') as filekey:
        return filekey.read()

# Function to decrypt files
def decrypt_file(encrypted_file_path, key):
    fernet = Fernet(key)
    with open(encrypted_file_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()
        decrypted_data = fernet.decrypt(encrypted_data)
    decrypted_file_path = encrypted_file_path.replace('.encrypted', '_decrypted')
    with open(decrypted_file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)
    return decrypted_file_path

# Folder location of where the encrypted files are located
encrypted_directory_path = "home/maxwell/Desktop/Happy Files/"

# Load the encryption key
encryption_key = load_key()

# Decrypt files in the specified directory
for root, dirs, files in os.walk(encrypted_directory_path):
    for file in files:
        if file.endswith('.encrypted'):
            encrypted_file_path = os.path.join(root, file)
            decrypted_file_path = decrypt_file(encrypted_file_path, encryption_key)
            print(f"File '{file}' decrypted to '{decrypted_file_path}'.")

print("Decryption process completed.")