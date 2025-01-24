import ply.lex as lex
import re

# Lista de tokens
tokens = (
    "CONST",
    "ID",
    "NUMBER",
    "COMMENT",
    "NEWLINE",
    "EQUALS",
    "OPERATOR",
    "WHITESPACE",
)

# Definición de tokens
t_CONST = r"const"
t_ID = r"[a-zA-Z_][a-zA-Z_0-9]*"
t_NUMBER = r"\d+(\.\d+)?"
t_EQUALS = r"="
t_OPERATOR = r"[\+\-\*/]"
t_WHITESPACE = r"[ \t]+"
t_ignore = ""

# Diccionario para almacenar constantes
constantes = {}


# Definición de comentarios
def t_COMMENT(t):
    r"\#.*"
    pass  # Ignorar comentarios


# Definición de nuevas líneas
def t_NEWLINE(t):
    r"\n+"
    t.lexer.lineno += len(t.value)
    return t


# Definición de errores
def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)


# Definición de reglas léxicas para constantes
def t_CONST_DEF(t):
    r"const\s+([a-zA-Z_][a-zA-Z_0-9]*)\s*=\s*(\d+(\.\d+)?)"
    constantes[t.lexer.lexmatch.group(1)] = t.lexer.lexmatch.group(2)
    pass  # Ignorar la definición de constantes


# Construir el lexer
lexer = lex.lex()


# Función para reemplazar constantes en el código fuente
def reemplazar_constantes(codigoFuente):
    resultado = []
    lexer.input(codigoFuente)
    print(constantes)
    while True:
        tok = lexer.token()
        if not tok:
            break
        if tok.type == "ID" and tok.value in constantes:
            resultado.append(constantes[tok.value])
        elif tok.type == "WHITESPACE":
            resultado.append(tok.value)
        elif tok.type == "NEWLINE":
            resultado.append("\n")
        else:
            resultado.append(tok.value)
    return "".join(resultado)


# Código de prueba
programa = """
const PI = 3.141592654
const E = 2.718281828
a = 0
calcular = verdadero

si calcular # Esto es un comentario
    a = PI * a # Se va a eliminar
sino a == 3
    a = E
"""

codigoPrueba = reemplazar_constantes(programa)

# Eliminar lineas en blanco
codigoPrueba = re.sub(r"\n\s*\n", "\n", codigoPrueba)
# Eliminar comentarios
codigoPrueba = re.sub(r"#.*", "", codigoPrueba)
# Eliminar espacios en blanco al final de la linea
codigoPrueba = re.sub(r"[ \t]+$", "", codigoPrueba, flags=re.MULTILINE)

print(codigoPrueba)
