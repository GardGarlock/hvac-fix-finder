# Backend API

The backend is a small [FastAPI](https://fastapi.tiangolo.com/) service that answers HVAC troubleshooting queries using **semantic search** over chunked manual text. On startup it loads `documentation/carrier/hvac_chunks.json` (produced by the chunking script in `scripts/`, typically written under a provider folder) and a sentence-transformer model, embeds all chunks, then at request time embeds the user’s question and returns the top few most similar passages with labels derived from each chunk’s metadata.

Chunk files for each brand live under `documentation/<brand>/` (for example `documentation/carrier/hvac_chunks.json`). The current code only loads the Carrier data file; that layout is the intended place to add more manufacturers.

The main entry point is `GET /diagnose?query=...`, which returns JSON with candidate explanations and a coarse confidence level based on embedding similarity. The app enables permissive CORS so a local or deployed front end can call it from the browser.

## Environment setup

Use a **virtual environment** so dependencies stay isolated from your system Python.

From the `backend` directory (or adjust paths if you want the venv somewhere else):

1. **Create** a venv (here it is named `.venv` in this folder):

   ```bash
   python3 -m venv .venv
   ```

2. **Activate** it:

   - **macOS / Linux:** `source .venv/bin/activate`
   - **Windows (Command Prompt):** `.venv\Scripts\activate.bat`
   - **Windows (PowerShell):** `.venv\Scripts\Activate.ps1`

3. **Install** dependencies from this directory’s `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

   The first run downloads the `all-MiniLM-L6-v2` model (and may pull in PyTorch as a dependency of `sentence-transformers`); that can take a few minutes and uses noticeable disk space.

You should see your shell prompt change (e.g. `(.venv)`) when the venv is active. Deactivate later with `deactivate`.

**Reusing a venv:** If you already created and use a venv for `backend/scripts` (see [scripts/README.md](scripts/README.md)), activate that same venv and run `pip install -r requirements.txt` from this `backend` directory to add the API packages. You do not need a second venv unless you prefer to keep projects separate.

## Run the server locally

The app reads `documentation/carrier/hvac_chunks.json` with a path relative to the process **current working directory**, so start the server from the `backend` folder.

With the venv activated and dependencies installed:

```bash
cd backend
uvicorn server:app --reload
```

By default the API is available at `http://127.0.0.1:8000`. Try:

- **Health / docs:** `http://127.0.0.1:8000/docs` (interactive OpenAPI UI)
- **Diagnose example:** `http://127.0.0.1:8000/diagnose?query=furnace%20wont%20heat`

The first request after startup may be slow while the model finishes loading; later requests are faster.

## Project layout (this folder)

| Path | Role |
|------|------|
| `server.py` | FastAPI app, embeddings, and `/diagnose` route. |
| `requirements.txt` | Python packages to run the server. |
| `documentation/<brand>/hvac_chunks.json` | Chunked manual data per brand (e.g. `documentation/carrier/` for Carrier). |

To regenerate or add chunk JSON, use the utilities documented in [scripts/README.md](scripts/README.md).

## Next steps

This service is a **very rough demo** of retrieval ideas: it is not full **RAG** (retrieval-augmented generation) yet, only similarity search that returns raw chunk text.

1. **Brand-aware retrieval.** Extend the API so the client passes a **brand** (or manufacturer) and the server loads **only** the chunk set from the matching directory under `documentation/`, e.g. `documentation/<brand>/hvac_chunks.json`, instead of always using Carrier. That implies embedding and storing vectors per brand (or a shared index with brand filters) once more than one provider exists.

2. **Real RAG with an LLM.** After retrieval, **pass the top chunks as context** into a language model and **generate** an answer that cites or synthesizes that context, instead of returning the chunk bodies verbatim. That is the usual “retrieve then generate” pattern.

3. **Persistent vector storage.** Today embeddings and the similarity index are held **in memory** inside the FastAPI process, which does not scale and reloads work on every restart. Move embedding storage and ANN search to a **vector database** or a database with vector support so lookups are durable, can grow with more manuals, and can be shared by multiple app instances.
