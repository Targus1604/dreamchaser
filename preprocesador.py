import re

constantes = {}


def reemplazarConstantes(match):
    constante = match.group(0)
    return constantes.get(constante)


def preprocesarCodigo(codigoFuente):
    # Reeemplazar las constantes definidas y elimina la linea donde se definieron

    # Itera sobre las lineas donde se definen las constantes y guarda su nombre y valor
    for match in re.finditer(r"const (\w+) = ([^\n]+)", codigoFuente):
        nombreConstante = match.group(1)
        valorConstante = match.group(2)
        constantes[nombreConstante] = valorConstante

    # Eliminar la línea donde se define el const
    codigoFuente = re.sub(r"const \w+ = [^\n]+\n", "", codigoFuente)
    pattern = rf"\b({'|'.join(re.escape(key) for key in constantes.keys())})\b"
    # pattern = \b(PI|E)\b <- output de ejemplo

    # Reemplazar las constantes por su valor
    codigoFuente = re.sub(pattern, reemplazarConstantes, codigoFuente)

    # Eliminar cualquier línea en blanco inicial
    codigoFuente = codigoFuente.lstrip()
    # Eliminar lineas en blanco en general
    codigoFuente = re.sub(r"\n+", "\n", codigoFuente)
    # Eliminar comentarios
    codigoFuente = re.sub(r"#.*", "", codigoFuente)
    # Eliminar espacios en blanco al final de la linea
    codigoFuente = re.sub(r"[ \t]+$", "", codigoFuente, flags=re.MULTILINE)

    return codigoFuente


# Código de prueba
programa = """
import ./libreria.txt
const PI = 3.141592654

const E = 2.718281828
a = 0
calcular = verdadero

si calcular # Esto es un comentario
    a = PI * a # Se va a eliminar
sino a == 3
    a = E
"""

codigoPrueba = preprocesarCodigo(programa)
print(codigoPrueba)
