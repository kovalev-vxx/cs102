def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """

    ciphertext = ""

    if len(plaintext) > len(keyword):
        key = (keyword * (1 + (len(plaintext) // len(keyword)))).lower()
    else:
        key = keyword.lower()

    shifts = []

    for i in key:
        shifts.append(ord(i) - 97)

    for i, m in zip(plaintext, shifts):
        if ord("A") <= ord(i) <= ord("Z") - m:
            w = ord(i) + m
            ciphertext += chr(w)
        elif ord("a") <= ord(i) <= ord("z") - m:
            w = ord(i) + m
            ciphertext += chr(w)
        elif ord("Z") - m <= ord(i) <= ord("a"):
            w = ord("Z") - ord(i)
            ciphertext += chr(ord('A') - 1 + m - w)
        elif ord("a") - m <= ord(i) <= ord("z"):
            w = ord("z") - ord(i)
            ciphertext += chr(ord("a") - 1 + m - w)
        else:
            ciphertext += i

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""

    if len(ciphertext) > len(keyword):
        key = (keyword * (1 + (len(ciphertext) // len(keyword)))).lower()
    else:
        key = keyword.lower()

    shifts = []
    k = 0

    for i in key:
        k += 1
        if k > len(ciphertext):
            break
        else:
            shifts.append(ord(i) - 97)

    for i, m in zip(ciphertext, shifts):
        if ord("A") + m <= ord(i) <= ord("Z"):
            plaintext += chr(ord(i) - m)
        elif ord("a") + m <= ord(i) <= ord("z"):
            plaintext += chr(ord(i) - m)
        elif ord("A") <= ord(i) <= ord("A") + m:
            plaintext += chr(ord("Z") + 1 - abs(ord(i) - m - ord("A")))
        elif ord("a") <= ord(i) <= ord("a") + m:
            plaintext += chr(ord("z") + 1 - abs(ord(i) - m - ord("a")))
        else:
            plaintext += i

    return plaintext
