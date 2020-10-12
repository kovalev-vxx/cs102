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
    key = ""
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
        key = "".join(a)
    elif len(plaintext) < len(keyword):
        len_key = len(plaintext)
        for i in range(0, len_key):
            key += s[i]
    else:
        key = keyword
    # -----------------------------#

    key = key.lower()  # transform key to lower register

    id_symb = list()  # create list with symbols ID
    shifts = list()  # create list with shifts

    for m in key:
        shifts.append(ord(m) - 97)  # fill shifts list

    for m in plaintext:  # fill symbols ID list
        id_symb.append(ord(m))

    # ---------------GET ENCRYPT WORD-------------- #

    ciph = list()

    for x, y in zip(id_symb, shifts):  # 65 - 90(A-Z), 97 - 122 (a-z)
        if 65 <= x <= (90 - y):
            w = x + y
            ciph.append(w)
        elif 97 <= x <= (122 - y):
            w = x + y
            ciph.append(w)
        elif (90 - y) <= x <= 97:
            w = 90 - x
            ciph.append(64 + y - w)
        elif (97 - y) <= x <= 122:
            w = 122 - x
            ciph.append(96 + y - w)
        else:
            ciph.append(x)

    encrypt_word = list()

    for m in ciph:
        encrypt_word.append(chr(m))

    ciphertext = "".join(encrypt_word)

    # ----------------------------- #

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
