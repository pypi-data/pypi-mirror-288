from io import BytesIO
import base64
import base64
import fitz  # PyMuPDF
import requests

def file_to_base64(image_full_path):
  with open(image_full_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def url_file_to_base64(url):
    response = requests.get(url)
    response.raise_for_status()
    return base64.b64encode(response.content).decode('utf-8')

def extract_text_from_pdf_file(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def extract_text_from_pdf_base64(pdf_base64):
    pdf_data = base64.b64decode(pdf_base64)
    pdf_stream = BytesIO(pdf_data)
    doc = fitz.open(stream=pdf_stream, filetype="pdf")
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text