# === utils/llm_reasoner.py ===
from transformers import pipeline

# Load a lightweight QA model from HuggingFace
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

def get_final_answer(query, top_chunks):
    """
    Takes the user query and top document chunks,
    passes them to a QA model, and returns an answer.
    """
    context = "\n".join(top_chunks)
    response = qa_pipeline(question=query, context=context)
    return response["answer"], top_chunks