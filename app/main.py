from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
import os
import gc

# Import lightweight modules first
from app.ingestion.load import load_content
from app.ingestion.chunk import chunk_text

app = FastAPI(
    title="Assurance AI - Low RAM",
    description="Optimized for 512MB RAM on Render",
    version="1.0"
)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body for /query
class QueryRequest(BaseModel):
    query: str
    session_id: str

@app.get("/")
def root():
    return {"message": "Assurance AI Low-RAM version is live!"}

@app.post("/api/v1/hackrx/run")
def run_solution(payload: dict):
    """
    HackRx Webhook:
    Load heavy stuff only inside this function, then free it.
    """
    try:
        from app.core.retriever import retrieve_chunks, build_index
        from app.core.engine import evaluate_decision

        query = payload.get("query", "")
        session_id = payload.get("session_id", "temp_session")

        relevant_chunks = retrieve_chunks(query, session_id, k=3)
        answer = evaluate_decision(query, session_id)

        # Free memory after use
        del relevant_chunks, answer
        gc.collect()

        return {"status": "success", "result": "Processed query"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/query")
def query_docs(request: QueryRequest):
    try:
        from app.core.retriever import retrieve_chunks
        from app.core.engine import evaluate_decision

        relevant_chunks = retrieve_chunks(request.query, request.session_id, k=3)
        answer = evaluate_decision(request.query, request.session_id)

        del relevant_chunks, answer
        gc.collect()

        return {
            "query": request.query,
            "response": answer,
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/upload_docs")
async def upload_docs(uploaded_files: List[UploadFile] = File(...)):
    responses = []
    alltext_chunks = []
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    index_dir = f"session_{session_id}"

    try:
        for uploaded_file in uploaded_files:
            contents = await uploaded_file.read()
            file_path = f"temp_uploads/{index_dir}/{uploaded_file.filename}"
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(contents)

            raw_text = load_content(file_path)
            text_chunks = chunk_text(raw_text)
            alltext_chunks.extend(text_chunks)

            responses.append({
                "filename": uploaded_file.filename,
                "status": "parsed and added to combined index",
                "session_id": session_id
            })

        from app.core.retriever import build_index
        build_index(alltext_chunks, session_id, force_rebuild=True)

        # Free memory
        del alltext_chunks
        gc.collect()

        return {
            "status": "success",
            "indexed_files": responses,
            "session_id": session_id
        }

    except Exception as e:
        return {"error": str(e)}
