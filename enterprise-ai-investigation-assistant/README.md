# Enterprise AI Investigation & Knowledge Assistant

A learning project for building an evidence-grounded investigation assistant. This first slice is a local FastAPI service backed only by fabricated sample records. It does not call an AI model, store uploaded documents, or make investigation decisions.

## Requirements

- macOS
- Python 3.15 (Python 3.11 or newer is supported)
- A terminal

If `python3.15 --version` does not work, install a compatible Python version for macOS from <https://www.python.org/downloads/macos/>. Open a new Terminal window after installation and verify its version before continuing.

If an existing `.venv` was created with Python 3.9 or another incompatible version, rename that folder before creating the new environment. A fresh checkout will not have a `.venv` folder.

## Set up locally

From Terminal, run:

```zsh
cd ~/Documents/GitHub/enterprise-ai-investigation-assistant
python3.15 --version
python3.15 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

The `mv` command preserves the old Python 3.9 environment as a backup. Run it only if `.venv` already exists; otherwise skip that line. The new virtual environment keeps this project's Python packages separate from other projects on your Mac. Activate it again with `source .venv/bin/activate` whenever you open a new Terminal window for this project.

## Run the tests

```zsh
python -m pytest
```

## Start the API

```zsh
python -m uvicorn investigation_assistant.main:app --reload
```

Open <http://127.0.0.1:8000/docs> for the interactive API page. The starter endpoints are:

- `GET /health` reports whether the local service is running.
- `GET /cases` lists fabricated sample cases.
- `GET /cases/{case_id}` fetches one sample case.

Stop the server with `Ctrl+C`.

## Current scope

This is a local starter, not a production system. It has no authentication, authorization, document upload, persistence, Azure resources, or AI-generated answers. Do not put real or confidential case information into it. Later phases will add features and controls incrementally, with human review for consequential outputs.
