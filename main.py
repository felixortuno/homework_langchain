import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# --- IMPORTACIONES PARA VERTEX AI (CUENTA DE PAGO) ---
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

# Configuración de página
st.set_page_config(page_title="Vertex AI Logo Studio", page_icon="☁️", layout="wide")

# Estilo CSS
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button { 
        background: linear-gradient(90deg, #4285F4, #34A853); 
        color: white; border: none; padding: 0.5rem 1rem; border-radius: 8px; font-weight: bold;
    }
    .stTextInput>div>div>input { background-color: #1f2937; color: white; }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("☁️ Vertex AI Logo Studio (Pro)")
    st.caption("Usando tu cuenta profesional de Google Cloud")

    with st.sidebar:
        st.header("Credenciales de Google Cloud")
        st.info("Estos datos están en tu consola de Google Cloud.")
        # Inputs para Vertex AI
        project_id = st.text_input("Google Cloud Project ID", placeholder="ej: mi-proyecto-123")
        location = st.text_input("Región", value="us-central1", placeholder="us-central1")
        # La API Key sigue siendo necesaria para la parte de texto (Gemini) via LangChain
        api_key = st.text_input("API Key (para Gemini)", type="password")

        st.divider()
        st.header("Diseño")
        brand = st.text_input("Marca")
        desc = st.text_area("Descripción")
        style = st.selectbox("Estilo", ["Minimalista", "Corporativo", "Abstracto 3D", "Emblema"])

    if st.button("🚀 Generar con Vertex AI"):
        if not api_key or not project_id or not location or not brand:
            st.warning("⚠️ Faltan datos. Asegúrate de poner el Project ID, Región y API Key.")
            return

        # Configuración de entorno para LangChain
        os.environ["GOOGLE_API_KEY"] = api_key

        try:
            with st.status("🧠 Gemini (Texto) está pensando...", expanded=True) as status:
                # ---------------------------------------------------------
                # PASO 1: GEMINI GENERA EL PROMPT (Usando LangChain)
                # ---------------------------------------------------------
                # Usamos gemini-1.5-pro que es muy estable para esto
                llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
                
                template = """
                Crea un prompt detallado en INGLÉS para un logo profesional.
                Marca: {brand}. Descripción: {desc}. Estilo: {style}.
                Requisitos: Fondo blanco sólido, vectorial, alta calidad, sin texto realista.
                Devuelve SOLO el prompt.
                """
                prompt_chain = PromptTemplate.from_template(template) | llm
                
                response = prompt_chain.invoke({"brand": brand, "desc": desc, "style": style})
                final_prompt = response.content
                st.write(f"**Prompt Maestro:** {final_prompt}")
                
                status.update(label="🎨 Vertex AI (Imagen 3) está renderizando...", state="running")

                # ---------------------------------------------------------
                # PASO 2: IMAGEN 3 (Usando SDK Oficial de Vertex AI)
                # ---------------------------------------------------------
                try:
                    # 1. Inicializar Vertex AI con tu proyecto y región
                    vertexai.init(project=project_id, location=location)
                    
                    # 2. Cargar el modelo Imagen 3
                    model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                    
                    # 3. Generar la imagen
                    images = model.generate_images(
                        prompt=final_prompt,
                        number_of_images=1,
                        aspect_ratio="1:1"
                    )
                    
                    # 4. Mostrar resultado
                    if images:
                        # Las imágenes de Vertex vienen en un formato especial, se muestran así:
                        st.image(images[0]._pil_image, caption=f"Logo Pro para {brand}", use_container_width=True)
                        status.update(label="✅ ¡Logo Profesional Generado!", state="complete")
                        st.balloons()
                    else:
                        status.update(label="⚠️ No se generó ninguna imagen.", state="error")

                except Exception as vertex_error:
                    st.error(f"Error en Vertex AI: {vertex_error}")
                    st.markdown("""
                    **Posibles causas con cuenta de pago:**
                    1. ¿Está habilitada la **API de Vertex AI** en tu proyecto de Google Cloud?
                    2. ¿Es correcto el **Project ID**?
                    3. ¿La **Región** (ej. `us-central1`) soporta Imagen 3?
                    """)

        except Exception as e:
            st.error(f"Error general: {str(e)}")

if __name__ == "__main__":
    main()