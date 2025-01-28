import re
from analisisLexico import lexer
from utils.programas import programaPrueba


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
            resultado.append(
                f"!importando: {tok.value.split('"')[1]}",
            )
        elif tok.type == "COMENTARIO":
            continue  # Ignorar comentarios
        elif tok.type == "INDENTACION":
            resultado.append("  ")
        else:
            resultado.append(tok.value)

    print("resultado", resultado)
    codigo_preprocesado = "".join(resultado)
    # Reemplazar múltiples saltos de línea consecutivos con un solo salto de línea
    codigo_preprocesado = re.sub(r"\n\s*\n", "\n", codigo_preprocesado)

    return codigo_preprocesado


codigo_preprocesado = preprocesar_codigo(programaPrueba)
print(codigo_preprocesado)
