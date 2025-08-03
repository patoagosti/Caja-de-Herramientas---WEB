import streamlit as st
from yt_dlp import YoutubeDL
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
    st.write("Acá vas a poder convertir archivos, como PDF a Word, imágenes, etc.")

    st.subheader("📥 Descargar video de YouTube")
    link = st.text_input("Pegá el link de YouTube")

    if st.button("Descargar video"):
        if link:
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'video_descargado.%(ext)s'  # Nombre fijo para el archivo
            }
            try:
                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(link, download=True)
                    filename = ydl.prepare_filename(info)

                st.success(f"Descarga completada ✅ ({info['title']})")

                # BOTÓN DE DESCARGA AL NAVEGADOR
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

elif opcion == "Mensajes":
    st.header("💬 Armadores de Mensajes")
    st.write("Acá vas a poder crear textos automáticos para mails, WhatsApp, etc.")

elif opcion == "Datos":
    st.header("📊 Herramientas de Datos")
    st.write("Acá vas a poder limpiar listas, comparar datos, organizar Excel, etc.")

elif opcion == "Automatizaciones":
    st.header("🤖 Automatizaciones")
    st.write("Acá vas a tener scripts que hagan tareas repetitivas por vos.")
