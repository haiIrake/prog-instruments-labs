import logging
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms


logger = logging.getLogger(__name__)


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
            logger.debug(f"ChaCha20 encryption started, plaintext size: {len(plaintext)} symbols")
            if nonce is None:
                nonce = os.urandom(16)

            cipher = Cipher(algorithm=algorithms.ChaCha20(key, nonce),
                            mode=None,
                            backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(plaintext) + encryptor.finalize()

            logger.debug(f"ChaCha20 encryption completed, ciphertext size: {len(ciphertext)} bytes")
            return ciphertext, nonce
        except Exception as e:
            logger.error(f"Encryption error: {e}")

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
            logger.debug(f"ChaCha20 decryption started, ciphertext size: {len(ciphertext)} bytes")
            cipher = Cipher(algorithm=algorithms.ChaCha20(key, nonce),
                            mode=None,
                            backend=default_backend())
            decryptor = cipher.decryptor()
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()

            logger.debug(f"ChaCha20 decryption completed, plaintext size: {len(plaintext)} symbols")
            return plaintext.decode("utf-8")
        except Exception as e:
            logger.error(f"Decryption error: {e}")
