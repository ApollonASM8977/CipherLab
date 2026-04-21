# ðŸ”¬ CipherLab

> Full cryptography toolkit â€” classical ciphers, modern encryption, asymmetric keys & encoders.

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

### âš™ï¸ Classical Ciphers
| Cipher | Description |
|---|---|
| Caesar | Shift cipher with configurable offset (1â€“25) |
| ROT13 | Caesar with shift 13 â€” self-inverse |
| Atbash | Mirror alphabet substitution |
| VigenÃ¨re | Keyword-based polyalphabetic cipher |
| PolySubCipher | 2-key alternating substitution (original algorithm) |
| Rail Fence | Transposition cipher with configurable rails |

### ðŸ”’ Modern Symmetric
| Cipher | Description |
|---|---|
| AES-256-GCM | Authenticated encryption â€” industry standard |
| AES-128-CBC | AES with 128-bit key in CBC mode |
| DES-CBC | Legacy cipher â€” educational only |
| 3DES-CBC | Triple DES with 24-byte key |

### ðŸ”‘ Asymmetric
| Cipher | Description |
|---|---|
| RSA-2048 | Key pair generation + OAEP-SHA256 encrypt/decrypt |

### ðŸ”¡ Encoders / Decoders
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

- **Sidebar** â€” navigate ciphers by category
- **Mode selector** â€” Encrypt / Decrypt / Encode / Decode
- **Auto key generator** â€” one click to generate a secure random key
- **RSA key pair generator** â€” generates 2048-bit PEM key pairs instantly
- **Step-by-step trace** â€” see every substitution for classical ciphers
- **â‡„ Swap** â€” flip input/output to chain operations
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
# â†’ http://localhost:5173
```

---

## Project Structure

```
CipherLab/
â”œâ”€â”€ backend/
â”‚   â”œâ”€â”€ main.py                  # FastAPI â€” /process, /generate-key, /ciphers
â”‚   â”œâ”€â”€ requirements.txt
â”‚   â””â”€â”€ ciphers/
â”‚       â”œâ”€â”€ classical.py         # Caesar, ROT13, Atbash, VigenÃ¨re, PolySubCipher, Rail Fence
â”‚       â”œâ”€â”€ modern.py            # AES-256-GCM, AES-128-CBC, DES, 3DES
â”‚       â”œâ”€â”€ asymmetric.py        # RSA-2048
â”‚       â””â”€â”€ encoders.py          # Base64, Base32, Hex, Binary, URL, Morse
â”‚
â””â”€â”€ frontend/
    â”œâ”€â”€ src/
    â”‚   â”œâ”€â”€ App.tsx              # Main shell â€” header + sidebar layout
    â”‚   â”œâ”€â”€ types.ts             # TypeScript interfaces
    â”‚   â””â”€â”€ components/
    â”‚       â”œâ”€â”€ Sidebar.tsx      # Category navigation
    â”‚       â”œâ”€â”€ CipherPanel.tsx  # Main cipher interface
    â”‚       â””â”€â”€ StepsView.tsx    # Step-by-step trace display
    â””â”€â”€ tailwind.config.js
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

- **Backend** â€” FastAPI, Python 3.11, Uvicorn
- **Cryptography** â€” `cryptography` library (AES, DES, RSA)
- **Classical ciphers** â€” Pure Python
- **Frontend** â€” React 18, TypeScript, Vite, Tailwind CSS
- **HTTP** â€” Axios

---

## Author

**Aboubacar Sidick Meite** â€” Cybersecurity Student  
[GitHub](https://github.com/ApollonASM8977)

---

## License

Â© 2026 Aboubacar Sidick Meite â€” All Rights Reserved.  
Unauthorized copying or distribution is strictly prohibited.

