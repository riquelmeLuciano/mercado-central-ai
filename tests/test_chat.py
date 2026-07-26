from src.chatbot import preguntar

if __name__ == "__main__":
  
    while True:

        pregunta = input("\nPregunta: ")

        if pregunta.lower() == "salir":
            break

        respuesta, fuentes = preguntar(pregunta)

        print("\nRespuesta:\n")
        print(respuesta)

        print("\nFuentes:")

        for fuente in fuentes:
            print("-", fuente)