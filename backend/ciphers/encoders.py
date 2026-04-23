"""
Encoders & decoders: Base64, Base32, Hex, Binary, URL, Morse.
© 2026 Aboubacar Sidick Meite (ApollonASM8977) — All Rights Reserved.
"""
import base64, binascii, urllib.parse

MORSE_ENC = {
    'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---',
    'K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-',
    'U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..',
    '0':'-----','1':'.----','2':'..---','3':'...--','4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.',
    ' ':'/'
}
MORSE_DEC = {v: k for k, v in MORSE_ENC.items()}


def base64_encode(text: str, **_) -> dict:
    out = base64.b64encode(text.encode()).decode()
    return {"output": out, "steps": [{"note": "Base64 encoding (RFC 4648)"}]}

def base64_decode(text: str, **_) -> dict:
    out = base64.b64decode(text.encode()).decode(errors="replace")
    return {"output": out, "steps": [{"note": "Base64 decoding"}]}

def base32_encode(text: str, **_) -> dict:
    out = base64.b32encode(text.encode()).decode()
    return {"output": out, "steps": [{"note": "Base32 encoding"}]}

def base32_decode(text: str, **_) -> dict:
    out = base64.b32decode(text.encode()).decode(errors="replace")
    return {"output": out, "steps": [{"note": "Base32 decoding"}]}

def hex_encode(text: str, **_) -> dict:
    out = binascii.hexlify(text.encode()).decode()
    steps = [{"char": c, "hex": format(ord(c), '02x')} for c in text[:50]]
    return {"output": out, "steps": steps}

def hex_decode(text: str, **_) -> dict:
    clean = text.replace(" ", "").replace("0x", "")
    out = binascii.unhexlify(clean).decode(errors="replace")
    return {"output": out, "steps": [{"note": "Hex decoding"}]}

def binary_encode(text: str, **_) -> dict:
    out = ' '.join(format(ord(c), '08b') for c in text)
    steps = [{"char": c, "binary": format(ord(c), '08b')} for c in text[:30]]
    return {"output": out, "steps": steps}

def binary_decode(text: str, **_) -> dict:
    parts = text.strip().split()
    out = ''.join(chr(int(b, 2)) for b in parts if b)
    return {"output": out, "steps": [{"note": f"{len(parts)} bytes decoded"}]}

def url_encode(text: str, **_) -> dict:
    out = urllib.parse.quote(text)
    return {"output": out, "steps": [{"note": "URL percent-encoding (RFC 3986)"}]}

def url_decode(text: str, **_) -> dict:
    out = urllib.parse.unquote(text)
    return {"output": out, "steps": [{"note": "URL percent-decoding"}]}

def morse_encode(text: str, **_) -> dict:
    words = text.upper().split(' ')
    out_words = []
    steps = []
    for word in words:
        coded = []
        for ch in word:
            m = MORSE_ENC.get(ch)
            if m:
                coded.append(m)
                steps.append({"char": ch, "morse": m})
        out_words.append(' '.join(coded))
    return {"output": ' / '.join(out_words), "steps": steps}

def morse_decode(text: str, **_) -> dict:
    words = text.strip().split(' / ')
    result = []
    steps = []
    for word in words:
        chars = word.strip().split(' ')
        for code in chars:
            ch = MORSE_DEC.get(code.strip(), '?')
            result.append(ch)
            steps.append({"morse": code, "char": ch})
        result.append(' ')
    return {"output": ''.join(result).strip(), "steps": steps}

