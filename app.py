import streamlit as st
from src.chatbot import preguntar
from pathlib import Path

# Configura la interfaz Streamlit
st.set_page_config(
    page_title="Mercado Central AI",
    page_icon="🛒",
    layout="wide"
)

st.title("Mercado Central AI")
st.caption("Asistente de IA para consultar documentos internos.")

st.info("""
### Preguntas Frecuentes

• ¿Cuál es la política de devoluciones?

• ¿Cuáles son los requisitos para ser proveedor?

• Si un cliente pide un reembolso ¿qué hago?

• ¿Cuál es el horario de atención?
""")


# Historial de conversación
if "historial_conversacion" not in st.session_state:
    st.session_state.historial_conversacion = []

# Formulario para ingresar una pregunta
pregunta = st.chat_input("Escribe tu pregunta...")

if pregunta:

    with st.spinner("Consultando documentos..."):
        respuesta, fuentes = preguntar(pregunta)

    st.session_state.historial_conversacion.append(
        {
            "pregunta": pregunta,
            "respuesta": respuesta,
            "fuentes": fuentes
        }
    )

    st.rerun()

for mensaje in st.session_state.historial_conversacion:

    with st.chat_message("user"):
        st.write(mensaje["pregunta"])

    with st.chat_message("assistant"):

        st.write(mensaje["respuesta"])

        with st.expander("📄 Fuentes utilizadas"):

            for fuente in mensaje["fuentes"]:
                nombre = Path(fuente["archivo"]).name
                st.write(
                f"📄 **{nombre}**  |  Página **{fuente['pagina']}**"
                )


# barra lateral
with st.sidebar:

    # Boton para borrar conversaciones
    if st.sidebar.button("🗑️ Borrar conversación"):

        st.session_state.historial_conversacion = []

        st.rerun()
    

    st.divider()

    # Informacion sobre el proyecto tecnologias, modelo y Embeddings
    st.header("Informacion sobre este Proyecto")

    st.write("""
    **Tecnologías usadas:**

    - LangChain
    - Ollama
    - ChromaDB
    - Streamlit
    """)

    st.write("Modelo:")
    st.success("qwen2.5:3b")

    st.write("Embeddings:")
    st.success("nomic-embed-text")

    st.divider()
    
    # mostrar los documentos que el modelo pueda consultar
    st.subheader("📂 Documentos disponibles")

    carpeta = Path("Documentos")

    for archivo in sorted(carpeta.iterdir()):

        if archivo.suffix.lower() in [".pdf", ".xlsx"]:
         st.write(f"📄 {archivo.name}")

