# HVAC Fix Finder

A small demo that helps field techs triage HVAC symptoms. The **front end** is a single file, [`hvac-fix-finder.html`](hvac-fix-finder.html), with embedded React. The **back end** is a FastAPI service that does semantic search over chunked Carrier service-manual text. Details for Python tooling and the API live in [`backend/README.md`](backend/README.md); utilities that build chunk JSON from markdown live in [`backend/scripts/README.md`](backend/scripts/README.md).

**Important:** The browser only calls the backend when the user sets **Brand** to **`carrier`** (case-insensitive, ignoring leading/trailing spaces). Any other brand (or an empty brand) uses the in-page “general knowledge” fallback and **does not** request `http://127.0.0.1:8000/diagnose`. The server code today also loads only Carrier chunks from `documentation/carrier/`, so this behavior is aligned end to end.

## Repository layout

| Path | Purpose |
|------|---------|
| `hvac-fix-finder.html` | UI and client-side diagnosis logic. |
| `backend/` | FastAPI app, dependencies, and `documentation/<brand>/` chunk data. See [backend/README.md](backend/README.md). |
| `backend/scripts/` | e.g. `chunk_md.py` to produce `hvac_chunks.json` for a provider folder. See [backend/scripts/README.md](backend/scripts/README.md). |

## Prerequisites

- **Python 3** with `venv` (for the API and optional scripts).
- A **web browser** (Chrome, Firefox, Safari, or Edge are fine).
- For full-stack local testing, run both a static file server (front end) and the API (back end) as below.

## Local environment setup (Python)

1. **Virtual environment (recommended)**  
   Create and activate a venv once; you can use the same venv for `backend` and `backend/scripts` and install both `requirements.txt` files into it, or keep separate venvs. Step-by-step instructions are in:

   - [backend/README.md — Environment setup](backend/README.md#environment-setup)  
   - [backend/scripts/README.md — Environment setup](backend/scripts/README.md#environment-setup)

2. **Install API dependencies** (from the repo root, with your venv activated):

   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Optional — script dependencies** (only if you will run `chunk_md.py` or add scripts under `backend/scripts`):

   ```bash
   pip install -r backend/scripts/requirements.txt
   ```

The first time the API runs, it downloads the `all-MiniLM-L6-v2` embedding model; that can take a few minutes and uses noticeable disk space.

## Host the back end locally

The API must be started from the `backend` directory (paths to chunk JSON are relative to the process working directory). With the venv active and dependencies installed:

```bash
cd backend
uvicorn server:app --reload
```

- Default base URL: `http://127.0.0.1:8000`  
- Interactive docs: `http://127.0.0.1:8000/docs`  
- Diagnose: `http://127.0.0.1:8000/diagnose?query=...`  

For behavior, data layout, and “next steps” (multi-brand, RAG, vector DB), see [backend/README.md](backend/README.md).

## Host the front end locally

**Option A — Simple static server (recommended for development)**  
The front end is configured to call the API at `http://127.0.0.1:8000`. Use a **different port** for the HTML so it does not clash with uvicorn on `8000`. From the **repository root**:

```bash
python3 -m http.server 8080
```

Then open `http://127.0.0.1:8080/hvac-fix-finder.html` in your browser.

**Option B — Open the file directly**  
You can open `hvac-fix-finder.html` in a browser from the file system. Some environments behave differently with `file://` and `fetch()`; if the Carrier + backend path misbehaves, use Option A.

## End-to-end test (Carrier + API)

1. Start the API (`uvicorn` in `backend` as above).  
2. Serve the front end (e.g. `python3 -m http.server 8080` at the repo root).  
3. In the app, set **Brand** to **Carrier** and submit a symptom. The UI should call `/diagnose` and show results sourced from the Carrier manual chunks.  
4. With any other brand (or no brand), the app uses the built-in general knowledge path only and does not rely on the running API for that request.

## Regenerating or adding documentation chunks

To turn a markdown manual into `hvac_chunks.json` under a provider folder such as `documentation/carrier/`, use `backend/scripts/chunk_md.py` as documented in [backend/scripts/README.md](backend/scripts/README.md).
