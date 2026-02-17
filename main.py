import streamlit as st
import os
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper

# Configura tu token de Hugging Face (Gratis)
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "tu_token_aquí"

# 1. El "Cerebro": Usamos un modelo potente y gratuito (ej: Mistral o Llama 3)
llm_endpoint = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    task="text-generation",
    temperature=0.5
)
llm = ChatHuggingFace(llm=llm_endpoint)

# 2. La "Mano": Herramienta para generar el logo usando Stable Diffusion
def generate_logo(prompt):
    # Usamos una API gratuita de Hugging Face para Stable Diffusion
    from huggingface_hub import InferenceClient
    client = InferenceClient(token=os.environ["HUGGINGFACEHUB_API_TOKEN"])
    
    # Optimizamos el prompt para que parezca un logo profesional
    enriched_prompt = f"Professional logo design, flat vector, minimalist, white background, high quality, {prompt}"
    
    image = client.text_to_image(enriched_prompt, model="stabilityai/stable-diffusion-xl-base-1.0")
    image.save("logo_generado.png")
    return "Logo generado con éxito y guardado como 'logo_generado.png'"

logo_tool = Tool(
    name="LogoGenerator",
    func=generate_logo,
    description="Útil para crear logos. Debes pasarle una descripción visual detallada."
)

# 3. El Agente
agent = initialize_agent(
    tools=[logo_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

# 4. Prueba
agent.invoke({"input": "Diseña un logo minimalista para una tienda de surf llamada 'Blue Wave'. Usa tonos azules y formas orgánicas."})