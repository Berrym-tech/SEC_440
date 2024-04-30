import os
from cryptography.fernet import Fernet

# Load the encryption key from the saved file
def load_key():
    with open('Ransom.key', 'rb') as filekey:
        key = filekey.read()
    return key

# Function to decrypt files
def decrypt_file(encrypted_file_path, key):
    fernet = Fernet(key)
    with open(encrypted_file_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()
        print("Encrypted Data:", encrypted_data)  # Debugging statement
        decrypted_data = fernet.decrypt(encrypted_data)
    return decrypted_data

# Folder location where the encrypted files are stored
encrypted_directory_path = "/home/maxwell/Desktop/Happy Files"

# Load the encryption key
key = load_key()
print("Encryption Key:", key)  # Debugging statement

# Decrypt files with the .encrypted extension
for root, dirs, files in os.walk(encrypted_directory_path):
    for file in files:
        if file.endswith('.encrypted'):
            encrypted_file_path = os.path.join(root, file)
            print("Decrypting:", encrypted_file_path)  # Debugging statement
            decrypted_data = decrypt_file(encrypted_file_path, key)
            decrypted_file_path = encrypted_file_path.replace('.encrypted', '')
            with open(decrypted_file_path, 'wb') as decrypted_file:
                decrypted_file.write(decrypted_data)
            os.remove(encrypted_file_path)
            print(f"File '{decrypted_file_path}' Decrypted.")

print("All files decrypted successfully.")
