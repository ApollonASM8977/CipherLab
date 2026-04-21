"""
Classical substitution & transposition ciphers.
Â© 2026 Aboubacar Sidick Meite (ApollonASM8977) â€” All Rights Reserved.
"""
import string

ALPHA = string.ascii_lowercase
POLY_KEY_A = "tuvwxyzabcdefghijklmnopqrs"
POLY_KEY_B = "fghijklmnopqrstuvwxyzabcde"
POLY_DEC_A = "hijklmnopqrstuvwxyzabcdefg"
POLY_DEC_B = "vwxyzabcdefghijklmnopqrstu"

MORSE = {
    'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---',
    'K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-',
    'U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..',
    '0':'-----','1':'.----','2':'..---','3':'...--','4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.',
    ' ':'/'
}
MORSE_REV = {v: k for k, v in MORSE.items()}


# â”€â”€ Caesar â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def caesar(text: str, shift: int, mode: str) -> dict:
    if mode == "decrypt": shift = -shift
    result, steps = [], []
    for ch in text:
        low = ch.lower()
        if low in ALPHA:
            idx = (ALPHA.index(low) + shift) % 26
            out = ALPHA[idx]
            steps.append({"input": low, "output": out, "note": f"shift {shift:+d}"})
            result.append(out)
        else:
            steps.append({"input": ch, "output": ch, "note": "pass"})
            result.append(ch)
    return {"output": "".join(result), "steps": steps}


# â”€â”€ ROT13 â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def rot13(text: str, **_) -> dict:
    r = caesar(text, 13, "encrypt")
    return r


# â”€â”€ Atbash â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def atbash(text: str, **_) -> dict:
    result, steps = [], []
    for ch in text:
        low = ch.lower()
        if low in ALPHA:
            out = ALPHA[25 - ALPHA.index(low)]
            steps.append({"input": low, "output": out, "note": "mirror"})
            result.append(out)
        else:
            steps.append({"input": ch, "output": ch, "note": "pass"})
            result.append(ch)
    return {"output": "".join(result), "steps": steps}


# â”€â”€ VigenÃ¨re â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def vigenere(text: str, key: str, mode: str) -> dict:
    key = ''.join(c for c in key.lower() if c in ALPHA) or "key"
    result, steps, ki = [], [], 0
    for ch in text:
        low = ch.lower()
        if low in ALPHA:
            kshift = ALPHA.index(key[ki % len(key)])
            shift = kshift if mode == "encrypt" else -kshift
            out = ALPHA[(ALPHA.index(low) + shift) % 26]
            steps.append({"input": low, "output": out, "key_char": key[ki % len(key)], "shift": shift})
            result.append(out)
            ki += 1
        else:
            steps.append({"input": ch, "output": ch, "note": "pass"})
            result.append(ch)
    return {"output": "".join(result), "steps": steps}


# â”€â”€ PolySubCipher (original) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def polysubcipher(text: str, mode: str) -> dict:
    enc_keys = {1: POLY_KEY_A, 2: POLY_KEY_A, 3: POLY_KEY_B, 4: POLY_KEY_A}
    dec_keys = {1: POLY_DEC_A, 2: POLY_DEC_A, 3: POLY_DEC_B, 4: POLY_DEC_A}
    keys = enc_keys if mode == "encrypt" else dec_keys
    result, steps, pos = [], [], 0
    for ch in text:
        low = ch.lower()
        if low in ALPHA:
            pos += 1
            cycle = ((pos - 1) % 4) + 1
            tbl = keys[cycle]
            out = tbl[ALPHA.index(low)]
            steps.append({"input": low, "output": out, "position": pos, "key": f"KEY_{'B' if cycle==3 else 'A'}", "cycle": cycle})
            result.append(out)
        else:
            steps.append({"input": ch, "output": ch, "note": "pass"})
            result.append(ch)
    return {"output": "".join(result), "steps": steps}


# â”€â”€ Rail Fence â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def rail_fence(text: str, rails: int, mode: str) -> dict:
    if rails < 2: rails = 2
    if mode == "encrypt":
        fence = [[] for _ in range(rails)]
        rail, direction = 0, 1
        for ch in text:
            fence[rail].append(ch)
            if rail == 0: direction = 1
            elif rail == rails - 1: direction = -1
            rail += direction
        output = "".join("".join(r) for r in fence)
        steps = [{"rail": i, "chars": "".join(fence[i])} for i in range(rails)]
    else:
        n = len(text)
        pattern = []
        rail, direction = 0, 1
        for i in range(n):
            pattern.append(rail)
            if rail == 0: direction = 1
            elif rail == rails - 1: direction = -1
            rail += direction
        indices = sorted(range(n), key=lambda i: (pattern[i], i))
        result = [''] * n
        for pos, ch in zip(indices, text):
            result[pos] = ch
        output = "".join(result)
        steps = [{"note": f"Deciphered with {rails} rails"}]
    return {"output": output, "steps": steps}

