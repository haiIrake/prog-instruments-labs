from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey


class AsymmetricCryptography:
    """
    Класс для асимметричного шифрования с использованием RSA.
    """
    @staticmethod
    def encrypt(public_key: RSAPublicKey, data: bytes) -> bytes:
        """
        Шифрует данные с использованием публичного RSA-ключа.
        :param public_key: публичный RSA-ключ
        :param data: данные, которые нужно зашифровать
        :return: зашифрованные данные
        """
        try:
            encrypted_data = public_key.encrypt(
                data,
                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                             algorithm=hashes.SHA256(),
                             label=None)
            )

            return encrypted_data
        except Exception as e:
            print(f"Encryption error: {e}")


    @staticmethod
    def decrypt(private_key: RSAPrivateKey, encrypted_data: bytes) -> bytes:
        """
        Дешифрует данные с использованием приватного RSA-ключа.
        :param private_key: приватный RSA-ключ
        :param encrypted_data: зашифрованные данные
        :return: дешифрованные данные
        """
        try:
            decrypted_data = private_key.decrypt(
                encrypted_data,
                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                             algorithm=hashes.SHA256(),
                             label=None)
            )

            return decrypted_data
        except Exception as e:
            print(f"Decryption error: {e}")
