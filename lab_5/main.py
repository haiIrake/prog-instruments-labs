import argparse
from file_processing import FileOperations
from generate_keys import GenerateKeys
from asymmetrical import AsymmetricCryptography
from symmetrical import SymmetricCryptography


def main():
    try:
        source = FileOperations.load_json("settings.json")

        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("-gen", "--generation", action="store_true", help="Запускает режим генерации ключей")
        group.add_argument("-enc", "--encryption", action="store_true", help="Запускает режим шифрования")
        group.add_argument("-dec", "--decryption", action="store_true", help="Запускает режим дешифрования")

        args = parser.parse_args()

        match (args.generation, args.encryption, args.decryption):
            case (True, False, False):
                print("Запущен режим генерации ключей...")

                public_key, private_key, encrypted_sym_key = GenerateKeys.generate_and_encrypt_keys()

                FileOperations.save_public_key(public_key, source["public_key"])
                FileOperations.save_private_key(private_key, source["private_key"])
                FileOperations.write_bin(encrypted_sym_key, source["symmetric_key"])

                print(f"Ключи успешно сгенерированы: {source["public_key"]}, {source["private_key"]}, {source["symmetric_key"]}")

            case (False, True, False):
                print("Запущен режим шифрования...")

                private_key = FileOperations.load_private_key(source["private_key"])
                encrypted_sym_key = FileOperations.read_bin(source["symmetric_key"])

                symmetric_key = AsymmetricCryptography.decrypt(private_key, encrypted_sym_key)

                text = FileOperations.read_bin(source["input_file"])

                encrypted_text, nonce = SymmetricCryptography.encrypt(text, symmetric_key)

                FileOperations.write_bin(encrypted_text, source["encrypted_file"])
                FileOperations.write_bin(nonce, source["nonce"])

                print(f"Файл успешно зашифрован: {source["encrypted_file"]}")

            case (False, False, True):
                print("Запущен режим дешифрования...")

                private_key = FileOperations.load_private_key(source["private_key"])
                encrypted_sym_key = FileOperations.read_bin(source["symmetric_key"])

                symmetric_key = AsymmetricCryptography.decrypt(private_key, encrypted_sym_key)

                encrypted_text = FileOperations.read_bin(source["encrypted_file"])
                nonce = FileOperations.read_bin(source["nonce"])

                decrypted_text = SymmetricCryptography.decrypt(encrypted_text, symmetric_key, nonce)

                FileOperations.write_txt(decrypted_text, source["decrypted_file"])

                print(f"Файл успешно дешифрован: {source["decrypted_file"]}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
