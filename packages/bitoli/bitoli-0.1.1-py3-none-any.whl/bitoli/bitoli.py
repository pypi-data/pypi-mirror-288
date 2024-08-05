import os
import zlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b85decode

def encode(data, key):
    key = key.encode()[:32].ljust(32, b'\0')
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = iv + encryptor.update(data.encode('utf-8')) + encryptor.finalize()
    compressed_data = zlib.compress(encrypted_data)
    return compressed_data

def decode(data, key):
    key = key.encode()[:32].ljust(32, b'\0')
    try:
        decompressed_data = zlib.decompress(data)
    except zlib.error:
        try:
            decoded = b85decode(data)
            decompressed_data = zlib.decompress(decoded)
        except:
            decompressed_data = data
    iv, ciphertext = decompressed_data[:16], decompressed_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_data.decode('utf-8')

if __name__ == "__main__":
    print("This module provides functions for encrypting (encode) and decrypting (decode) data.")
    print("Please use this module as an import in another script.")
