import streamlit as st
import os
import requests
import json
import base64
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Configuración de página
st.set_page_config(page_title="Gemini 2.0 Logo Studio", page_icon="⚡", layout="wide")

# Estilos CSS
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .stButton>button { 
        background: linear-gradient(90deg, #4F46E5, #7C3AED); 
        color: white; border: none; padding: 0.5rem 1rem; border-radius: 8px; font-weight: bold;
    }
    .stTextInput>div>div>input { background-color: #1f2937; color: white; border: 1px solid #374151; }
    </style>
    """, unsafe_allow_html=True)

def generate_image_rest(api_key, prompt):
    """Genera imagen usando la API REST directamente para evitar errores de librería"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:predict?key={api_key}"
    
    headers = {"Content-Type": "application/json"}
    data = {
        "instances": [{"prompt": prompt}],
        "parameters": {"sampleCount": 1, "aspectRatio": "1:1"}
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code != 200:
        raise Exception(f"Error API Imagen ({response.status_code}): {response.text}")
    
    # Decodificar la imagen en base64
    try:
        predictions = response.json().get('predictions', [])
        if not predictions:
            raise Exception("No se generó ninguna imagen.")
        
        # La API devuelve la imagen en base64
        bytes_base64 = predictions[0]['bytesBase64Encoded']
        return base64.b64decode(bytes_base64)
    except Exception as e:
        raise Exception(f"Error procesando imagen: {str(e)}")

def main():
    st.title("⚡ Gemini 2.0 Logo Studio")
    st.caption("Powered by Gemini 2.0 Flash & Imagen 3")

    with st.sidebar:
        st.header("Configuración")
        # Usamos la API Key estándar (AI Studio)
        api_key = st.text_input("Google API Key", type="password", help="Tu clave de Google AI Studio")
        
        st.divider()
        brand_name = st.text_input("Marca")
        desc = st.text_area("Descripción")
        style = st.selectbox("Estilo", ["Minimalista", "Futurista", "Geométrico", "3D Render"])
        color = st.selectbox("Color", ["Blanco y Negro", "Neón", "Pastel", "Oro y Negro"])

    if st.button("🚀 Generar con Gemini 2.0"):
        if not api_key or not brand_name:
            st.warning("⚠️ Necesitas introducir la API Key y el nombre.")
            return

        os.environ["GOOGLE_API_KEY"] = api_key

        try:
            # ---------------------------------------------------------
            # PASO 1: TEXTO (Gemini 2.0 Flash)
            # ---------------------------------------------------------
            with st.status("🧠 Gemini 2.0 está diseñando...", expanded=True) as status:
                
                # CAMBIO CLAVE: Usamos 'gemini-2.0-flash'
                llm = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash",
                    google_api_key=api_key,
                    temperature=0.7
                )
                
                template = """
                Actúa como Director de Arte. Crea un prompt en INGLÉS para generar un logo.
                Marca: {brand}. Descripción: {desc}. Estilo: {style}. Color: {color}.
                Requisitos: Fondo blanco sólido, vectorial, alta resolución, sin texto complejo.
                Devuelve SOLO el prompt del logo.
                """
                
                chain = PromptTemplate.from_template(template) | llm
                response = chain.invoke({
                    "brand": brand_name,
                    "desc": desc,
                    "style": style,
                    "color": color
                })
                
                final_prompt = response.content
                st.write(f"**Prompt generado:** {final_prompt}")
                
                status.update(label="🎨 Generando imagen (Imagen 3)...", state="running")

                # ---------------------------------------------------------
                # PASO 2: IMAGEN (Llamada Directa REST)
                # ---------------------------------------------------------
                try:
                    # Usamos nuestra función personalizada que no falla por versiones
                    image_bytes = generate_image_rest(api_key, final_prompt)
                    
                    st.image(image_bytes, caption=f"Logo para {brand_name}", use_container_width=True)
                    status.update(label="✅ ¡Éxito!", state="complete")
                    st.balloons()
                    
                except Exception as img_error:
                    st.error(f"Fallo en Imagen: {str(img_error)}")
                    st.info("💡 Si falla la imagen, verifica que tu API Key tenga habilitado 'Google AI Studio' y créditos.")

        except Exception as e:
            st.error(f"Error general: {str(e)}")
            st.markdown("**Nota:** Si ves un error 404 aquí, asegúrate de que estás usando una API Key válida de [Google AI Studio](https://aistudio.google.com/).")

if __name__ == "__main__":
    main()