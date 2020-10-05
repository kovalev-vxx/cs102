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
        if i.isupper() and i.isalpha() and ord(i) > 90 - shift:  # 65 - 90(A-Z), 97 - 122 (a-z)
            a = 90 - ord(i)
            ciphertext += chr(a + 65)
        elif i.isupper() and i.isalpha():
            a = ord(i)
            ciphertext += chr(a + shift)
        elif i.lower() and ord(i) > 122 - shift and i.isalpha():
            a = 122 - ord(i)
            ciphertext += chr(a + 97)
        elif i.lower() and i.isalpha():
            a = ord(i)
            ciphertext += chr(a + shift)
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
        if i.isupper() and i.isalpha() and ord(i) - shift >= 65:  # 65 - 90(A-Z), 97 - 122 (a-z)
            a = ord(i) - shift
            plaintext += chr(a)
        elif i.isupper() and i.isalpha():
            a = 90 - ord(i)
            plaintext += chr(a + 65)
        elif i.islower() and i.isalpha() and ord(i) - shift >= 97:
            a = ord(i) - shift
            plaintext += chr(a)
        elif i.islower() and i.isalpha():
            a = 122 - ord(i)
            plaintext += chr(a + 97)
        else:
            plaintext += i

    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
