from analisisLexico import lexer


# Función para preprocesar el código fuente
def preprocesar_codigo(codigoFuente):
    resultado = []
    lexer.input(codigoFuente)

    while True:
        tok = lexer.token()
        if not tok:
            break
        if tok.type == "IMPORT":
            # Leer el contenido del archivo importado
            resultado.append("IMPORT")
        elif tok.type == "COMENTARIO":
            continue  # Ignorar comentarios
        else:
            resultado.append(tok.value)

    print("resultado", resultado)
    codigo_preprocesado = "".join(resultado)

    return codigo_preprocesado


# Código de prueba
programa = """
import "libreria.txt"
const PI = 3.141592654

const E = 2.718281828
a = 0
calcular = verdadero

si calcular # Esto es un comentario
    a = PI * a # Se va a eliminar
sino a == 3
    a = E
"""

codigo_preprocesado = preprocesar_codigo(programa)
print(codigo_preprocesado)
