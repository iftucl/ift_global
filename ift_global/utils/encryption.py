import base64
import hashlib
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


def create_ash_key(key_size: int):
    """
    Generates a hashing key.

    :param key_size: Numeric 64, 32, ...
    :type key_size: int
    :return: Returns a hexadecimal key
    :rtype: str
    """
    _key = os.urandom(key_size)
    return _key.hex()

def create_ash_salt(salt_size: int):
    """
    Generates salt.

    :param salt_size: Size of salt
    :type salt_size: int
    :return: Returns salt in hexadecimal
    :rtype: str
    """
    _salt = os.urandom(salt_size)
    return _salt.hex()

class HashingTool:
    """
    Hashing functionality.

    Hashes data provided using key and salt.
    """

    def __init__(self, key: str, salt: str, data: str):
        """
        Constructor.

        :param key: A hexadecimal key.
        :type key: str
        :param salt: A hexadecimal salt.
        :type salt: str
        :param data: Data to be hashed.
        :type data: str
        """
        self._key = bytes.fromhex(key)
        self._salt = bytes.fromhex(salt)
        self.hashed = self.hashit(data.encode())

    def hashit(self, data):
        """Hashes data provided."""
        data_with_salt = self._salt + data
        # Hash the new data with the stored key and salt
        h = hashlib.blake2b(key=self._key)
        h.update(data_with_salt)
        digest = h.hexdigest()
        return digest

    def __eq__(self, hasher):
        return self.hashed == hasher.hashed

    def __ne__(self, hasher):
        return self.hashed != hasher.hashed


class EncryptDecrypt:
    """
    Functionality to Encrypt & Decrypt.

    Encrypts and decrypts data based on hex key.
    """

    def __init__(self, internal_key):
        """
        Class constructor.

        :param internal_key: Internal key as hex representation.
        :type internal_key: str
        """
        self.block_size = algorithms.AES.block_size // 8  # Block size in bytes (AES block size is in bits)
        self.key = self._load_key(internal_key)

    @staticmethod
    def _load_key(key):
        key_bytes = bytes.fromhex(key)
        digest_key = hashlib.sha256(key_bytes).digest()
        return digest_key

    def encrypt(self, encrypt_str: str) -> str:
        """
        Encrypt a string.

        :param encrypt_str: A string to be encrypted.
        :type encrypt_str: str
        :return: Base64 encoded string.
        :rtype: str
        """
        # Pad the input string
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(encrypt_str.encode()) + padder.finalize()
        
        iv = os.urandom(self.block_size)  # Generate a random IV (initialization vector)

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        
        encryptor = cipher.encryptor()
        
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        return base64.b64encode(iv + encrypted_data).decode('utf-8')

    def decrypt(self, decrypt_str: str) -> str:
        """
        Decrypt a base64 encoded string.

        :param decrypt_str: A string to be decrypted.
        :type decrypt_str: str
        :return: Decrypted string.
        :rtype: str
        """
        enc = base64.b64decode(decrypt_str.encode('utf-8'))
        
        iv = enc[:self.block_size]
        
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        
        decryptor = cipher.decryptor()
        
        decrypted_data = decryptor.update(enc[self.block_size:]) + decryptor.finalize()
        
        # Unpad the decrypted data
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        
        return (unpadder.update(decrypted_data) + unpadder.finalize()).decode('utf-8')