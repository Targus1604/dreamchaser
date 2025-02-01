import re
from analisisLexico import lexer
from utils.programas import programaPrueba


# Función para preprocesar el código fuente
def preprocesar_codigo(codigoFuente):
    resultado = []
    lexer.input(codigoFuente)
    while True:
        token = lexer.token()
        if not token:
            break
        if token.type == "IMPORTAR":
            # Leer el contenido del archivo importado
            resultado.append(
                f"!importando: {token.value.split("'")[1]}",
            )
        else:
            resultado.append(token.value)

    codigo_preprocesado = "".join(resultado)
    # Reemplazar múltiples saltos de línea consecutivos con un solo salto de línea
    codigo_preprocesado = re.sub(r"\n\s*\n", "\n", codigo_preprocesado)

    return codigo_preprocesado


codigo_preprocesado = preprocesar_codigo(programaPrueba)
print(codigo_preprocesado)
