import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms


class SymmetricCryptography:
    """
    Класс для симметричного шифрования с использованием алгоритма ChaCha20.
    """
    @staticmethod
    def encrypt(plaintext: bytes, key: bytes, nonce: bytes = None) -> tuple[bytes, bytes]:
        """
        Шифрует данные с помощью алгоритма шифрования ChaCha20.
        :param plaintext: данные, которые должны быть зашифрованы
        :param key: ключ шифрования (32 байта)
        :param nonce: одноразовое случайное число (16 байт)
        :return: кортеж, содержащий зашифрованные данные и nonce
        """
        try:
            if nonce is None:
                nonce = os.urandom(16)

            cipher = Cipher(algorithm=algorithms.ChaCha20(key, nonce),
                            mode=None,
                            backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(plaintext) + encryptor.finalize()

            return ciphertext, nonce
        except Exception as e:
            print(f"Encryption error: {e}")


    @staticmethod
    def decrypt(ciphertext: bytes, key: bytes, nonce: bytes = None) -> str:
        """
        Дешифрует данные, зашифрованные с помощью алгоритма ChaCha20.
        :param ciphertext: зашифрованные данные
        :param key: ключ шифрования (32 байта)
        :param nonce: nonce, использованный во время шифрования (16 байт)
        :return: строка с дешифрованными данными
        """
        try:
            cipher = Cipher(algorithm=algorithms.ChaCha20(key, nonce),
                            mode=None,
                            backend=default_backend())
            decryptor = cipher.decryptor()
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()

            return plaintext.decode("utf-8")
        except Exception as e:
            print(f"Decryption error: {e}")
