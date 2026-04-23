"""
RSA-2048 asymmetric encryption.
© 2026 Aboubacar Sidick Meite (ApollonASM8977) — All Rights Reserved.
"""
import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend


def generate_rsa_keypair() -> dict:
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    priv_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode()
    pub_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode()
    return {"private_key": priv_pem, "public_key": pub_pem}


def rsa_encrypt(text: str, public_key_pem: str) -> dict:
    pub = serialization.load_pem_public_key(public_key_pem.encode(), backend=default_backend())
    ct = pub.encrypt(
        text.encode(),
        padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
    )
    return {
        "output": base64.b64encode(ct).decode(),
        "steps": [{"note": "RSA-2048 OAEP-SHA256 encryption with public key"}],
    }


def rsa_decrypt(ciphertext_b64: str, private_key_pem: str) -> dict:
    priv = serialization.load_pem_private_key(private_key_pem.encode(), password=None, backend=default_backend())
    ct = base64.b64decode(ciphertext_b64)
    pt = priv.decrypt(
        ct,
        padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
    )
    return {
        "output": pt.decode(),
        "steps": [{"note": "RSA-2048 OAEP-SHA256 decryption with private key ✓"}],
    }

