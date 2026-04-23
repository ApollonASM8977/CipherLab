# 🔬 CipherLab

> Full cryptography toolkit — classical ciphers, modern encryption, asymmetric keys & encoders.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)
![React](https://img.shields.io/badge/Frontend-React%2018-61DAFB?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript)
![License](https://img.shields.io/badge/License-Proprietary-red)
![Ciphers](https://img.shields.io/badge/Ciphers-16-green)

---

## What is CipherLab?

CipherLab is a full-stack web application that brings together **16 cryptographic tools** in one clean terminal-style interface.  
Select any cipher, enter your text, configure parameters, and get instant results with step-by-step traces.

---

## Features

### ⚙️ Classical Ciphers
| Cipher | Description |
|---|---|
| Caesar | Shift cipher with configurable offset (1–25) |
| ROT13 | Caesar with shift 13 — self-inverse |
| Atbash | Mirror alphabet substitution |
| Vigenère | Keyword-based polyalphabetic cipher |
| PolySubCipher | 2-key alternating substitution (original algorithm) |
| Rail Fence | Transposition cipher with configurable rails |

### 🔒 Modern Symmetric
| Cipher | Description |
|---|---|
| AES-256-GCM | Authenticated encryption — industry standard |
| AES-128-CBC | AES with 128-bit key in CBC mode |
| DES-CBC | Legacy cipher — educational only |
| 3DES-CBC | Triple DES with 24-byte key |

### 🔑 Asymmetric
| Cipher | Description |
|---|---|
| RSA-2048 | Key pair generation + OAEP-SHA256 encrypt/decrypt |

### 🔡 Encoders / Decoders
| Encoder | Description |
|---|---|
| Base64 | RFC 4648 standard encoding |
| Base32 | Base32 encoding/decoding |
| Hexadecimal | Byte-by-byte hex encoding |
| Binary | 8-bit binary representation |
| URL Encoding | Percent-encoding (RFC 3986) |
| Morse Code | International Morse encode/decode |

---

## UI Highlights

- **Sidebar** — navigate ciphers by category
- **Mode selector** — Encrypt / Decrypt / Encode / Decode
- **Auto key generator** — one click to generate a secure random key
- **RSA key pair generator** — generates 2048-bit PEM key pairs instantly
- **Step-by-step trace** — see every substitution for classical ciphers
- **⇄ Swap** — flip input/output to chain operations
- **Copy** button on every output

---

## Installation

```bash
git clone https://github.com/ApollonASM8977/CipherLab.git
cd CipherLab
```

### Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
# ↑ http://localhost:5173
```

---

## Project Structure

```
CipherLab/
├── backend/
│   ├── main.py                  # FastAPI — /process, /generate-key, /ciphers
│   ├── requirements.txt
│   └── ciphers/
│       ├── classical.py         # Caesar, ROT13, Atbash, Vigenère, PolySubCipher, Rail Fence
│       ├── modern.py            # AES-256-GCM, AES-128-CBC, DES, 3DES
│       ├── asymmetric.py        # RSA-2048
│       └── encoders.py          # Base64, Base32, Hex, Binary, URL, Morse
│
└── frontend/
    ├── src/
    │   ├── App.tsx              # Main shell — header + sidebar layout
    │   ├── types.ts             # TypeScript interfaces
    │   └── components/
    │       ├── Sidebar.tsx      # Category navigation
    │       ├── CipherPanel.tsx  # Main cipher interface
    │       └── StepsView.tsx    # Step-by-step trace display
    └── tailwind.config.js
```

---

## API

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `GET` | `/ciphers` | List all available ciphers with metadata |
| `POST` | `/process` | Process text with any cipher |
| `POST` | `/generate-key` | Generate a random key for any cipher |

---

## Tech Stack

- **Backend** — FastAPI, Python 3.11, Uvicorn
- **Cryptography** — `cryptography` library (AES, DES, RSA)
- **Classical ciphers** — Pure Python
- **Frontend** — React 18, TypeScript, Vite, Tailwind CSS
- **HTTP** — Axios

---

## Author

**Aboubacar Sidick Meite** — Cybersecurity Student  
[GitHub](https://github.com/ApollonASM8977)

---

## License

© 2026 Aboubacar Sidick Meite — All Rights Reserved.  
Unauthorized copying or distribution is strictly prohibited.

