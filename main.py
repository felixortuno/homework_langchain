import streamlit as st
import os
import time
import io
from utils import load_css, get_placeholder_image

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
        st.markdown("**Diseño de marcas impulsado por Gemini 2.0 Flash**")
    with col2:
        # Placeholder para un logo o animación si se desea
        pass

    st.divider()

    with st.sidebar:
        st.header("⚙️ Configuración")
        api_key = st.text_input("Google API Key", type="password", help="Tu clave de API de Google AI Studio")
        
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
            status_container.write("💡 Generando prompt óptimo con Gemini 2.0...")
            
            # Actualizado a gemini-2.0-flash-exp (o la versión disponible más reciente)
            llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key, temperature=0.7)
            
            prompt_template = PromptTemplate.from_template(
                """
                Actúa como un Director de Arte de clase mundial. Tu tarea es crear un prompt de generación de imagen (en INGLÉS) altamente detallado para un logo.
                
                Marca: {brand}
                Descripción del negocio: {desc}
                Estilo deseado: {style}
                Paleta de Colores Preferida: {palette}
                
                Requisitos del prompt:
                - Debe ser descriptivo, centrado en la composición visual, colores, iluminación y estilo.
                - Incluye palabras clave como "vector logo", "white background", "high quality", "professional design", "minimalist".
                - Asegurate de que el prompt refleje la paleta de colores "{palette}".
                - NO incluyas explicaciones, SOLAMENTE devuelve el prompt en inglés.
                """
            )
            
            chain = prompt_template | llm
            response = chain.invoke({"brand": brand, "desc": desc, "style": style, "palette": color_palette})
            final_prompt = response.content.strip()
            
            status_container.write("✨ Diseño conceptual creado.")
            st.success(f"**Prompt Generado:** {final_prompt}")
            
            # --- FASE 2: GENERACIÓN DE IMAGEN ---
            status_container.update(label="🎨 Renderizando logo (Imagen 3)...", state="running")
            
            try:
                # Usamos Imagen 3
                model_imagen = genai.GenerativeModel('imagen-3.0-generate-001')
                result = model_imagen.generate_content(final_prompt)
                
                if hasattr(result, 'parts') and result.parts:
                    status_container.update(label="✅ ¡Logo generado con éxito!", state="complete", expanded=False)
                    
                    st.divider()
                    col_img, col_details = st.columns([2, 1])
                    
                    # Extraer datos de la imagen
                    img_data = result.parts[0].inline_data.data
                    
                    # Guardar en historial
                    st.session_state.generated_logos.insert(0, {
                        "brand": brand,
                        "image": img_data,
                        "prompt": final_prompt,
                        "time": time.strftime("%H:%M:%S")
                    })
                    
                    with col_img:
                        st.image(img_data, caption=f"Logo para {brand}", use_column_width=True)
                        st.balloons()
                    
                    with col_details:
                        st.markdown("### 📥 Resultados")
                        st.markdown("Tu logo ha sido generado utilizando la última tecnología de Google Imagen 3.")
                        
                        # Botón de descarga
                        st.download_button(
                            label="📥 Descargar Logo Original",
                            data=img_data,
                            file_name=f"logo_{brand.replace(' ', '_').lower()}.png",
                            mime="image/png",
                            key="download_btn_main"
                        )
                else:
                    raise Exception("La API no devolvió datos de imagen válidos.")

            except Exception as img_error:
                status_container.update(label="⚠️ Aviso de Generación", state="complete", expanded=True)
                st.error(f"No se pudo generar la imagen final directamente. Error: {img_error}")
                st.caption("Nota: Imagen 3 en AI Studio puede requerir acceso de Trusted Tester o Vertex AI.")
                
                # PLAN B Mejorado
                st.markdown("---")
                
                # Placeholder dinámico
                st.image(get_placeholder_image(brand), caption="Previsualización de Estructura")
                
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
                st.image(logo["image"], caption=f"{logo['brand']} ({logo['time']})", use_column_width=True)
                st.download_button(
                    label="📥 Descargar",
                    data=logo["image"],
                    file_name=f"history_logo_{i}.png",
                    mime="image/png",
                    key=f"history_btn_{i}"
                )
                with st.expander("Ver Prompt"):
                    st.code(logo["prompt"], language="text")

if __name__ == "__main__":
    main()