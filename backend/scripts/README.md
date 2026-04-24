# Scripts

Small command-line utilities for this repository. Each script below is documented with its purpose, requirements, and usage. When you add a new script, add a subsection here so others can run it without reading the source first.

## Environment setup

Use a **virtual environment** so script dependencies stay isolated from your system Python.

From the `backend/scripts` directory (or with paths adjusted to match where you want the venv to live):

1. **Create** a venv (here it is named `.venv` in this folder):

   ```bash
   python3 -m venv .venv
   ```

2. **Activate** it:

   - **macOS / Linux:** `source .venv/bin/activate`
   - **Windows (Command Prompt):** `.venv\Scripts\activate.bat`
   - **Windows (PowerShell):** `.venv\Scripts\Activate.ps1`

3. **Install** dependencies from this folder’s `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

You should see your shell prompt change (e.g. `(.venv)`) when the venv is active. Run the scripts with `python` while activated. Deactivate later with `deactivate`.

**Reusing a venv:** If you already created a venv for the FastAPI app (see [../README.md](../README.md) under `backend/`), activate that same venv and run `pip install -r requirements.txt` from this `scripts` directory to install the script dependencies. You do not need a second venv unless you prefer to keep environments separate.

When you add a script that needs new packages, add them to `requirements.txt` and document them in the script’s section below.

---

## `chunk_md.py`

Splits a markdown HVAC manual into overlapping chunks, preserves heading hierarchy in metadata, and exports a JSON file for search or RAG. Headers (`#` … `######`) are split first, then long sections are sub-split to `chunk_size` with `chunk_overlap`. The table-of-contents `H1` is stripped from metadata for cleaner paths.

**Arguments**

| Argument | Description |
|----------|-------------|
| `input` | Path to the source `.md` file (required, positional). |
| `--size` | Target chunk size in characters (default: `1200`). |
| `--overlap` | Overlap between adjacent chunks in characters (default: `150`). |
| `--save_path` | Directory to write the output file. If omitted, the file is written to the current working directory. The output filename is always `hvac_chunks.json`. |

**Example**

To keep a provider’s chunks next to that provider’s documentation, pass a folder under `documentation/`. Use your provider name in place of `[provider]` (for example `carrier` or `trane`):

```bash
python backend/scripts/chunk_md.py path/to/manual.md --save_path documentation/[provider]
```

This creates (or reuses) the directory `documentation/[provider]/` and writes:

`documentation/[provider]/hvac_chunks.json`

Each entry in the JSON is an object with `content` (string) and `metadata` (including `section_path` built from the heading chain).

**Minimal run** (output in the current directory as `hvac_chunks.json`):

```bash
python backend/scripts/chunk_md.py path/to/manual.md
```

---

## Adding a new script

When you add another script to this folder:

1. Name the file descriptively (e.g. `import_manuals.py`).
2. Add a new `##` section above this “Adding a new script” block with: what it does, how to install dependencies, arguments, and one or two copy-pastable examples.
3. If the script has shared dependencies, add them to `requirements.txt` and mention them in the **Environment setup** section if they need a short note.
