from src.loader import cargar_documentos

if __name__ == "__main__":

    docs = cargar_documentos()

    print("\n====================")
    print(docs[0].metadata)
    print("====================\n")

    print(docs[0].page_content[:800])