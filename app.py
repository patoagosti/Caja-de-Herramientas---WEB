import streamlit as st
from yt_dlp import YoutubeDL
import base64
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter
from docx import Document
from pdf2docx import Converter
from docx2pdf import convert as docx2pdf_convert
import os

st.set_page_config(page_title="Caja de Herramientas", layout="wide")
st.title("Caja de Herramientas")

st.sidebar.title("Categorías")
opcion = st.sidebar.radio(
    "Seleccioná una categoría",
    ["Conversores", "Mensajes", "Datos", "Automatizaciones"]
)

if opcion == "Conversores":
    st.header("🔄 Herramientas de Conversión")
    tipo_conversor = st.selectbox("Seleccioná un tipo de conversor", ["Videos", "Documentos"])

    if tipo_conversor == "Videos":
        st.subheader("📥 Descargar video de YouTube")
        link = st.text_input("Pegá el link de YouTube")

        if st.button("Descargar video"):
            if link:
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': 'video_descargado.%(ext)s'
                }
                try:
                    with YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(link, download=True)
                        filename = ydl.prepare_filename(info)

                    st.success(f"Descarga completada ✅ ({info['title']})")

                    with open(filename, "rb") as file:
                        st.download_button(
                            label="📥 Descargar video a tu PC",
                            data=file,
                            file_name=os.path.basename(filename),
                            mime="video/mp4"
                        )

                except Exception as e:
                    st.error(f"Ocurrió un error: {e}")
            else:
                st.warning("Pegá un link primero.")

    elif tipo_conversor == "Documentos":
        st.subheader("📄 Conversores PDF y Word")

        def get_download_link(file, filename, file_label):
            with open(file, "rb") as f:
                data = f.read()
            b64 = base64.b64encode(data).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">{file_label}</a>'
            return href

        # PDF a Word
        st.write("### PDF a Word")
        uploaded_pdf = st.file_uploader("Sube un archivo PDF", type=["pdf"], key="pdf_to_word")

        if uploaded_pdf is not None:
            with open("temp_input.pdf", "wb") as f:
                f.write(uploaded_pdf.read())

            st.write("Convirtiendo...")
            cv = Converter("temp_input.pdf")
            cv.convert("temp_output.docx", start=0, end=None)
            cv.close()

            st.markdown(get_download_link("temp_output.docx", "convertido.docx", "Descargar Word"), unsafe_allow_html=True)

        # Word a PDF
        st.write("### Word a PDF")
        uploaded_word = st.file_uploader("Sube un archivo Word", type=["docx"], key="word_to_pdf")

        if uploaded_word is not None:
            with open("temp_input.docx", "wb") as f:
                f.write(uploaded_word.read())

            st.write("Convirtiendo...")
            docx2pdf_convert("temp_input.docx", "temp_output.pdf")

            st.markdown(get_download_link("temp_output.pdf", "convertido.pdf", "Descargar PDF"), unsafe_allow_html=True)

        # Combinar PDFs
        st.write("### Combinar PDFs")
        uploaded_pdfs = st.file_uploader("Sube archivos PDF para combinar", type=["pdf"], accept_multiple_files=True)

        if uploaded_pdfs:
            merger = PdfWriter()
            for pdf in uploaded_pdfs:
                reader = PdfReader(pdf)
                for page in reader.pages:
                    merger.add_page(page)

            with open("combined.pdf", "wb") as f:
                merger.write(f)

            st.markdown(get_download_link("combined.pdf", "combinado.pdf", "Descargar PDF combinado"), unsafe_allow_html=True)

        # Limpieza de archivos temporales
        if os.path.exists("temp_input.pdf"): os.remove("temp_input.pdf")
        if os.path.exists("temp_output.docx"): os.remove("temp_output.docx")
        if os.path.exists("temp_input.docx"): os.remove("temp_input.docx")
        if os.path.exists("temp_output.pdf"): os.remove("temp_output.pdf")
        if os.path.exists("combined.pdf"): os.remove("combined.pdf")

elif opcion == "Mensajes":
    st.header("💬 Armadores de Mensajes")
    st.write("Acá vas a poder crear textos automáticos para mails, WhatsApp, etc.")

elif opcion == "Datos":
    st.header("📊 Herramientas de Datos")
    st.write("Acá vas a poder limpiar listas, comparar datos, organizar Excel, etc.")

elif opcion == "Automatizaciones":
    st.header("🤖 Automatizaciones")
    st.write("Acá vas a tener scripts que hagan tareas repetitivas por vos.")
