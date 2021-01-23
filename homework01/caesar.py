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
    >>> d = {"python", "java", "ruby"}
    >>> caesar_breaker("python", d)
    0
    >>> caesar_breaker("sbwkrq", d)
    3
    """
    best_shift = 0
    ciphertext = ciphertext.split()  # type: ignore
    shift = 0
    max_score = 0
    en_alphabet_count = 26

    while shift < en_alphabet_count:
        score = 0
        shift += 1
        check_words = [decrypt_caesar(word, shift) for word in ciphertext]
        for i in check_words:
            if i in dictionary:
                score += 1

        if max_score < score:
            max_score = score
            best_shift = shift

    return best_shift
