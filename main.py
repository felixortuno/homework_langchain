import streamlit as st
import os
import time
import io
from utils import load_css, get_placeholder_image, clean_svg_code

# Intentamos importar las librerías con seguridad
try:
    import google.generativeai as genai
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.prompts import PromptTemplate
except ImportError as e:
    st.error(f"⚠️ Error Crítico de Instalación: Faltan librerías. Asegúrate de que 'requirements.txt' tenga 'google-generativeai'. Detalle: {e}")
    st.stop()

# Configuración de la página
st.set_page_config(page_title="Creador de Logos IA", page_icon="🎨", layout="wide")

# Cargar estilos CSS Minimalistas
load_css()

# Inicializar Estado de Sesión para Historial
if 'generated_logos' not in st.session_state:
    st.session_state.generated_logos = []

def main():
    # --- SIDEBAR (Configuración) ---
    with st.sidebar:
        st.header("Configuración")
        api_key = st.text_input("Clave de Google (API Key)", type="password", help="Tu llave para usar la Inteligencia Artificial de Google")
        
        st.markdown("### Tu Marca")
        brand = st.text_input("Nombre de tu negocio", placeholder="Ej: Cafetería Aroma")
        desc = st.text_area("¿A qué te dedicas?", placeholder="Ej: Vendemos café de especialidad y pasteles caseros...", height=80)
        
        st.markdown("### Estilo")
        style = st.selectbox("Estilo Visual", ["Minimalista y Limpio", "Moderno y Tecnológico", "Geométrico", "Elegante", "Divertido", "Orgánico y Natural"])
        color_palette = st.selectbox("Colores", ["La IA decide", "Blanco y Negro", "Un solo color", "Cálidos (Rojos, Naranjas)", "Fríos (Azules, Verdes)", "Colores Pastel"])
        
        # Debug Tools (Más discreto)
        with st.expander("Opciones Avanzadas"):
            if st.button("Verificar Conexión"):
                if not api_key:
                    st.toast("Falta la Clave API")
                else:
                    try:
                        genai.configure(api_key=api_key)
                        st.toast("✅ Conexión establecida correctamente")
                    except Exception as e:
                        st.error(f"Error: {e}")

    # --- MAIN AREA ---
    # Encabezado Minimalista
    st.title("Creador de Logos IA")
    st.markdown("Diseña logotipos **profesionales y editables** en segundos usando Inteligencia Artificial.")
    st.markdown("---")

    # Botón de Acción Principal (Centrado o ancho completo)
    col_action, _ = st.columns([1, 2])
    with col_action:
        generate_btn = st.button("✨ ¡Crear mi Logo!", type="primary")

    if generate_btn:
        if not api_key:
            st.warning("⚠️ Necesitas poner tu Clave API en el menú de la izquierda.")
            return
        if not brand:
            st.warning("⚠️ Escribe el nombre de tu marca.")
            return

        os.environ["GOOGLE_API_KEY"] = api_key
        genai.configure(api_key=api_key)

        # Contenedor de estado limpio
        status_text = st.empty()
        status_text.caption("⏳ Iniciando la magia...")
        
        try:
            # --- FASE 1: GEMINI 2.0 FLASH (Diseño & Código) ---
            status_text.caption("🎨 La IA está dibujando tu logo...")
            
            llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key, temperature=0.7)
            
            svg_prompt_template = PromptTemplate.from_template(
                """
                Role: Senior Graphic Designer & SVG Coder.
                Task: Create a MINIMALIST, PROFESSIONAL SVG LOGO.
                
                Brand Info:
                - Name: {brand}
                - Description: {desc}
                - Style: {style}
                - Palette: {palette}
                
                Requirements:
                1. Use simple geometric shapes and clean typography (sans-serif).
                2. Use a square viewbox (e.g., 0 0 512 512).
                3. The logo MUST include the brand name "{brand}".
                4. Use gradients (defs) if appropriate for the style, otherwise flat colors.
                5. RETURN ONLY THE RAW SVG CODE. No markdown blocks.
                """
            )
            
            chain = svg_prompt_template | llm
            response = chain.invoke({"brand": brand, "desc": desc, "style": style, "palette": color_palette})
            
            # Limpiar SVG
            svg_code = clean_svg_code(response.content)
            
            if "<svg" in svg_code:
                status_text.empty() # Limpiar estado
                
                logo_data = {
                    "brand": brand,
                    "svg": svg_code,
                    "time": time.strftime("%H:%M:%S")
                }
                # Guardar en historial
                st.session_state.generated_logos.insert(0, logo_data)
                
                # --- RESULTADO PRINCIPAL ---
                st.subheader("¡Aquí tienes tu logo!")
                
                col_display, col_info = st.columns([1, 1])
                
                with col_display:
                    # Renderizado SVG con fondo transparente/claro para contraste
                    st.markdown(f'''
                        <div style="
                            background-color: transparent; 
                            border: 1px solid #333; 
                            border-radius: 12px; 
                            padding: 20px; 
                            text-align: center;">
                            {svg_code}
                        </div>
                    ''', unsafe_allow_html=True)
                
                with col_info:
                    st.markdown(f"**Marca:** {brand}")
                    st.markdown(f"**Estilo:** {style}")
                    st.success("✅ Formato de Alta Calidad (Vector)")
                    
                    st.download_button(
                        label="Descargar Archivo",
                        data=svg_code.encode('utf-8'),
                        file_name=f"logo_{brand.lower().replace(' ', '_')}.svg",
                        mime="image/svg+xml"
                    )
                    
            else:
                status_text.error("No se pudo generar el logo. Inténtalo de nuevo.")

        except Exception as e:
            status_text.error(f"Ocurrió un error: {str(e)}")

    # --- HISTORIAL (Colapsable) ---
    if st.session_state.generated_logos:
        st.markdown("---")
        with st.expander("📂 Ver mis diseños anteriores"):
            cols = st.columns(4) # 4 columnas para miniaturas
            for i, logo in enumerate(st.session_state.generated_logos[:8]): # Mostrar solo los últimos 8
                with cols[i % 4]:
                    if "svg" in logo:
                         st.markdown(f'''
                            <div style="
                                border: 1px solid #2d313a; 
                                border-radius: 8px; 
                                padding: 10px; 
                                margin-bottom: 10px;
                                background: #161920;">
                                {logo["svg"]}
                            </div>
                         ''', unsafe_allow_html=True)
                         st.caption(logo['brand'])
                         st.download_button(
                            label="↓",
                            data=logo["svg"].encode('utf-8'),
                            file_name=f"history_logo_{i}.svg",
                            mime="image/svg+xml",
                            key=f"hist_btn_{i}",
                            help="Descargar este logo"
                        )

if __name__ == "__main__":
    main()