import re
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
        elif tok.type == "COMMENT" or tok.type == "NEWLINE":
            continue  # Ignorar comentarios y nuevas líneas
        elif (
            tok.type == "ID"
            or tok.type == "NUMBER"
            or tok.type == "PLUS"
            or tok.type == "MINUS"
            or tok.type == "TIMES"
            or tok.type == "DIVIDE"
            or tok.type == "EQUALS"
            or tok.type == "STRING"
        ):
            resultado.append(tok.value)
        elif tok.type == "WHITESPACE":
            resultado.append(tok.value)

    # print("resultado", resultado)
    codigo_preprocesado = "".join(str(resultado))

    # Eliminar líneas en blanco
    codigo_preprocesado = re.sub(r"\n\s*\n", "\n", codigo_preprocesado)
    # Eliminar espacios en blanco al final de la línea
    codigo_preprocesado = re.sub(
        r"[ \t]+$", "", codigo_preprocesado, flags=re.MULTILINE
    )

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
