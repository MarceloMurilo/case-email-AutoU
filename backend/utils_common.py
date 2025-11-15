"""
Funções comuns - Extração e limpeza de texto
"""
import re
import io
import pdfplumber


def extract_text_from_pdf(file_content: bytes) -> str:
    """Extrai texto de arquivo PDF"""
    try:
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        return text.strip()
    except Exception as e:
        raise Exception(f"Erro ao extrair PDF: {str(e)}")


def extract_text_from_txt(file_content: bytes) -> str:
    """Extrai texto de arquivo TXT"""
    for encoding in ['utf-8', 'latin-1', 'cp1252']:
        try:
            return file_content.decode(encoding)
        except UnicodeDecodeError:
            continue
    return file_content.decode('utf-8', errors='ignore')


def clean_text(text: str) -> str:
    """Limpeza básica do texto"""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

