# === utils/chunker.py ===
def chunk_text(text, max_length=500):
    """
    Splits the input text into chunks of max_length characters.
    Tries to break on sentence or paragraph boundaries.
    """
    import re

    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) + 1 <= max_length:
            current_chunk += (" " + para)
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks