import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAIClient
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
import os

# Configuración de la página con estilo sofisticado
st.set_page_config(page_title="AI Logo Designer Pro", page_icon="🎨", layout="wide")

# Estilo CSS personalizado para el look "Moderno"
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #FF4B4B; color: white; }
    .stSlider label, .stSelectbox label { color: #bfbfbf; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

def generate_logo():
    st.title("🎨 AI Logo Designer Pro")
    st.subheader("Generación de identidad visual mediante IA")

    # --- SIDEBAR: PARÁMETROS PERSONALIZABLES ---
    with st.sidebar:
        st.header("Configuración del Logo")
        concept = st.text_area("Concepto de la marca", placeholder="Ej: Una cafetería interestelar...")
        
        style = st.selectbox("Estilo Visual", 
                            ["Minimalista Moderno", "Retro/Vintage", "Futurista/Cyberpunk", "Geométrico", "Lujo/Elegante"])
        
        colors = st.select_slider("Paleta de Colores", 
                                 options=["Monocromático", "Pastel", "Vibrante/Neón", "Dorado/Negro", "Colores de Tierra"])
        
        detail_level = st.select_slider("Nivel de Detalle", options=["Esquemático", "Equilibrado", "Hiper-detallado"])
        
        aspect_ratio = st.radio("Relación de Aspecto", ["1:1 (Cuadrado)", "16:9 (Horizontal)", "9:16 (Vertical)"])
        
        api_key = st.text_input("OpenAI API Key", type="password")

    # --- LÓGICA CORE (LANGCHAIN) ---
    if st.button("Generar Identidad Visual"):
        if not api_key or not concept:
            st.error("Por favor, introduce tu API Key y el concepto del logo.")
            return

        os.environ["OPENAI_API_KEY"] = api_key
        
        with st.spinner("El Director de Arte está trabajando en tu concepto..."):
            # 1. Definición del Prompt Ingenierizado
            template = """
            Eres un diseñador gráfico profesional de logos de élite. 
            Crea un prompt detallado para generar un logo basado en:
            - Concepto: {concept}
            - Estilo: {style}
            - Paleta de colores: {colors}
            - Nivel de detalle: {detail}
            
            Requisitos técnicos del prompt: Fondo blanco o plano, vectores limpios, alta resolución, 
            sin texto genérico, diseño profesional para branding.
            """
            
            prompt_template = PromptTemplate(
                input_variables=["concept", "style", "colors", "detail"],
                template=template
            )
            
            # Formateamos el prompt final
            final_prompt = prompt_template.format(
                concept=concept, 
                style=style, 
                colors=colors, 
                detail=detail_level
            )

            try:
                # 2. Conexión con DALL-E vía LangChain
                # DALL-E 3 es el estándar actual para calidad de logos
                dalle = DallEAPIWrapper(model="dall-e-3")
                image_url = dalle.run(final_prompt)

                # --- VISUALIZACIÓN ---
                st.divider()
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.image(image_url, caption=f"Logo: {style} - {colors}", use_container_width=True)
                
                with col2:
                    st.success("¡Logo generado con éxito!")
                    st.info(f"**Prompt utilizado:** \n\n {final_prompt}")
                    st.download_button("Descargar Logo (URL)", data=image_url, file_name="logo_concept.txt")

            except Exception as e:
                st.error(f"Error en la generación: {str(e)}")

if __name__ == "__main__":
    generate_logo()