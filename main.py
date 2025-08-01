# === main.py ===
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import List
from utils.pdf_reader import download_and_parse_pdf
from utils.chunker import chunk_text
from utils.embedder import generate_and_store_embeddings, query_top_chunks
from utils.llm_reasoner import get_final_answer
from time import time

app = FastAPI()

class InputPayload(BaseModel):
    documents: str  # PDF URL
    questions: List[str]

@app.post("/hackrx/run")
async def run_handler(payload: InputPayload):
    try:
        start_time = time()

        # Step 1: Download and read PDF
        text = download_and_parse_pdf(payload.documents)

        # Step 2: Chunk document and store embeddings
        chunks = chunk_text(text)
        generate_and_store_embeddings(chunks)

        # Step 3: Process each question
        answers = []
        for q in payload.questions:
            top_chunks = query_top_chunks(q)
            answer, _ = get_final_answer(q, top_chunks)
            answers.append(answer)

        end_time = time()
        processing_time = round(end_time - start_time, 2)

        return {
            "success": True,
            "answers": answers,
            "processing_info": {
                "num_questions": len(payload.questions),
                "num_chunks": len(chunks),
                "processing_time_seconds": processing_time
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "success": False,
            "error": str(e)
        })