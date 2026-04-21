"""
Modern symmetric ciphers: AES-256-GCM, AES-128-CBC, DES, 3DES.
Â© 2026 Aboubacar Sidick Meite (ApollonASM8977) â€” All Rights Reserved.
"""
import base64, os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


def _pad(data: bytes, block_size: int) -> bytes:
    p = padding.PKCS7(block_size * 8).padder()
    return p.update(data) + p.finalize()

def _unpad(data: bytes, block_size: int) -> bytes:
    u = padding.PKCS7(block_size * 8).unpadder()
    return u.update(data) + u.finalize()

def _b64(b: bytes) -> str: return base64.b64encode(b).decode()
def _ub64(s: str) -> bytes: return base64.b64decode(s)


# â”€â”€ AES-256-GCM â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def aes_256_gcm(text: str, key_b64: str, mode: str) -> dict:
    key = _ub64(key_b64)
    if len(key) != 32:
        raise ValueError("AES-256 key must be 32 bytes (base64-encoded)")
    if mode == "encrypt":
        iv = os.urandom(12)
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
        enc = cipher.encryptor()
        ct = enc.update(text.encode()) + enc.finalize()
        tag = enc.tag
        payload = _b64(iv) + "." + _b64(ct) + "." + _b64(tag)
        return {"output": payload, "steps": [{"iv": _b64(iv), "tag": _b64(tag), "note": "AES-256-GCM authenticated encryption"}]}
    else:
        parts = text.split(".")
        if len(parts) != 3: raise ValueError("Invalid AES-GCM ciphertext format (expected iv.ct.tag)")
        iv, ct, tag = _ub64(parts[0]), _ub64(parts[1]), _ub64(parts[2])
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
        dec = cipher.decryptor()
        pt = dec.update(ct) + dec.finalize()
        return {"output": pt.decode(), "steps": [{"note": "AES-256-GCM authenticated decryption â€” tag verified âœ“"}]}


# â”€â”€ AES-128-CBC â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def aes_128_cbc(text: str, key_b64: str, mode: str) -> dict:
    key = _ub64(key_b64)
    if len(key) != 16: raise ValueError("AES-128 key must be 16 bytes (base64-encoded)")
    if mode == "encrypt":
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        enc = cipher.encryptor()
        ct = enc.update(_pad(text.encode(), 16)) + enc.finalize()
        return {"output": _b64(iv) + "." + _b64(ct), "steps": [{"iv": _b64(iv), "note": "AES-128-CBC encryption"}]}
    else:
        parts = text.split(".")
        if len(parts) != 2: raise ValueError("Invalid AES-CBC ciphertext (expected iv.ct)")
        iv, ct = _ub64(parts[0]), _ub64(parts[1])
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        dec = cipher.decryptor()
        pt = _unpad(dec.update(ct) + dec.finalize(), 16)
        return {"output": pt.decode(), "steps": [{"note": "AES-128-CBC decryption âœ“"}]}


# â”€â”€ DES-CBC â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def des_cbc(text: str, key_b64: str, mode: str) -> dict:
    key = _ub64(key_b64)
    if len(key) != 8: raise ValueError("DES key must be 8 bytes (base64-encoded)")
    if mode == "encrypt":
        iv = os.urandom(8)
        cipher = Cipher(algorithms.TripleDES(key * 3), modes.CBC(iv), backend=default_backend())
        enc = cipher.encryptor()
        ct = enc.update(_pad(text.encode(), 8)) + enc.finalize()
        return {"output": _b64(iv) + "." + _b64(ct), "steps": [{"iv": _b64(iv), "note": "DES-CBC encryption (educational â€” not secure)"}]}
    else:
        parts = text.split(".")
        if len(parts) != 2: raise ValueError("Invalid DES ciphertext (expected iv.ct)")
        iv, ct = _ub64(parts[0]), _ub64(parts[1])
        cipher = Cipher(algorithms.TripleDES(key * 3), modes.CBC(iv), backend=default_backend())
        dec = cipher.decryptor()
        pt = _unpad(dec.update(ct) + dec.finalize(), 8)
        return {"output": pt.decode(), "steps": [{"note": "DES-CBC decryption âœ“"}]}


# â”€â”€ 3DES-CBC â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def triple_des_cbc(text: str, key_b64: str, mode: str) -> dict:
    key = _ub64(key_b64)
    if len(key) != 24: raise ValueError("3DES key must be 24 bytes (base64-encoded)")
    if mode == "encrypt":
        iv = os.urandom(8)
        cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=default_backend())
        enc = cipher.encryptor()
        ct = enc.update(_pad(text.encode(), 8)) + enc.finalize()
        return {"output": _b64(iv) + "." + _b64(ct), "steps": [{"iv": _b64(iv), "note": "3DES-CBC encryption"}]}
    else:
        parts = text.split(".")
        if len(parts) != 2: raise ValueError("Invalid 3DES ciphertext (expected iv.ct)")
        iv, ct = _ub64(parts[0]), _ub64(parts[1])
        cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=default_backend())
        dec = cipher.decryptor()
        pt = _unpad(dec.update(ct) + dec.finalize(), 8)
        return {"output": pt.decode(), "steps": [{"note": "3DES-CBC decryption âœ“"}]}


# â”€â”€ Key generators â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def generate_key(cipher_id: str) -> dict:
    sizes = {"aes-256-gcm": 32, "aes-128-cbc": 16, "des-cbc": 8, "3des-cbc": 24}
    size = sizes.get(cipher_id)
    if not size: raise ValueError(f"Unknown cipher: {cipher_id}")
    return {"key": _b64(os.urandom(size)), "size_bytes": size, "encoding": "base64"}

