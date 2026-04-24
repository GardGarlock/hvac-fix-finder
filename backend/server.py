from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer, util
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("documentation/carrier/hvac_chunks.json", "r") as f:
    chunks = json.load(f)

model = SentenceTransformer('all-MiniLM-L6-v2')
chunk_texts = [c['content'] for c in chunks]
chunk_embeddings = model.encode(chunk_texts, convert_to_tensor=True)

@app.get("/diagnose")
def diagnose(query: str):
    query_embedding = model.encode(query, convert_to_tensor=True)
    hits = util.semantic_search(query_embedding, chunk_embeddings, top_k=3)[0]
    
    results = []
    for hit in hits:
        chunk = chunks[hit['corpus_id']]
        results.append({
            "name": chunk['metadata'].get('section_path', 'Manual Reference'),
            "explanation": chunk['content'],
            "confidence": "High" if hit['score'] > 0.6 else "Medium"
        })
    
    return {"results": results}
