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

    # -----------GET KEY------------#
    s = list(keyword)  # create list keyword
    key = ""
    i = 0

    if len(ciphertext) > len(keyword):
        div = len(ciphertext) // len(keyword)
        time_word = keyword * div
        dif = len(ciphertext) - len(time_word)  # difference between ciphertext and time_word
        a = list(time_word)  # create list time_word
        while i < dif:
            a.append(a[i])
            i += 1
        key = "".join(a)
    elif len(ciphertext) < len(keyword):
        len_key = len(ciphertext)
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

    for m in ciphertext:  # fill symbols ID list
        id_symb.append(ord(m))

    # -------GET DECRYPT WORD------- #

    ciph = list()

    for x, y in zip(id_symb, shifts):  # 65 - 90(A-Z), 97 - 122 (a-z)
        if (65 + y) <= x <= 90:
            w = x - y
            ciph.append(w)
        elif (97 + y) <= x <= 122:
            w = x - y
            ciph.append(w)
        elif 65 <= x <= (65 + y):
            w = abs(x - y - 65)
            ciph.append(91 - w)
        elif 97 <= x <= (97 + y):
            w = abs(x - y - 97)
            ciph.append(123 - w)
        else:
            ciph.append(x)

    decrypt_word = list()

    for m in ciph:
        decrypt_word.append(chr(m))

    plaintext = "".join(decrypt_word)

    # ------------------------- #

    return plaintext
