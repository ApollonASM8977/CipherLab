"""
CipherLab API â€” FastAPI backend.
Â© 2026 Aboubacar Sidick Meite (ApollonASM8977) â€” All Rights Reserved.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Any

from ciphers import classical, modern, asymmetric, encoders

app = FastAPI(title="CipherLab API", version="1.0.0")
app.add_middleware(CORSMiddleware,
    allow_origins=["http://localhost:5173","http://localhost:5174","http://127.0.0.1:5173"],
    allow_methods=["*"], allow_headers=["*"])


class ProcessRequest(BaseModel):
    cipher: str
    mode: str = "encrypt"
    text: str = Field(..., min_length=1, max_length=10000)
    params: dict[str, Any] = {}


@app.get("/")
def root(): return {"name": "CipherLab API", "version": "1.0.0"}


@app.get("/ciphers")
def list_ciphers():
    return {"ciphers": [
        # Classical
        {"id":"caesar",       "name":"Caesar",          "category":"classical", "modes":["encrypt","decrypt"], "params":[{"key":"shift","type":"number","default":3,"min":1,"max":25,"label":"Shift"}]},
        {"id":"rot13",        "name":"ROT13",            "category":"classical", "modes":["encrypt"],           "params":[]},
        {"id":"atbash",       "name":"Atbash",           "category":"classical", "modes":["encrypt"],           "params":[]},
        {"id":"vigenere",     "name":"VigenÃ¨re",         "category":"classical", "modes":["encrypt","decrypt"], "params":[{"key":"key","type":"text","default":"SECRET","label":"Keyword"}]},
        {"id":"polysubcipher","name":"PolySubCipher",    "category":"classical", "modes":["encrypt","decrypt"], "params":[]},
        {"id":"rail-fence",   "name":"Rail Fence",       "category":"classical", "modes":["encrypt","decrypt"], "params":[{"key":"rails","type":"number","default":3,"min":2,"max":10,"label":"Rails"}]},
        # Modern
        {"id":"aes-256-gcm",  "name":"AES-256-GCM",     "category":"modern",    "modes":["encrypt","decrypt"], "params":[{"key":"key","type":"key","label":"Key (Base64, 32 bytes)","generate":True}]},
        {"id":"aes-128-cbc",  "name":"AES-128-CBC",     "category":"modern",    "modes":["encrypt","decrypt"], "params":[{"key":"key","type":"key","label":"Key (Base64, 16 bytes)","generate":True}]},
        {"id":"des-cbc",      "name":"DES-CBC",          "category":"modern",    "modes":["encrypt","decrypt"], "params":[{"key":"key","type":"key","label":"Key (Base64, 8 bytes)","generate":True,"warning":"DES is weak â€” educational only"}]},
        {"id":"3des-cbc",     "name":"3DES-CBC",         "category":"modern",    "modes":["encrypt","decrypt"], "params":[{"key":"key","type":"key","label":"Key (Base64, 24 bytes)","generate":True}]},
        # Asymmetric
        {"id":"rsa-2048",     "name":"RSA-2048",         "category":"asymmetric","modes":["encrypt","decrypt"], "params":[
            {"key":"public_key","type":"textarea","label":"Public Key (PEM)","forMode":"encrypt"},
            {"key":"private_key","type":"textarea","label":"Private Key (PEM)","forMode":"decrypt"},
        ], "generateKeypair": True},
        # Encoders
        {"id":"base64",   "name":"Base64",       "category":"encoder", "modes":["encode","decode"], "params":[]},
        {"id":"base32",   "name":"Base32",       "category":"encoder", "modes":["encode","decode"], "params":[]},
        {"id":"hex",      "name":"Hexadecimal",  "category":"encoder", "modes":["encode","decode"], "params":[]},
        {"id":"binary",   "name":"Binary",       "category":"encoder", "modes":["encode","decode"], "params":[]},
        {"id":"url",      "name":"URL Encoding", "category":"encoder", "modes":["encode","decode"], "params":[]},
        {"id":"morse",    "name":"Morse Code",   "category":"encoder", "modes":["encode","decode"], "params":[]},
    ]}


@app.post("/process")
def process(req: ProcessRequest):
    c, m, t, p = req.cipher, req.mode, req.text, req.params
    try:
        # Classical
        if c == "caesar":       r = classical.caesar(t, int(p.get("shift",3)), m)
        elif c == "rot13":      r = classical.rot13(t)
        elif c == "atbash":     r = classical.atbash(t)
        elif c == "vigenere":   r = classical.vigenere(t, p.get("key","secret"), m)
        elif c == "polysubcipher": r = classical.polysubcipher(t, m)
        elif c == "rail-fence": r = classical.rail_fence(t, int(p.get("rails",3)), m)
        # Modern
        elif c == "aes-256-gcm": r = modern.aes_256_gcm(t, p["key"], m)
        elif c == "aes-128-cbc": r = modern.aes_128_cbc(t, p["key"], m)
        elif c == "des-cbc":     r = modern.des_cbc(t, p["key"], m)
        elif c == "3des-cbc":    r = modern.triple_des_cbc(t, p["key"], m)
        # Asymmetric
        elif c == "rsa-2048":
            if m == "encrypt": r = asymmetric.rsa_encrypt(t, p["public_key"])
            else:              r = asymmetric.rsa_decrypt(t, p["private_key"])
        # Encoders
        elif c == "base64":  r = encoders.base64_encode(t) if m=="encode" else encoders.base64_decode(t)
        elif c == "base32":  r = encoders.base32_encode(t) if m=="encode" else encoders.base32_decode(t)
        elif c == "hex":     r = encoders.hex_encode(t)    if m=="encode" else encoders.hex_decode(t)
        elif c == "binary":  r = encoders.binary_encode(t) if m=="encode" else encoders.binary_decode(t)
        elif c == "url":     r = encoders.url_encode(t)    if m=="encode" else encoders.url_decode(t)
        elif c == "morse":   r = encoders.morse_encode(t)  if m=="encode" else encoders.morse_decode(t)
        else: raise HTTPException(400, f"Unknown cipher: {c}")
        return {"cipher": c, "mode": m, "input": t, **r}
    except HTTPException: raise
    except Exception as e: raise HTTPException(400, str(e))


@app.post("/generate-key")
def generate_key(body: dict):
    cipher_id = body.get("cipher","aes-256-gcm")
    try:
        if cipher_id == "rsa-2048":
            return asymmetric.generate_rsa_keypair()
        return modern.generate_key(cipher_id)
    except Exception as e:
        raise HTTPException(400, str(e))

