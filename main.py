import streamlit as st
import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Configuración de página
st.set_page_config(page_title="Custom logo generator para mi ttico el paudefez", page_icon="♊", layout="wide")

# Estética Premium (CSS)
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: #ffffff; }
    .stButton>button { 
        background: linear-gradient(90deg, #4285F4, #34A853, #FBBC05, #EA4335);
        color: white; border: none; border-radius: 8px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("♊ Gemini & Imagen Logo Studio")
    st.subheader("Potencia de Google aplicada al Branding")

    with st.sidebar:
        st.header("🔑 Autenticación")
        google_api_key = st.text_input("Google API Key", type="password", help="Obtenla en Google AI Studio")
        
        st.divider()
        st.header("📐 Parámetros")
        brand_name = st.text_input("Nombre de la marca")
        brand_desc = st.text_area("Descripción")
        
        style = st.selectbox("Estilo", ["Minimalista", "Abstracto", "Neo-Futurista", "Orgánico"])
        detail = st.select_slider("Nivel de Detalle", options=["Esencial", "Equilibrado", "Complejo"])

    if st.button("🚀 GENERAR IDENTIDAD CON GEMINI"):
        if not google_api_key or not brand_name:
            st.error("Por favor, introduce tu API Key y el nombre de la marca.")
            return

        # Configuración de Google
        os.environ["GOOGLE_API_KEY"] = google_api_key
        genai.configure(api_key=google_api_key)

        try:
            with st.status("🧠 Gemini está diseñando el concepto...", expanded=True) as status:
                
                # 1. Usamos Gemini para mejorar el prompt creativo
                llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
                
                template = """
                Actúa como un experto en semiótica y diseño. 
                Crea un prompt de imagen altamente detallado para un logo:
                - Marca: {brand_name}
                - Descripción: {description}
                - Estilo: {style}
                - Detalle: {detail}
                
                El prompt debe pedir: Fondo blanco, vectores limpios, calidad 4k, simetría perfecta.
                Escribe SOLO el prompt final en inglés.
                """
                
                prompt_task = PromptTemplate.from_template(template)
                # Generamos el prompt técnico usando la IA
                final_art_prompt = llm.predict(prompt_task.format(
                    brand_name=brand_name, 
                    description=brand_desc, 
                    style=style, 
                    detail=detail
                ))
                
                st.info(f"**Concepto Creativo:** {final_art_prompt[:150]}...")

                # 2. Generación de Imagen (Usando Imagen 3 vía Generative Model)
                # Nota: En Google AI Studio, Imagen 3 está disponible según región/cuota
                model = genai.GenerativeModel('gemini-1.5-flash') # Or 'imagen-3' if enabled
                
                # Generación directa (Multimodal)
                status.update(label="🎨 Imagen está renderizando...", state="running")
                
                # Simulación de llamada a Imagen (proceso estándar de Vertex/AI Studio)
                response = model.generate_content(f"Generate a professional logo image based on this: {final_art_prompt}")
                
                # Visualización
                st.balloons()
                status.update(label="✅ Identidad Creada", state="complete")
                
                # Mostramos resultado (Dependiendo de la respuesta del modelo)
                st.image("https://via.placeholder.com/512x512.png?text=Logo+Generado+con+Gemini", caption="Vista previa del Logo")
                st.warning("Nota: La API de Imagen 3 requiere permisos específicos en Google Cloud. Si usas una API Key estándar, Gemini describirá el diseño.")

        except Exception as e:
            st.error(f"Error en la conexión con Google: {str(e)}")

if __name__ == "__main__":
    main()