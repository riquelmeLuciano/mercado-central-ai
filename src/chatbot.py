from langchain_chroma import Chroma  # Una clase que proporciona una base de datos de vectores persistente para almacenar y buscar información.
from langchain_ollama import OllamaEmbeddings, ChatOllama # Clase que permite generar embeddings utilizando un modelo pre-entrenado llamado "nomic-embed-text".

#Crea una instancia de OllamaEmbeddings con el modelo "nomic-embed-text" para generar embeddings.
embeddings = OllamaEmbeddings(model="nomic-embed-text")

'''
Crea una instancia de Chroma, que se utilizará como vectorstore. 
El directorio "chroma_db" será utilizado para almacenar los datos persistente, y 
el objeto de embeddings creado anteriormente será usado para generar vectores.
'''
vectorstore = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

'''
Crea una instancia de ChatOllama utilizando el modelo "qwen2.5:3b". 
El parámetro temperature se establece en 0 para garantizar respuestas más predecibles y menos creativas.
'''
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)

'''
La función preguntar toma una pregunta como entrada y devuelve una respuesta 
basada en el contexto disponible en el vectorstore.
Parámetros: pregunta --> Una cadena que representa la pregunta a responder.
'''
def preguntar(pregunta):

    #Búsqueda de Documentos Relevantes:
    documentos = vectorstore.similarity_search(
        pregunta,
        k=6   #-->  buscar los 6 documentos más similares a la pregunta.
    )

    #Combina el contenido de los documentos seleccionados en un solo string separado por dos saltos de línea.
    contexto = "\n\n".join(
        doc.page_content for doc in documentos
    )

    #Crea un prompt basado en el contexto y la pregunta para que la IA genere una respuesta.
    prompt = f"""
Eres un asistente para empleados de Mercado Central 24h.

Responde únicamente utilizando la información del contexto.

Si no existe información suficiente responde:

"Disculpe, No encontre esa información en los documentos."

Contexto:

{contexto}

Pregunta:
{pregunta}

Respuesta:
"""

    #Utiliza el método invoke del objeto de IA para generar una respuesta basada en el prompt.
    respuesta = llm.invoke(prompt)

    #Recorre los documentos seleccionados y extrae la información de las metadatos, incluyendo el nombre del archivo y la página.
    fuentes = []
    for doc in documentos:

        fuentes.append({
            "archivo": doc.metadata.get("source", "Desconocido"),
            "pagina": doc.metadata.get("page", 0) + 1
        })

    #Devuelve la respuesta generada por la IA y una lista de fuentes utilizadas para obtener la información.
    return respuesta.content, fuentes
