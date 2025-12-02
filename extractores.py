# ============================================================
#  extractores.py – Versión optimizada para ACRJ–ICI v7
#  Compatible con Streamlit Cloud (NO usa pdfplumber)
# ============================================================

import re
from typing import Optional
from docx import Document
import PyPDF2


def limpiar_texto(texto: Optional[str]) -> str:
    """
    Limpia el texto antes de procesarlo.
    - Elimina saltos de línea múltiples.
    - Normaliza espacios.
    - Devuelve texto ordenado.
    """
    if not texto:
        return ""

    texto = re.sub(r"\r\n", "\n", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    texto = re.sub(r"[ \t]{2,}", " ", texto)

    return texto.strip()


def leer_pdf(archivo) -> str:
    """
    Lee un PDF usando PyPDF2 (compatible con Streamlit Cloud).
    Extrae texto básico sin requerir dependencias externas.
    """
    texto_total = []

    lector = PyPDF2.PdfReader(archivo)
    for pagina in lector.pages:
        contenido = pagina.extract_text() or ""
        texto_total.append(contenido)

    return "\n\n".join(texto_total)


def leer_word(archivo) -> str:
    """
    Lee archivos .docx usando python-docx.
    Devuelve el texto concatenado.
    """
    doc = Document(archivo)
    partes = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n\n".join(partes)
