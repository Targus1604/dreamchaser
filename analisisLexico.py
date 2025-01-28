import ply.lex as lex

# Lista de nombres de tokens
tokens = (
    "NUMERO",
    "MAS",
    "MENOS",
    "MULTIPLICACION",
    "DIVISION",
    "ID",
    "IGUAL",
    "NUEVA_LINEA",
    "COMENTARIO",
    "IMPORT",
    "STRING",
    "INDENTACION",
)

# Reglas de expresiones regulares para tokens simples
t_ID = r"[a-zA-Z_][a-zA-Z_0-9]*"
t_MAS = r"\+"
t_MENOS = r"-"
t_MULTIPLICACION = r"\*"
t_DIVISION = r"/"
t_IGUAL = r"="
t_STRING = r"\".*?\""


# Regla para números
def t_NUMERO(t):
    r"(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?"
    return t


# Regla para indentación (4 espacios en blanco)
def t_INDENTACION(t):
    r"[ \t]{4}"
    return t


# # Regla para espacios y tabulaciones (pero no saltos de línea)
def t_ESPACIO(t):
    r"\s"
    pass  # Ignorar espacios y tabulaciones


# Regla para comentarios
def t_COMENTARIO(t):
    r"\#.*"
    pass  # Ignorar comentarios


# Regla para nuevas líneas
def t_NUEVA_LINEA(t):
    r"\n+"
    t.lexer.lineno += len(t.value)
    return t


# Regla para importaciones
def t_IMPORT(t):
    r"import\s+\".*?\" "
    return t


# Regla para manejar errores
def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)


t_ignore = "\t"

# Construir el lexer
lexer = lex.lex()
# programa = """

# const PI = 3.141592654
# """
programa = """
si calcular # Esto es un comentario
    a = PI * a # Se va a eliminar
sino a == 3
    a = E
"""
lexer.input(programa)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)
