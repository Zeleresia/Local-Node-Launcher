# Local-Node-Launcher

A lightweight web panel to manage local app processes (Node.js or Python) from your browser. Add instances by pointing to a working directory and a command (e.g., `npm run start`, `node index.js`, `python app.py`), then start/stop or remove them from a simple UI

> Built with Flask, standard `templates/` and `static/` folders, and minimal dependencies. Flask serves static assets from `/static/...` and loads HTML from `templates/`.

---

## Features

- **Process control (local)**: define instances with `name`, `cwd`, and `cmd`; start/stop via web.
- **Persistent registry**: instances stored in `apps.json` in the project root.
- **Clean UI**: modern spacing, max-width container, responsive navbar, and table view.
- **Dark/Light mode**: one-click theme toggle, preference saved in `localStorage`.
- **Zero database**: JSON storage; no external services required.
- **Cross-language commands**: run Node.js (`npm`, `node`) and Python (`python`, `py`) commands that exist in your PATH.

---

## Why this project

- **Minimal setup**: only Python + Flask. No Docker or database required.
- **Familiar layout**: standard Flask `templates/` and `static/` separation, making customization straightforward.
- **Works on Windows**: designed to run locally on Windows; commands are executed with `shell=True` so common CLIs resolve from PATH.
- **Portable**: a single folder with `app_server.py`, `templates/`, `static/`, and `apps.json`.

---

## Tech Stack

- **Python** (Flask) for the web server and routes.
- **HTML/CSS/JS** for the UI (served via Flask’s `templates/` and `static/`).

---


## Quick Start

### 1) Requirements
- Python 3.9+  
- Windows, macOS, or Linux

### 2) Setup

```bash
# Clone
git clone https://github.com/Zeleresia/Local-Node-Launcher.git
cd local-app-launcher

# (Recommended) Create & activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Install dependencies
pip install Flask
```

### 3) Run
Run the `app.bat` or
```bash
python app_server.py
```

Open `http://127.0.0.1:5000/`.

---

## Usage

1. **Add Instance**  
   - **Name** – a friendly label (e.g., my Node bot)
   - **Working dir** – folder that contains the project (e.g., `X:\project\bot`)
   - **Command** – what to run (e.g., `npm run start`, `node index.js`, `python app.py`, `py -3.11 -m uvicorn main:app`)

2. **Start / Stop**  
   Use the **Start** or **Stop** button per row.

3. **Delete**  
   Remove an instance from the registry (does not delete files in your project folder).

`apps.json` is updated automatically.

---

## Configuration Notes

- **Static/Template linking**  
  In `templates/index.html`, link CSS/JS with:
  ```html
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
  <script defer src="{{ url_for('static', filename='app.js') }}"></script>
  ```
  This is the canonical Flask way to serve static assets.

- **Theme toggle**  
  The toggle sets `data-theme="light"` or `"dark"` on `<html>` and persists the preference in `localStorage`.

---

## Security & Limitations

- **Local only**: this tool executes commands on your machine. Keep it bound to `127.0.0.1` unless you know what you’re doing.
- **Command trust**: only add commands you trust; they’ll run with your user’s privileges.
- **No auth by default**: if you expose this beyond localhost, add authentication and TLS first.
- **No remote orchestration**: this is a local launcher, not a production process manager.

---

## Roadmap

- Optional: log tail in UI (read-only).
- Optional: export/import `apps.json`.
- Optional: auth & roles.

---

## Contributing

Contributions are welcome. Please open an issue to discuss changes, then submit a PR.

---

## License

MIT (see `LICENSE`).
