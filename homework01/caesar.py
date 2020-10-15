import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    id_symbol = []
    encrypt_id = []

    for i in plaintext:
        id_symbol.append(ord(i))

    for id in id_symbol:  # 65 - 90(A-Z), 97 - 122 (a-z)
        if 65 <= id <= (90 - shift):
            w = id + shift
            encrypt_id.append(w)
        elif 97 <= id <= (122 - shift):
            w = id + shift
            encrypt_id.append(w)
        elif (90 - shift) <= id <= 97:
            w = 90 - id
            encrypt_id.append(64 + shift - w)
        elif (97 - shift) <= id <= 122:
            w = 122 - id
            encrypt_id.append(96 + shift - w)
        else:
            encrypt_id.append(id)

        encrypt_word = []

        for ID in encrypt_id:  # transform ID to symbols
            encrypt_word.append(chr(ID))

        ciphertext = "".join(encrypt_word)

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    id_symbol = []
    decrypt_id = []

    for symbol in ciphertext:
        id_symbol.append(ord(symbol))

    for id in id_symbol:  # 65 - 90(A-Z), 97 - 122 (a-z)
        if (65 + shift) <= id <= 90:
            w = id - shift
            decrypt_id.append(w)
        elif (97 + shift) <= id <= 122:
            w = id - shift
            decrypt_id.append(w)
        elif 65 <= id <= (65 + shift):
            w = abs(id - shift - 65)
            decrypt_id.append(91 - w)
        elif 97 <= id <= (97 + shift):
            w = abs(id- shift - 97)
            decrypt_id.append(123 - w)
        else:
            decrypt_id.append(id)

    decrypt_word = []

    for ID in decrypt_id:  # transform ID to symbols
        decrypt_word.append(chr(ID))

    plaintext = "".join(decrypt_word)

    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0

    return best_shift
