import argparse
import logging
from file_processing import FileOperations
from generate_keys import GenerateKeys
from asymmetrical import AsymmetricCryptography
from symmetrical import SymmetricCryptography


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("cryptosystem.log", encoding="utf-8"),
              logging.StreamHandler()],
)
logger = logging.getLogger("main")


def main():
    try:
        source = FileOperations.load_json("settings.json")

        logger.info("Parsing command line arguments")
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("-gen", "--generation", action="store_true", help="Запускает режим генерации ключей")
        group.add_argument("-enc", "--encryption", action="store_true", help="Запускает режим шифрования")
        group.add_argument("-dec", "--decryption", action="store_true", help="Запускает режим дешифрования")

        args = parser.parse_args()

        match (args.generation, args.encryption, args.decryption):
            case (True, False, False):
                logger.info("Key generation mode started")

                public_key, private_key, encrypted_sym_key = GenerateKeys.generate_and_encrypt_keys()

                FileOperations.save_public_key(public_key, source["public_key"])
                FileOperations.save_private_key(private_key, source["private_key"])

                logger.debug(f"Saving symmetric encryption key to {source["symmetric_key"]}")
                FileOperations.write_bin(encrypted_sym_key, source["symmetric_key"])
                logger.debug(f"Symmetric encryption key was successfully saved to {source["symmetric_key"]}")

                logger.info("Keys were successfully generated and saved to "
                            f"{source["public_key"]}, {source["private_key"]}, {source["symmetric_key"]}")

            case (False, True, False):
                logger.info("Encryption mode started")

                private_key = FileOperations.load_private_key(source["private_key"])

                logger.debug(f"Loading symmetric encryption key from {source["symmetric_key"]}")
                encrypted_sym_key = FileOperations.read_bin(source["symmetric_key"])
                logger.debug(f"Symmetric encryption key from {source["symmetric_key"]} was successfully loaded")

                logger.debug("Decrypting symmetric encryption key")
                symmetric_key = AsymmetricCryptography.decrypt(private_key, encrypted_sym_key)
                logger.debug("Symmetric encryption key was successfully decrypted")

                text = FileOperations.read_bin(source["input_file"])

                encrypted_text, nonce = SymmetricCryptography.encrypt(text, symmetric_key)

                FileOperations.write_bin(encrypted_text, source["encrypted_file"])
                FileOperations.write_bin(nonce, source["nonce"])

                logger.info(f"File was successfully encrypted and saved to {source["encrypted_file"]}")

            case (False, False, True):
                logger.info("Decryption mode started")

                private_key = FileOperations.load_private_key(source["private_key"])

                logger.debug(f"Loading symmetric encryption key from {source["symmetric_key"]}")
                encrypted_sym_key = FileOperations.read_bin(source["symmetric_key"])
                logger.debug(f"Symmetric encryption key from {source["symmetric_key"]} was successfully loaded")

                logger.debug("Decrypting symmetric encryption key")
                symmetric_key = AsymmetricCryptography.decrypt(private_key, encrypted_sym_key)
                logger.debug("Symmetric encryption key was successfully decrypted")

                encrypted_text = FileOperations.read_bin(source["encrypted_file"])
                nonce = FileOperations.read_bin(source["nonce"])

                decrypted_text = SymmetricCryptography.decrypt(encrypted_text, symmetric_key, nonce)

                FileOperations.write_txt(decrypted_text, source["decrypted_file"])

                logger.info(f"File was successfully decrypted and saved to {source["decrypted_file"]}")
    except Exception as e:
        logger.error(f"Error: {e}")


if __name__ == "__main__":
    main()
