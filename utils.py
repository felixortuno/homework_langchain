import streamlit as st

def load_css():
    """Carga los estilos CSS personalizados para la aplicación."""
    st.markdown("""
    <style>
        /* Importamos una fuente moderna */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
        }

        /* Fondo oscuro y elegante */
        .stApp {
            background: radial-gradient(circle at top left, #1a1a2e, #16213e, #0f3460);
            color: #e0e0e0;
        }

        /* Títulos con gradiente */
        h1, h2, h3 {
            background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }

        /* Sidebar personalizado */
        [data-testid="stSidebar"] {
            background-color: rgba(22, 33, 62, 0.95);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Inputs estilizados */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #fff;
            border-radius: 12px;
        }
        .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
            border-color: #00d2ff;
            box-shadow: 0 0 10px rgba(0, 210, 255, 0.2);
        }

        /* Botón Principal */
        .stButton>button {
            width: 100%;
            border-radius: 12px;
            background: linear-gradient(90deg, #00d2ff, #3a7bd5);
            border: none;
            color: white;
            font-weight: 600;
            padding: 0.75rem 1.5rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 210, 255, 0.3);
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 210, 255, 0.5);
        }

        /* Contenedores de estado */
        .stStatusWidget {
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)

def get_placeholder_image(brand_name):
    """Genera una URL para una imagen placeholder."""
    placeholder_color = "16213e"
    placeholder_text = brand_name.replace(" ", "+")
    return f"https://placehold.co/800x600/{placeholder_color}/FFF/png?text={placeholder_text}&font=montserrat"
