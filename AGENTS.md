# AGENTS.md — CipherLab

**Read first.** The owner's rules for every project (mandatory checklists, synchronisation at the start and end of every session, standing rules) are in `AGENTS-master.md`, in the owner's private repository `agents-rules`, cloned at `~/agents-rules` on each of the owner's computers and loaded automatically by the global `~/.claude/CLAUDE.md`. Apply them before anything else. If they are not in your context, read `~/agents-rules/AGENTS-master.md` first; if you cannot, ask the owner before working. This file only holds what is specific to this project.

## This project

- **What it is**: Full cryptography toolkit: classical ciphers, modern encryption, asymmetric keys and encoders.
- **Category**: Personnel; public repository: nothing private may be written in it (no secret, no private matter).
- **Stack**: Python 3.11 + FastAPI backend, React 18 + TypeScript frontend.
- **Install, run, test**:
  - Backend (FastAPI): `cd backend`, `python -m venv .venv`, `.venv\Scripts\activate`, `pip install -r requirements.txt`, `uvicorn main:app --reload --port 8000`.
  - Frontend (React + TypeScript + Vite): `cd frontend`, `npm install --ignore-scripts`, `npm run dev`; check with `npm run build` (runs `tsc`).
- **Branches**: work and test on `stg`; `master` is production and only receives work the owner has validated, merged from `stg` on the owner's OK. A push to `master` deploys: nothing.
- **Folder**: mini-PC `D:\My Project\Personnel\CipherLab`; on another computer, `~/agents-rules/sync-all.cmd` clones it in the same place under that computer's root.
- **Where we are**: `README.md`; create `docs/agent/HANDOFF.md` (and the other traces of the master file) as soon as real work starts here.
- **Rules learned on this project**: none yet.
