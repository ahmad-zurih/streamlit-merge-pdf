import streamlit as st
from PyPDF2 import PdfMerger, PdfReader
import random
from typing import List
from io import BytesIO
import base64

def merge_pdf(pdf_files: List, out_file_name: str) -> BytesIO:
    """
    Function that takes multiple pdf files and merges them into one pdf file in order.
    Returns a BytesIO object containing the merged PDF.
    """
    merger = PdfMerger()
    for file in pdf_files:
        pdf_file = PdfReader(file, strict=False)
        merger.append(pdf_file)

    merged_pdf = BytesIO()
    merger.write(merged_pdf)
    merger.close()
    merged_pdf.seek(0)
    return merged_pdf

def get_pdf_download_link(pdf_buffer: BytesIO, file_name: str) -> str:
    """
    Generate a download link for the merged PDF file.
    """
    b64 = base64.b64encode(pdf_buffer.getvalue()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}">Download merged file</a>'
    return href

def main():
    st.title('PDF Merger Tool')
    
    # File uploader allows multiple files
    uploaded_files = st.file_uploader("Choose PDF files", accept_multiple_files=True, type=['pdf'])
    if uploaded_files:
        output_file_name = st.text_input("Enter output file name", f"merged_{random.randint(100000,999999)}.pdf")
        
        if st.button('Merge PDFs'):
            if not output_file_name.endswith('.pdf'):
                output_file_name += '.pdf'
                
            merged_pdf = merge_pdf(uploaded_files, output_file_name)
            download_link = get_pdf_download_link(merged_pdf, output_file_name)
            st.markdown(download_link, unsafe_allow_html=True)
            st.success(f"PDFs merged successfully!")

if __name__ == '__main__':
    main()
