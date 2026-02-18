import streamlit as st

def load_css():
    """Carga los estilos CSS personalizados para la aplicación (Minimalista & Moderno)."""
    st.markdown("""
    <style>
        /* Importamos fuente moderna 'Outfit' */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
            color: #e0e0e0;
        }

        /* Fondo General - Oscuro Mate */
        .stApp {
            background-color: #0e1117;
            background-image: radial-gradient(circle at 50% 0%, #1c2333 0%, #0e1117 60%);
            background-attachment: fixed;
        }

        /* Títulos */
        h1, h2, h3, h4, h5, h6 {
            font-weight: 600;
            color: #ffffff;
            letter-spacing: -0.5px;
        }
        h1 {
            background: linear-gradient(to right, #ffffff, #a0a0a0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Sidebar - Discreto y Limpio */
        [data-testid="stSidebar"] {
            background-color: #161920;
            border-right: 1px solid #2d313a;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
             color: #d0d0d0;
        }

        /* Inputs y Selects */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
            background-color: #1e232d;
            border: 1px solid #353a47;
            color: #f7f7f7;
            border-radius: 8px;
            font-weight: 400;
        }
        .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus, .stSelectbox>div>div>div:focus {
            border-color: #5d6679;
            box-shadow: none;
        }

        /* Botones - Minimalistas */
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            background-color: #ffffff;
            color: #000000;
            border: none;
            font-weight: 500;
            padding: 0.6rem 1.2rem;
            transition: all 0.2s ease;
        }
        .stButton>button:hover {
            background-color: #e0e0e0;
            transform: translateY(-1px);
        }
        /* Botón Secundario (si lo hubiera) */
        .stButton>button[kind="secondary"] {
            background-color: transparent;
            border: 1px solid #484f60;
            color: #ffffff;
        }
        .stButton>button[kind="secondary"]:hover {
            border-color: #ffffff;
        }

        /* Contenedores y Cards */
        div[data-testid="stExpander"] {
            background-color: transparent;
            border: none;
        }
        
        /* Ajustes de espaciado */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        
        /* Links */
        a {
            color: #7b96b8;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }

        /* Status Container limpio */
        .stStatusWidget {
             background-color: #1e232d;
             border: 1px solid #353a47;
             border-radius: 8px;
        }
    </style>
    """, unsafe_allow_html=True)

def get_placeholder_image(brand_name):
    """Genera una URL para una imagen placeholder con estilo minimalista."""
    placeholder_color = "000000" # Negro puro para placeholder
    placeholder_text = brand_name.replace(" ", "+")
    return f"https://placehold.co/800x600/{placeholder_color}/FFF/png?text={placeholder_text}&font=montserrat"

def clean_svg_code(code_string):
    """
    Limpia la respuesta del LLM para extraer solo el código SVG.
    Elimina bloques de markdown ```xml ... ``` o ```svg ... ```.
    """
    code_string = code_string.strip()
    
    # Eliminar bloques de código markdown
    if "```xml" in code_string:
        code_string = code_string.replace("```xml", "").replace("```", "")
    elif "```svg" in code_string:
        code_string = code_string.replace("```svg", "").replace("```", "")
    elif "```" in code_string:
        code_string = code_string.replace("```", "")
        
    # Asegurarse de empezar con <svg y terminar con </svg>
    start_index = code_string.find("<svg")
    end_index = code_string.rfind("</svg>")
    
    if start_index != -1 and end_index != -1:
        return code_string[start_index:end_index+6]
    
    return code_string
