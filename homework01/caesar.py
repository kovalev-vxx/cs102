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
    id_symbols = []
    encrypt_id = []

    for i in plaintext:
        id_symbols.append(ord(i))

    for i in id_symbols:
        if ord("A") <= i <= (ord("Z") - shift):
            w = i + shift
            encrypt_id.append(w)
        elif ord("a") <= i <= (ord("z") - shift):
            w = i + shift
            encrypt_id.append(w)
        elif (ord("Z") - shift) <= i <= ord("a"):
            w = ord("Z") - i
            encrypt_id.append(ord("A") + shift - w - 1)
        elif (ord("a") - shift) <= i <= ord("z"):
            w = ord("z") - i
            encrypt_id.append(ord("a") + shift - w - 1)
        else:
            encrypt_id.append(i)

        encrypt_word = []

        for i in encrypt_id:  # transform ID to symbols
            encrypt_word.append(chr(i))

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
    id_symbols = []
    decrypt_id = []

    for i in ciphertext:
        id_symbols.append(ord(i))

    for i in id_symbols:  # 65 - 90(A-Z), 97 - 122 (a-z)
        if (ord("A") + shift) <= i <= ord("Z"):
            w = i - shift
            decrypt_id.append(w)
        elif (ord("a") + shift) <= i <= ord("z"):
            w = i - shift
            decrypt_id.append(w)
        elif ord("A") <= i <= (ord("A") + shift):
            w = abs(i - shift - ord("A"))
            decrypt_id.append(ord("Z") - w + 1)
        elif ord("a") <= i <= (ord("a") + shift):
            w = abs(i - shift - ord("a"))
            decrypt_id.append(ord("z") - w + 1)
        else:
            decrypt_id.append(i)

    decrypt_word = []

    for i in decrypt_id:  # transform ID to symbols
        decrypt_word.append(chr(i))

    plaintext = "".join(decrypt_word)

    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0

    return best_shift
