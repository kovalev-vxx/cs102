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
    id_symb = list()  # create list with symbols ID
    encrypt_ID = list()  # create list with encrypt symbols ID

    for i in plaintext:
        id_symb.append(ord(i))

    for i in id_symb:  # 65 - 90(A-Z), 97 - 122 (a-z)
        if 65 <= i <= (90 - shift):
            w = i + shift
            encrypt_ID.append(w)
        elif 97 <= i <= (122 - shift):
            w = i + shift
            encrypt_ID.append(w)
        elif (90 - shift) <= i <= 97:
            w = 90 - i
            encrypt_ID.append(64 + shift - w)
        elif (97 - shift) <= i <= 122:
            w = 122 - i
            encrypt_ID.append(96 + shift - w)
        else:
            encrypt_ID.append(i)

        encrypt_word = list()

        for m in encrypt_ID:  # transform ID to symbols
            encrypt_word.append(chr(m))

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
    id_symb = list()  # create list with symbols ID
    decrypt_ID = list()  # create list with decrypt symbols ID

    for m in ciphertext:
        id_symb.append(ord(m))

    for i in id_symb:  # 65 - 90(A-Z), 97 - 122 (a-z)
        if (65 + shift) <= i <= 90:
            w = i - shift
            decrypt_ID.append(w)
        elif (97 + shift) <= i <= 122:
            w = i - shift
            decrypt_ID.append(w)
        elif 65 <= i <= (65 + shift):
            w = abs(i - shift - 65)
            decrypt_ID.append(91 - w)
        elif 97 <= i <= (97 + shift):
            w = abs(i - shift - 97)
            decrypt_ID.append(123 - w)
        else:
            decrypt_ID.append(i)

    decrypt_word = list()

    for i in decrypt_ID:  # transform ID to symbols
        decrypt_word.append(chr(i))

    plaintext = "".join(decrypt_word)

    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0

    return best_shift
