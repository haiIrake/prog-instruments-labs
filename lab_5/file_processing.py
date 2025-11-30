import json
import logging
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey


logger = logging.getLogger(__name__)


class FileOperations:
    """
    Класс для файловых операций и сериализации/десериализации ключей шифрования.
    """
    @staticmethod
    def read_bin(filename: str) -> bytes:
        """
        Читает содержимое бинарного файла.
        :param filename: путь к файлу
        :return: содержимое файла в байтах
        """
        try:
            logger.debug(f"Reading binary file: {filename}")
            with open(filename, "rb") as file:
                data = file.read()
                logger.debug(f"Binary file {filename} was read, size: {len(data)} bytes")
                return data
        except FileNotFoundError:
            logger.error(f"File {filename} not found")
        except Exception as e:
            logger.error(f"An error occurred while reading the file {filename}: {e}")

    @staticmethod
    def write_bin(data: bytes, filename: str) -> None:
        """
        Записывает бинарные данные в файл.
        :param data: бинарные данные для записи
        :param filename: путь к файлу, в который будут записаны данные
        """
        try:
            logger.debug(f"Writing binary file: {filename}, size: {len(data)} bytes")
            with open(filename, "wb") as file:
                file.write(data)
            logger.debug(f"Binary file {filename} was successfully written")
        except Exception as e:
            logger.error(f"An error occurred while saving the file {filename}: {e}")

    @staticmethod
    def load_json(filename: str) -> dict:
        """
        Загружает данные из json-файла.
        :param filename: путь к файлу
        :return: словарь с содержимым файла
        """
        try:
            logger.debug(f"Loading configuration from {filename}")
            with open(filename, "r", encoding="utf-8") as file:
                config = json.load(file)
                logger.debug(f"Configuration from {filename} was successfully loaded")
                return config
        except FileNotFoundError:
            logger.error(f"File {filename} not found")
        except json.JSONDecodeError:
            logger.error(f"File {filename} isn't correct JSON")
        except Exception as e:
            logger.error(f"An error occurred while reading the file {filename}: {e}")

    @staticmethod
    def write_txt(data: str, filename: str) -> None:
        """
        Записывает текст в файл.
        :param data: строка, которая будет записана в файл
        :param filename: путь к файлу, в который будет записан текст
        """
        try:
            logger.debug(f"Writing text file: {filename}, size: {len(data)} symbols")
            with open(filename, "w", encoding="utf-8") as file:
                file.write(data)
            logger.debug(f"Text file {filename} was successfully written")
        except Exception as e:
            logger.error(f"An error occurred while saving the file {filename}: {e}")

    @staticmethod
    def load_public_key(key_path: str) -> RSAPublicKey:
        """
        Загружает публичный RSA-ключ из pem-файла.
        :param key_path: путь к файлу
        :return: публичный ключ
        """
        try:
            logger.debug(f"Loading public key from {key_path}")
            with open(key_path, "rb") as key_file:
                public_key = load_pem_public_key(key_file.read())
            logger.debug(f"Public key from {key_path} was successfully loaded")
            return public_key
        except FileNotFoundError:
            logger.error(f"Public key file not found at {key_path}")
        except Exception as e:
            logger.error(f"Failed to load public key: {e}")

    @staticmethod
    def save_public_key(public_key: RSAPublicKey, key_path: str) -> None:
        """
        Сохраняет публичный RSA-ключ по указанному пути.
        :param public_key: публичный ключ
        :param key_path: путь к pem-файлу для сохранения
        """
        try:
            logger.debug(f"Saving public key to {key_path}")
            pem_data = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

            with open(key_path, "wb") as key_file:
                key_file.write(pem_data)
            logger.debug(f"Public key was successfully saved to {key_path}")
        except Exception as e:
            logger.error(f"An error occurred while saving public key: {e}")

    @staticmethod
    def load_private_key(key_path: str) -> RSAPrivateKey:
        """
        Загружает приватный RSA-ключ из pem-файла.
        :param key_path: путь к файлу
        :return: приватный ключ
        """
        try:
            logger.debug(f"Loading private key from {key_path}")
            with open(key_path, "rb") as key_file:
                private_key = load_pem_private_key(key_file.read(), password=None)
            logger.debug(f"Private key from {key_path} was successfully loaded")
            return private_key
        except FileNotFoundError:
            logger.error(f"Private key file not found at {key_path}")
        except Exception as e:
            logger.error(f"Failed to load private key: {e}")

    @staticmethod
    def save_private_key(private_key: RSAPrivateKey, key_path: str) -> None:
        """
        Сохраняет приватный RSA-ключ по указанному пути.
        :param private_key: приватный ключ
        :param key_path: путь к pem-файлу для сохранения
        """
        try:
            logger.debug(f"Saving private key to {key_path}")
            pem_data = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )

            with open(key_path, "wb") as key_file:
                key_file.write(pem_data)
            logger.debug(f"Private key was successfully saved to {key_path}")
        except Exception as e:
            logger.error(f"An error occurred while saving private key: {e}")
