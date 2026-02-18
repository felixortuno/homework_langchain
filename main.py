import streamlit as st
import os
# Importaciones corregidas para las versiones actuales
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper

# Configuración de interfaz profesional
st.set_page_config(page_title="AI Logo Studio Pro", page_icon="🚀", layout="wide")

# Estética avanzada con CSS
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .stButton>button { background: linear-gradient(45deg, #ff4b4b, #ff7575); color: white; border: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("🎨 AI Logo Designer")
    st.write("Generador de identidad visual de alto nivel.")

    # Sidebar: Controles de usuario
    with st.sidebar:
        st.header("⚙️ Configuración")
        api_key = st.text_input("OpenAI API Key", type="password")
        
        concept = st.text_input("Nombre o concepto de la marca")
        style = st.selectbox("Estilo", ["Minimalista", "Futurista", "Retro", "Lujo"])
        palette = st.selectbox("Colores", ["Vibrante", "Pastel", "Monocromo", "Dorado y Negro"])
        
        # Parámetros avanzados
        st.divider()
        detail = st.select_slider("Detalle", options=["Bajo", "Medio", "Alto"])
        aspect = st.radio("Relación de aspecto", ["1:1", "16:9"])

    # Lógica de generación
    if st.button("Generar Logo Profesional"):
        if not api_key or not concept:
            st.warning("Falta la API Key o el concepto de la marca.")
            return

        # Configuramos el entorno para LangChain
        os.environ["OPENAI_API_KEY"] = api_key

        with st.spinner("Diseñando tu logo..."):
            try:
                # 1. Definición del Prompt Dinámico (Capa de IA)
                template = """
                Eres un experto en branding. Crea un logo para: {concept}.
                Estilo: {style}. Paleta de colores: {palette}.
                Nivel de detalle: {detail}.
                Instrucciones: Fondo blanco sólido, vectorizado, simétrico, alta resolución.
                """
                prompt = PromptTemplate.from_template(template)
                formatted_prompt = prompt.format(
                    concept=concept, 
                    style=style, 
                    palette=palette, 
                    detail=detail
                )

                # 2. Conector DALL-E 3
                dalle = DallEAPIWrapper(model="dall-e-3")
                image_url = dalle.run(formatted_prompt)

                # 3. Presentación de resultados
                st.image(image_url, caption=f"Logo para {concept}", use_container_width=True)
                st.success("¡Logo generado!")
                st.balloons()

            except Exception as e:
                st.error(f"Error técnico: {str(e)}")

if __name__ == "__main__":
    main()