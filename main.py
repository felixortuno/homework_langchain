import streamlit as st
import os
import time

# Intentamos importar las librerías con seguridad
try:
    import google.generativeai as genai
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.prompts import PromptTemplate
except ImportError as e:
    st.error(f"⚠️ Error Crítico de Instalación: Faltan librerías. Asegúrate de que 'requirements.txt' tenga 'google-generativeai'. Detalle: {e}")
    st.stop()

# Configuración
st.set_page_config(page_title="Logo Studio Pro", page_icon="🎨", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 8px; background: linear-gradient(90deg, #4F46E5, #06B6D4); border: none; font-weight: bold; color: white; }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🎨 Gemini Logo Studio (Modo Seguro)")
    st.caption("Sistema robusto para cuentas con Google Cloud Credits")

    with st.sidebar:
        st.header("Configuración")
        # Usamos la API Key estándar para evitar líos de JSON de cuentas de servicio
        api_key = st.text_input("Google API Key", type="password", help="Tu clave AIza...")
        
        st.divider()
        brand = st.text_input("Marca", "Ej: TechNova")
        desc = st.text_area("Descripción", "Ej: Empresa de ciberseguridad")
        style = st.selectbox("Estilo", ["Minimalista", "Futurista", "Geométrico", "3D"])

    if st.button("🚀 Crear Logo"):
        if not api_key or not brand:
            st.warning("⚠️ Faltan datos (API Key o Marca).")
            return

        os.environ["GOOGLE_API_KEY"] = api_key
        genai.configure(api_key=api_key)

        try:
            # --- FASE 1: GEMINI PIENSA EL DISEÑO ---
            with st.status("🧠 Gemini está diseñando...", expanded=True) as status:
                
                # Usamos 1.5 Flash que es el modelo más estable ahora mismo
                llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
                
                prompt_template = PromptTemplate.from_template(
                    "Eres un diseñador experto. Crea un prompt en INGLÉS para un logo de: {brand}. "
                    "Descripción: {desc}. Estilo: {style}. "
                    "Requisitos: Fondo blanco, vectorial, minimalista. Solo devuelve el prompt."
                )
                
                chain = prompt_template | llm
                response = chain.invoke({"brand": brand, "desc": desc, "style": style})
                final_prompt = response.content
                
                st.info(f"**Diseño Conceptual:** {final_prompt}")
                status.update(label="🎨 Intentando generar imagen...", state="running")

                # --- FASE 2: GENERACIÓN DE IMAGEN (CON RED DE SEGURIDAD) ---
                try:
                    # Intento 1: Usar el modelo Imagen 3 (puede fallar si la cuenta no tiene whitelist)
                    model_imagen = genai.GenerativeModel('imagen-3.0-generate-001')
                    result = model_imagen.generate_content(final_prompt)
                    
                    # Verificamos si realmente devolvió algo visual
                    if hasattr(result, 'parts') and result.parts:
                         st.image(result.parts[0].inline_data.data, caption="Generado con Imagen 3")
                         st.balloons()
                    else:
                        raise Exception("El modelo no devolvió datos de imagen.")

                except Exception as img_error:
                    # PLAN B: Si falla, mostramos el error pero NO ROMPEMOS la app
                    status.update(label="⚠️ Aviso de Google Cloud", state="complete")
                    st.warning(f"No se pudo generar la imagen real (Error: {img_error}).")
                    
                    st.markdown("### 🛠️ Diagnóstico para tu cuenta de 1000€:")
                    st.markdown("""
                    Aunque tienes créditos, **Google restringe el acceso a Imagen 3 por API Key**.
                    Para que funcione, necesitas habilitar **Vertex AI API** en tu consola de Google Cloud.
                    
                    **Mientras tanto, aquí tienes una simulación de cómo quedaría:**
                    """)
                    # Generamos un placeholder visual elegante
                    st.image(f"https://placehold.co/600x600/111/FFF/png?text={brand}+Logo", caption="Placeholder de Diseño")

        except Exception as e:
            st.error(f"Error General: {str(e)}")

if __name__ == "__main__":
    main()