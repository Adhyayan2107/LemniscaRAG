from pypdf import PdfReader
import os

def load_documents(folder_path):
    documents = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            reader = PdfReader(file_path)

            text = ""
            for page_number, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            documents.append({
                "filename": filename,
                "content": text
            })

    return documents