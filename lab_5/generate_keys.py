import os
from cryptography.hazmat.primitives.asymmetric import rsa
from asymmetrical import AsymmetricCryptography


class GenerateKeys:
    """
    Класс для генерации ключей шифрования.
    """
    @staticmethod
    def generate_symmetric_key() -> tuple[bytes, bytes]:
        """
        Генерирует 256-битный ключ и 128-битный nonce для симметричного шифрования.
        :return: кортеж, содержащий ключ (32 байта) и nonce (16 байт)
        """
        key = os.urandom(32)
        nonce = os.urandom(16)

        return key, nonce


    @staticmethod
    def generate_rsa_key_pair() -> tuple[rsa.RSAPublicKey, rsa.RSAPrivateKey]:
        """
        Генерирует пару RSA-ключей (публичный и приватный).
        :return: кортеж, содержащий публичный и приватный ключи
        """
        private_key = rsa.generate_private_key(public_exponent=65537,
                                               key_size=2048)
        public_key = private_key.public_key()

        return public_key, private_key


    @staticmethod
    def generate_and_encrypt_keys() -> tuple[rsa.RSAPublicKey, rsa.RSAPrivateKey, bytes]:
        """
        Генерирует ключи симметричного и асимметричного шифрования и затем шифрует симметричный ключ.
        :return: кортеж (открытый ключ, закрытый ключ, зашифрованный симметричный ключ)
        """
        symmetric_key, nonce = GenerateKeys.generate_symmetric_key()
        public_key, private_key = GenerateKeys.generate_rsa_key_pair()

        encrypted_sym_key = AsymmetricCryptography.encrypt(public_key, symmetric_key)

        return public_key, private_key, encrypted_sym_key
