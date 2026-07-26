from pathlib import Path # Clase para manejar rutas de archivos y directorios.

import pandas as pd #Biblioteca para manipulación de datos tabulares.
from langchain_core.documents import Document # Document desde langchain_core.documents: Clase que representa un documento.
from langchain_community.document_loaders import PyPDFLoader # Cargador específico para PDFs.
from langchain_text_splitters import RecursiveCharacterTextSplitter # Clase para dividir el texto en fragmentos.


# La función cargar_pdfs carga documentos en formato PDF de una carpeta y devuelve una lista de objetos Document.
# Parámetros: carpeta: Una cadena que representa la ruta de la carpeta donde se encuentran los archivos PDF.
def cargar_pdfs(carpeta="Documentos"):

    # Inicializa una lista vacía para almacenar los objetos Document y convierte el parámetro carpeta a un objeto Path.
    documentos = []
    carpeta = Path(carpeta)

    '''
    Recorre todos los archivos PDF en la carpeta especificada, carga cada uno utilizando PyPDFLoader y 
    extiende la lista de documentos con los objetos Document generados.
    '''
    for archivo in carpeta.glob("*.pdf"):
        print(f"📄 Leyendo PDF: {archivo.name}")

        loader = PyPDFLoader(str(archivo))
        documentos.extend(loader.load())

    # Devuelve la lista de objetos Document cargados.
    return documentos


# La función cargar_excel carga documentos en formato Excel de una carpeta y devuelve una lista de objetos Document.
# Parámetros: carpeta: Una cadena que representa la ruta de la carpeta donde se encuentra un archivo excel
def cargar_excel(carpeta="Documentos"):

    # inicializar
    documentos = []
    carpeta = Path(carpeta)

    '''
    Recorre todos los archivos Excel en la carpeta especificada, carga cada uno utilizando pandas, 
    y convierte cada fila del DataFrame en un objeto Document.
    '''
    for archivo in carpeta.glob("*.xlsx"):
        print(f"📊 Leyendo Excel: {archivo.name}")

        df = pd.read_excel(archivo)

        for _, fila in df.iterrows():

            texto = "\n".join(
                f"{col}: {fila[col]}"
                for col in df.columns
            )

            documentos.append(
                Document(
                    page_content=texto,
                    metadata={
                        "source": archivo.name
                    }
                )
            )

    return documentos


'''
La función cargar_documentos coordina el proceso de cargar y procesar los documentos en PDF y Excel, 
dividiendo el contenido en fragmentos más pequeños.
'''
def cargar_documentos():
    documentos = []

    documentos.extend(cargar_pdfs())
    documentos.extend(cargar_excel())

    #División del Contenido
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=150
    )
    documentos = splitter.split_documents(documentos)

    # conteo de Fragmentos
    print(f"\n✅ Total chunks: {len(documentos)}")

    return documentos