from docx import Document
from io import BytesIO
import streamlit as st
import pandas as pd
import re

def download_docx_button(label, filename, content: str):
    doc = Document()
    for line in content.strip().splitlines():
        doc.add_paragraph(line)
    buf = BytesIO()
    doc.save(buf)
    st.download_button(
        label=label,
        data=buf.getvalue(),
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
