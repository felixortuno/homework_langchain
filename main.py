import streamlit as st
import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Configuración de la página
st.set_page_config(page_title="Gemini Logo Studio", page_icon="🎨", layout="wide")

# Estilos CSS Modernos (Dark Mode Google Style)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    .stButton>button { 
        background: linear-gradient(90deg, #4285F4, #9B72CB); 
        color: white; border: none; border-radius: 8px; height: 50px; font-weight: bold;
    }
    .stTextInput>div>div>input { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("🎨 Gemini Logo Studio")
    st.caption("Powered by Gemini 1.5 & Imagen 3")

    # --- SIDEBAR ---
    with st.sidebar:
        st.header("Configuración")
        api_key = st.text_input("Google AI Studio Key", type="password", help="Pega tu API Key de Google aquí")
        
        st.divider()
        brand = st.text_input("Nombre de la Marca")
        desc = st.text_area("Descripción del Negocio")
        
        style = st.selectbox("Estilo", ["Minimalista", "3D Render", "Abstracto", "Geométrico", "Ilustración"])
        color = st.selectbox("Color Principal", ["Azul Tecnológico", "Negro Lujo", "Verde Eco", "Naranja Vibrante"])

    # --- ÁREA PRINCIPAL ---
    if st.button("✨ Generar Identidad Visual"):
        if not api_key or not brand:
            st.warning("⚠️ Necesitas poner la API Key y el nombre de la marca.")
            return

        # Configuración de credenciales
        os.environ["GOOGLE_API_KEY"] = api_key
        genai.configure(api_key=api_key)

        try:
            # ---------------------------------------------------------
            # PASO 1: GENERACIÓN DEL PROMPT (TEXTO) CON GEMINI
            # ---------------------------------------------------------
            with st.status("🧠 Gemini está diseñando el concepto...", expanded=True) as status:
                
                # Instanciamos el modelo de CHAT (Ojo: Usamos .invoke, no .predict)
                llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
                
                prompt_template = PromptTemplate.from_template(
                    "Actúa como un diseñador experto. Crea un prompt en INGLÉS para generar un logo de la marca '{brand}'. "
                    "Descripción: {desc}. Estilo: {style}. Color: {color}. "
                    "El prompt debe ser descriptivo, pedir fondo blanco limpio, alta resolución y vector style. "
                    "Solo devuelve el prompt, nada más."
                )
                
                # SINTAXIS MODERNA (LCEL): Chain = Prompt | LLM
                chain = prompt_template | llm
                
                # Ejecutamos con .invoke()
                response = chain.invoke({
                    "brand": brand, 
                    "desc": desc, 
                    "style": style, 
                    "color": color
                })
                
                # Extraemos el texto del objeto AIMessage
                final_prompt = response.content
                st.write(f"**Prompt Optimizado:** {final_prompt}")
                
                status.update(label="✅ Concepto creado. Generando imagen...", state="running")

                # ---------------------------------------------------------
                # PASO 2: GENERACIÓN DE IMAGEN (IMAGEN 3)
                # ---------------------------------------------------------
                # Intentamos usar el modelo 'imagen-3.0-generate-001'
                # Nota: Si tu API Key no tiene permisos para Imagen, esto dará error.
                try:
                    # Usamos la librería directa de Google (genai) porque es más estable para imágenes que LangChain
                    imagen_model = genai.GenerativeModel('imagen-3.0-generate-001')
                    
                    # Llamada a la API de Imagen
                    result = imagen_model.generate_images(
                        prompt=final_prompt,
                        number_of_images=1,
                    )
                    
                    # Visualización
                    for image in result.images:
                        st.image(image, caption=f"Logo para {brand}", use_container_width=True)
                        
                    status.update(label="🎉 ¡Logo Completado!", state="complete")
                    st.balloons()
                    
                except Exception as img_error:
                    status.update(label="⚠️ Error en Imagen", state="error")
                    st.error(f"No se pudo generar la imagen. Tu API Key podría no tener acceso a 'Imagen 3' todavía. Error: {img_error}")
                    st.info("💡 Intenta usar 'gemini-pro-vision' o verifica tu acceso en Google AI Studio.")

        except Exception as e:
            st.error(f"Error general: {str(e)}")

if __name__ == "__main__":
    main()