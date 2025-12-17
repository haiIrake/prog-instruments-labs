def encrypt_trithemius(text: str, alphabet: str, key: str) -> str:
    """
    Шифрует текст с помощью шифра Тритемиуса.
    :param text: исходный текст
    :param alphabet: алфавит, используемый для шифрования
    :param key: ключевое слово для шифра
    :return: строка с зашифрованным текстом
    """
    if not text:
        raise ValueError("Text is empty")

    if not alphabet:
        raise ValueError("Alphabet is empty")

    alphabet = alphabet.lower()

    if not key:
        raise ValueError("Key is empty")

    key = key.lower()

    if not all(c in alphabet for c in key):
        raise ValueError("Key must contain characters from alphabet")

    extended_key = key * (len(text) // len(key))
    if len(extended_key) != len(text):
        extended_key += key[:len(text) - len(extended_key)]

    encrypted = ""

    for c1, c2 in zip(text, extended_key):
        match c1:
            case c if c in alphabet:
                replace = (alphabet.index(c) + alphabet.index(c2) + 1) % len(alphabet)
                encrypted += alphabet[replace]
            case c if c.lower() in alphabet:
                replace = (alphabet.index(c.lower()) + alphabet.index(c2) + 1) % len(alphabet)
                encrypted += alphabet[replace].upper()
            case _:
                encrypted += c1

    return encrypted


def decrypt_trithemius(text: str, alphabet: str, key: str) -> str:
    """
    Дешифрует текст, зашифрованный шифром Тритемиуса.
    :param text: зашифрованный текст
    :param alphabet: алфавит, используемый для шифрования
    :param key: ключевое слово для шифра
    :return: строка с дешифрованным текстом
    """
    if not text:
        raise ValueError("Text is empty")

    if not alphabet:
        raise ValueError("Alphabet is empty")

    alphabet = alphabet.lower()

    if not key:
        raise ValueError("Key is empty")

    key = key.lower()

    if not all(c in alphabet for c in key):
        raise ValueError("Key must contain characters from alphabet")

    extended_key = key * (len(text) // len(key))
    if len(extended_key) != len(text):
        extended_key += key[:len(text) - len(extended_key)]

    decrypted = ""

    for c1, c2 in zip(text, extended_key):
        match c1:
            case c if c in alphabet:
                replace = alphabet.index(c) - alphabet.index(c2) - 1
                decrypted += alphabet[replace]
            case c if c.lower() in alphabet:
                replace = alphabet.index(c.lower()) - alphabet.index(c2) - 1
                decrypted += alphabet[replace].upper()
            case _:
                decrypted += c1

    return decrypted


def get_frequency(text: str) -> dict:
    """
    Вычисляет частоту каждого символа в тексте.
    :param text: входной текст
    :return: словарь, в котором ключи - символы, а значения - их частоты
    """
    if not text:
        raise ValueError("Text is empty")

    freq_dict = {}

    for char in text:
        if char.lower() in freq_dict:
            freq_dict[char.lower()] += 1
        else:
            freq_dict[char.lower()] = 1

    for char, count in freq_dict.items():
        freq_dict[char] = count / len(text)

    return dict(sorted(freq_dict.items(), key=lambda item: item[1], reverse=True))


def get_key(freq_dict1: dict, freq_dict2: dict) -> dict:
    """
    Создаёт ключ путём сопоставления ключей из двух входных словарей.
    :param freq_dict1: словарь частот зашифрованного текста
    :param freq_dict2: словарь частот языка
    :return: словарь замен, в котором символы зашифрованного текста сопоставляются с
    наиболее вероятными оригинальными символами
    """
    if not freq_dict1:
        raise ValueError("Dictionary of ciphertext frequencies is empty")

    if not freq_dict2:
        raise ValueError("Dictionary of language frequencies is empty")

    return {k1: k2 for k1, k2 in zip(freq_dict1.keys(), freq_dict2.keys())}


def decrypt(text: str, key: dict) -> str:
    """
    Заменяет символы в тексте согласно переданному ключу.
    :param text: исходный текст
    :param key: словарь замен
    :return: новый текст, в котором символы заменены в соответствии с ключом
    """
    if not text:
        raise ValueError("Text is empty")

    if not key:
        raise ValueError("Dictionary of replacements is empty")

    decrypted = ""

    for char in text:
        decrypted_char = key.get(char.lower())
        if decrypted_char is None:
            decrypted_char = char.lower()
        decrypted += decrypted_char

    return decrypted
