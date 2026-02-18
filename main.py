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
st.set_page_config(page_title="Logo Studio Pro | AI Design", page_icon="✨", layout="wide")

# Cargar estilos CSS
load_css()

# Inicializar Estado de Sesión para Historial
if 'generated_logos' not in st.session_state:
    st.session_state.generated_logos = []

def main():
    # Encabezado Hero
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("✨ Logo Studio Pro")
        st.markdown("**Diseño de marcas Vectoriales (SVG) con Gemini 2.0 Flash**")
    with col2:
        # Placeholder para un logo o animación si se desea
        pass

    st.divider()

    with st.sidebar:
        st.header("⚙️ Configuración")
        api_key = st.text_input("Google API Key", type="password", help="Tu clave de API de Google AI Studio")
        
        # Sección de Depuración
        with st.expander("🛠️ Herramientas de Depuración"):
            col_debug1, col_debug2 = st.columns(2)
            
            with col_debug1:
                if st.button("🔍 Verificar Imagen 3"):
                    if not api_key:
                        st.error("Falta API Key")
                    else:
                        try:
                            genai.configure(api_key=api_key)
                            models = [m.name for m in genai.list_models()]
                            if 'models/imagen-3.0-generate-001' in models:
                                st.success("✅ TIENES ACCESO a Imagen 3")
                            else:
                                st.error("❌ NO TIENES ACCESO a Imagen 3")
                                st.caption("Usando modo SVG por defecto.")
                        except Exception as e:
                            st.error(f"Error: {e}")

            with col_debug2:
                if st.button("📋 Listar Todos"):
                    if not api_key:
                        st.error("Falta API Key")
                    else:
                        try:
                            genai.configure(api_key=api_key)
                            models = list(genai.list_models())
                            st.write("Modelos encontrados:")
                            for m in models:
                                st.code(f"{m.name}")
                        except Exception as e:
                            st.error(f"Error: {e}")

        st.markdown("---")
        st.subheader("📝 Detalles de la Marca")
        brand = st.text_input("Nombre de la Marca", placeholder="Ej: NebulaTech")
        desc = st.text_area("Descripción del Negocio", placeholder="Ej: Startup de inteligencia artificial y exploración espacial...", height=100)
        
        # Nuevas Opciones
        style = st.selectbox("Estilo Visual", ["Minimalista & Limpio", "Futurista & Neón", "Geométrico & Abstracto", "Lujoso & Elegante", "Retro & Vintage", "3D & Renderizado"])
        color_palette = st.selectbox("Paleta de Colores", ["IA Decide (Automático)", "Cálido (Rojos, Naranjas)", "Frío (Azules, Verdes)", "Monocromático (B/N)", "Pastel & Suave", "Alto Contraste & Vibrante"])
        
        st.markdown("---")
        st.info("💡 **Tip:** Describe detalladamente los valores de tu marca para mejores resultados.")

    # Área Principal
    if st.button("🚀 Generar Concepto y Logo", type="primary"):
        if not api_key:
            st.warning("⚠️ Por favor, introduce tu Google API Key en la barra lateral.")
            return
        if not brand:
            st.warning("⚠️ Por favor, escribe el nombre de tu marca.")
            return

        os.environ["GOOGLE_API_KEY"] = api_key
        genai.configure(api_key=api_key)

        status_container = st.status("🧠 Analizando identidad de marca...", expanded=True)
        
        try:
            # --- FASE 1: GEMINI 2.0 FLASH PIENSA EL DISEÑO ---
            status_container.write("💡 Generando concepto de diseño...")
            
            # Usamos Gemini 2.0 Flash para todo
            llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key, temperature=0.7)
            
            # Prompt para generar código SVG directamente
            svg_prompt_template = PromptTemplate.from_template(
                """
                Eres un experto diseñador gráfico y programador SVG.
                Tu tarea es crear un LOGO VECTORIAL (SVG) para una marca.
                
                Detalles del Logo:
                - Marca: {brand}
                - Qué hace: {desc}
                - Estilo: {style}
                - Paleta de Colores: {palette}
                
                Instrucciones:
                1. Crea un diseño de logo {style} creativo y profesional.
                2. Usa formas geométricas simples, degradados (defs), y buena tipografía (usa fuentes estándar sans-serif).
                3. El SVG debe ser perfectamente escalable, viewbox cuadrada recomendada (ej. 0 0 512 512).
                4. Asegúrate de incluir el nombre "{brand}" en el diseño.
                5. DEBES RESPONDER ÚNICAMENTE CON EL CÓDIGO SVG.
                6. No incluyas markdown, ni ```xml, ni explicaciones. Solo el código raw.
                """
            )
            
            chain = svg_prompt_template | llm
            
            status_container.write("🎨 Escribiendo código vectorial SVG...")
            response = chain.invoke({"brand": brand, "desc": desc, "style": style, "palette": color_palette})
            
            # Limpiar y obtener el código SVG
            svg_code = clean_svg_code(response.content)
            
            if "<svg" in svg_code:
                status_container.update(label="✅ ¡Logo Vectorial generado!", state="complete", expanded=False)
                
                st.divider()
                col_img, col_details = st.columns([2, 1])
                
                # Guardar en historial
                st.session_state.generated_logos.insert(0, {
                    "brand": brand,
                    "svg": svg_code,
                    "time": time.strftime("%H:%M:%S")
                })
                
                with col_img:
                    # Renderizar SVG usando HTML para que se vea bien
                    st.markdown(f'<div style="background: transparent; padding: 20px; border-radius: 10px; border: 1px solid #333;">{svg_code}</div>', unsafe_allow_html=True)
                    st.balloons()
                
                with col_details:
                    st.markdown("### 📥 Resultados")
                    st.markdown("Tu logo ha sido generado en formato **Vectorial (SVG)**.")
                    st.info("Los SVGs son escalables infinitamente y perfectos para impresión y web.")
                    
                    # Botón de descarga SVG (convertido a bytes)
                    st.download_button(
                        label="📥 Descargar SVG (Vector)",
                        data=svg_code.encode('utf-8'),
                        file_name=f"logo_{brand.replace(' ', '_').lower()}.svg",
                        mime="image/svg+xml",
                        key="download_btn_main_svg"
                    )
            else:
                raise Exception("El modelo no generó un código SVG válido.")

        except Exception as e:
            status_container.update(label="❌ Error en el proceso", state="error")
            st.error(f"Ocurrió un error inesperado: {str(e)}")

    # --- HISTORIAL DE DISEÑOS ---
    if st.session_state.generated_logos:
        st.markdown("---")
        st.subheader("📚 Historial de Sesión")
        
        # Mostrar en grid de 3 columnas
        cols = st.columns(3)
        for i, logo in enumerate(st.session_state.generated_logos):
            with cols[i % 3]:
                if "svg" in logo:
                     # Renderizar pequeño en historial
                     st.markdown(f'<div style="max-height: 200px; overflow: hidden; border: 1px solid #444; border-radius: 8px; padding: 10px;">{logo["svg"]}</div>', unsafe_allow_html=True)
                     st.caption(f"{logo['brand']} ({logo['time']})")
                     st.download_button(
                        label="📥 Descargar SVG",
                        data=logo["svg"].encode('utf-8'),
                        file_name=f"history_logo_{i}.svg",
                        mime="image/svg+xml",
                        key=f"history_btn_{i}"
                    )
                else:
                    # Soporte retroactivo para imágenes
                    st.warning("Formato antiguo")

if __name__ == "__main__":
    main()