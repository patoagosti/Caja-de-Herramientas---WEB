import streamlit as st
from yt_dlp import YoutubeDL

st.set_page_config(page_title="Caja de Herramientas de Pato", layout="wide")
st.title("🧰 Caja de Herramientas de Pato")

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

    if link:
        ydl_opts = {}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            formats = info.get('formats', [])
            qualities = []
            for f in formats:
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('ext') == 'mp4':
                    qualities.append(f"{f['format_id']} - {f['height']}p")

        calidad = st.selectbox("Seleccioná la calidad", qualities)

        if st.button("Descargar video"):
            st.write(f"Descargando en calidad: {calidad}")
            ydl_opts = {
                'format': calidad.split(' ')[0]
            }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            st.success("Descarga completada ✅ (se guardó en la carpeta actual)")

elif opcion == "Mensajes":
    st.header("💬 Armadores de Mensajes")
    st.write("Acá vas a poder crear textos automáticos para mails, WhatsApp, etc.")

elif opcion == "Datos":
    st.header("📊 Herramientas de Datos")
    st.write("Acá vas a poder limpiar listas, comparar datos, organizar Excel, etc.")

elif opcion == "Automatizaciones":
    st.header("🤖 Automatizaciones")
    st.write("Acá vas a tener scripts que hagan tareas repetitivas por vos.")


