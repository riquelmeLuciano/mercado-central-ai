from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from src.loader import cargar_documentos


'''
La función crear_vectorstore coordina el proceso de cargar los documentos, 
generar embeddings y crear un vectorstore persistente.
'''
def crear_vectorstore():

    print("📚 Cargando documentos...")
    documentos = cargar_documentos()

    chunks = documentos
    print(f"✅ Se cargarán {len(chunks)} fragmentos.")


    print("🧠 Generando embeddings...")

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"       
    )

    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )

    vectorstore.add_documents(chunks)

    print("✅ Base vectorial creada correctamente.")

    return vectorstore