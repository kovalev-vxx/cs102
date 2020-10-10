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

    s = list(keyword)  # create list keyword
    key = ''
    i = 0
    # -----------GET KEY------------#
    if len(plaintext) > len(keyword):
        div = len(plaintext) // len(keyword)
        time_word = keyword * div
        dif = len(plaintext) - len(time_word)  # difference between plainttext and time_word
        a = list(time_word)  # create list time_word
        while i < dif:
            a.append(a[i])
            i += 1
        key = ''.join(a)
    elif len(plaintext) < len(keyword):
        len_key = len(plaintext)
        for i in range(0, len_key):
            key += s[i]
    else:
        key = keyword
    # -----------------------------#

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
    # PUT YOUR CODE HERE
    return plaintext
