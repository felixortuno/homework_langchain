import streamlit as st
import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Configuración de página
st.set_page_config(page_title="Gemini 2.0 Logo Studio", page_icon="⚡", layout="wide")

# Estilo CSS Moderno
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button { 
        background: linear-gradient(90deg, #3b82f6, #8b5cf6); 
        color: white; border: none; padding: 0.5rem 1rem; border-radius: 10px; font-weight: bold;
    }
    .stTextInput>div>div>input { background-color: #1f2937; color: white; }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("⚡ Gemini 2.0 Logo Studio")
    st.caption("Generación de Logos con la última tecnología de Google")

    with st.sidebar:
        st.header("Configuración")
        # Input para la API Key
        api_key = st.text_input("Google API Key", type="password")
        
        st.divider()
        brand_name = st.text_input("Nombre de la Marca")
        brand_desc = st.text_area("Descripción")
        style = st.selectbox("Estilo", ["Minimalista", "Futurista", "Geométrico", "Vintage"])
        color = st.selectbox("Color", ["Blanco y Negro", "Neón", "Pastel", "Corporativo"])

    if st.button("Generar Identidad Visual"):
        if not api_key or not brand_name:
            st.warning("⚠️ Necesitas la API Key y el nombre de la marca.")
            return

        # Configuración de credenciales
        os.environ["GOOGLE_API_KEY"] = api_key
        genai.configure(api_key=api_key)

        try:
            with st.status("🧠 Gemini 2.0 está pensando...", expanded=True) as status:
                
                # -----------------------------------------------------------
                # CAMBIO CLAVE: Usamos 'gemini-2.0-flash'
                # -----------------------------------------------------------
                # Si este falla, la alternativa segura es 'gemini-1.5-pro-latest'
                llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
                
                # Definimos el Prompt
                template = """
                Eres un experto en diseño gráfico. Escribe un prompt en INGLÉS para generar un logo.
                Marca: {brand}. Descripción: {desc}. Estilo: {style}. Color: {color}.
                Requisitos: Fondo blanco limpio, vectores, alta calidad, sin texto realista.
                Devuelve SOLO el prompt.
                """
                
                prompt_template = PromptTemplate.from_template(template)
                
                # Cadena de LangChain (LCEL)
                chain = prompt_template | llm
                
                # Ejecutamos con invoke
                response = chain.invoke({
                    "brand": brand_name,
                    "desc": brand_desc,
                    "style": style,
                    "color": color
                })
                
                final_prompt = response.content
                st.write(f"**Prompt generado:** {final_prompt}")
                
                status.update(label="🎨 Renderizando imagen con Imagen 3...", state="running")

                # -----------------------------------------------------------
                # GENERACIÓN DE IMAGEN
                # -----------------------------------------------------------
                try:
                    # Modelo de imagen de Google
                    imagen_model = genai.GenerativeModel('imagen-3.0-generate-001')
                    
                    result = imagen_model.generate_images(
                        prompt=final_prompt,
                        number_of_images=1,
                    )
                    
                    for img in result.images:
                        st.image(img, caption=f"Logo para {brand_name}", use_container_width=True)
                        
                    status.update(label="✅ ¡Éxito!", state="complete")
                    st.balloons()
                    
                except Exception as img_error:
                    st.error(f"Error generando la imagen: {img_error}")
                    st.info("Nota: Asegúrate de que tu API Key tiene permisos para 'Imagen 3' en Google AI Studio.")

        except Exception as e:
            st.error(f"Error de conexión: {str(e)}")
            st.markdown("**Posible solución:** Verifica que tu API Key sea correcta y que tengas acceso a Gemini 2.0 en tu región.")

if __name__ == "__main__":
    main()