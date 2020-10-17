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

    for i in plaintext:
        if ord("A") <= ord(i) <= (ord("Z") - shift):
            ciphertext += chr(ord(i) + shift)
        elif ord("a") <= ord(i) <= (ord("z") - shift):
            ciphertext += chr(ord(i) + shift)
        elif (ord("Z") - shift) <= ord(i) <= ord("a"):
            ciphertext += chr(ord("A") + shift - ord("Z") + ord(i) - 1)
        elif (ord("a") - shift) <= ord(i) <= ord("z"):
            ciphertext += chr(ord("a") + shift - ord("z") + ord(i) - 1)
        else:
            ciphertext += i

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

    for i in ciphertext:
        if (ord("A") + shift) <= ord(i) <= ord("Z"):
            plaintext += chr(ord(i) - shift)
        elif (ord("a") + shift) <= ord(i) <= ord("z"):
            plaintext += chr(ord(i) - shift)
        elif ord("A") <= ord(i) <= (ord("A") + shift):
            plaintext += chr(ord("Z") - abs(ord(i) - shift - ord("A")) + 1)
        elif ord("a") <= ord(i) <= (ord("a") + shift):
            plaintext += chr(ord("z") - abs(ord(i) - shift - ord("a")) + 1)
        else:
            plaintext += i

    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0

    return best_shift