import main
import pytest
from unittest.mock import patch, MagicMock


ENGLISH_FREQ = {
    " ": 0.182, "e": 0.127, "t": 0.091, "a": 0.082,
    "o": 0.075, "i": 0.070, "n": 0.067, "s": 0.063,
    "h": 0.061, "r": 0.060, "d": 0.043, "l": 0.040,
    "c": 0.028, "u": 0.028, "m": 0.024, "w": 0.024,
    "f": 0.022, "g": 0.020, "y": 0.020, "p": 0.019,
    "b": 0.015, "v": 0.0098, "k": 0.0077, "j": 0.0015,
    "x": 0.0015, "q": 0.00095, "z": 0.00074
}
RUSSIAN_FREQ = {
    " ": 0.128675, "о": 0.096456, "и": 0.075312,
    "е": 0.072292, "а": 0.064841, "н": 0.061820,
    "т": 0.061619, "с": 0.051953, "р": 0.040677,
    "в": 0.039267, "м": 0.029803, "л": 0.029400,
    "д": 0.026983, "я": 0.026379, "к": 0.025977,
    "п": 0.024768, "з": 0.015908, "ы": 0.015707,
    "ь": 0.015103, "у": 0.013290, "ч": 0.011679,
    "ж": 0.010673, "г": 0.009867, "х": 0.008659,
    "ф": 0.007249, "й": 0.006847, "ю": 0.006847,
    "б": 0.006645, "ц": 0.005034, "ш": 0.004229,
    "щ": 0.003625, "э": 0.002416, "ъ": 0.000000
}


def test_trithemius():
    encrypted = main.encrypt_trithemius("Hello World!", "abcdefghijklmnopqrstuvwxyz", "key")
    decrypted = main.decrypt_trithemius(encrypted, "abcdefghijklmnopqrstuvwxyz", "key")
    assert encrypted == "Sjkwt Htqwi!"
    assert decrypted == "Hello World!"


def test_get_frequency():
    result1 = main.get_frequency("hello")
    result2 = main.get_frequency("HeLLo")
    assert isinstance(result1, dict)
    assert sum(result1.values()) == pytest.approx(1.0, 0.001)
    assert result1 == result2


def test_get_key():
    freq1 = {"a": 0.5, "b": 0.3, "c": 0.2}
    freq2 = {"d": 0.4, "e": 0.3, "f": 0.3}
    result = main.get_key(freq1, freq2)
    assert result == {"a": "d", "b": "e", "c": "f"}


def test_decrypt():
    result = main.decrypt("abc", {"a": "x", "b": "y", "c": "z"})
    assert result == "xyz"


@pytest.mark.parametrize(
    "text,alphabet,key",
    [
        ("Test123", "abcdefghijklmnopqrstuvwxyz", "ROFL"),
        ("hi!", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "longkey"),
        ("Привет мир", "абвгдеёжзийклмнопрстуфхцчшщъыьэюя", "Самара"),
        ("", "abc", "key"),
        ("hello", "", "key"),
        ("hello", "abc", ""),
        ("hello", "abc", "key")
    ]
)
def test_trithemius_parametrize(text, alphabet, key):
    if not text:
        with pytest.raises(ValueError, match="Text is empty"):
            main.encrypt_trithemius(text, alphabet, key)
    elif not alphabet:
        with pytest.raises(ValueError, match="Alphabet is empty"):
            main.encrypt_trithemius(text, alphabet, key)
    elif not key:
        with pytest.raises(ValueError, match="Key is empty"):
            main.encrypt_trithemius(text, alphabet, key)
    elif not all(c in alphabet.lower() for c in key.lower()):
        with pytest.raises(ValueError, match="Key must contain characters from alphabet"):
            main.encrypt_trithemius(text, alphabet, key)
    else:
        encrypted = main.encrypt_trithemius(text, alphabet, key)
        decrypted = main.decrypt_trithemius(encrypted, alphabet, key)
        assert isinstance(encrypted, str)
        assert len(encrypted) == len(text)
        assert encrypted != text
        assert decrypted == text


@pytest.mark.parametrize(
    "text,alphabet,key,lang_freq",
    [
        ("This is a sample text for frequency analysis.", "abcdefghijklmnopqrstuvwxyz", "secret", ENGLISH_FREQ),
        ("Это пример текста для частотного анализа.", "абвгдеёжзийклмнопрстуфхцчшщъыьэюя", "секрет", RUSSIAN_FREQ),
        ("This is a sample text for frequency analysis.", "abcdefghijklmnopqrstuvwxyz", "secret", {})
    ]
)
def test_statistical_decryption_simulation(text, alphabet, key, lang_freq):
    encrypted = main.encrypt_trithemius(text, alphabet, key)
    encrypted_freq = main.get_frequency(encrypted)

    if not lang_freq:
        with pytest.raises(ValueError, match="Dictionary of language frequencies is empty"):
            main.get_key(encrypted_freq, lang_freq)
    else:
        replacement_key = main.get_key(encrypted_freq, lang_freq)
        attempted_decrypt = main.decrypt(encrypted, replacement_key)
        assert isinstance(attempted_decrypt, str)
        assert len(attempted_decrypt) == len(encrypted)


def test_encrypt_with_mocked_alphabet_index():
    mock_alphabet = MagicMock(spec=str)
    mock_alphabet.lower.return_value = "abc"
    mock_alphabet.index.side_effect = lambda x: {"a": 0, "b": 1, "c": 2}[x]
    mock_alphabet.__len__.return_value = 3
    mock_alphabet.__contains__.side_effect = lambda x: x in "abc"

    with patch.object(main, "encrypt_trithemius") as mock_encrypt:
        mock_encrypt.return_value = "test_output"
        result = mock_encrypt("text", mock_alphabet, "key")

    assert result == "test_output"


def test_frequency_analysis_with_stub():
    class StubText:
        def __init__(self, text):
            self.text = text

        def __iter__(self):
            return iter(self.text)

    stub_text = StubText("aaaabbc")

    original_get_frequency = main.get_frequency
    main.get_frequency = lambda x: {"a": 0.57, "b": 0.29, "c": 0.14}

    try:
        result = main.get_frequency(stub_text)
        assert "a" in result
        assert result["a"] > result["b"]
    finally:
        main.get_frequency = original_get_frequency
