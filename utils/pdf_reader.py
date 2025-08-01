# === utils/pdf_reader.py ===
import requests
import fitz  # PyMuPDF

def download_and_parse_pdf(url):
    """
    Downloads the PDF from a given URL and extracts all text.
    Returns a single string with the document content.
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download PDF: {response.status_code}")

    with open("temp.pdf", "wb") as f:
        f.write(response.content)

    doc = fitz.open("temp.pdf")
    text = "\n".join([page.get_text() for page in doc])
    doc.close()
    return text