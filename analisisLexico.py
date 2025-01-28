import ply.lex as lex

# Lista de nombres de tokens
tokens = (
    "NUMBER",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "ID",
    "EQUALS",
    "NEWLINE",
    "COMMENT",
    "IMPORT",
    "STRING",
)

# Reglas de expresiones regulares para tokens simples
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_EQUALS = r"="
t_STRING = r"\".*?\""


# Regla para identificadores
def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    return t


# Regla para números
def t_NUMBER(t):
    r"(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?"
    return t


# Regla para comentarios
def t_COMMENT(t):
    r"\#.*"
    pass  # Ignorar comentarios


# Regla para nuevas líneas
def t_NEWLINE(t):
    r"\n+"
    t.lexer.lineno += len(t.value)
    return t


# Regla para importaciones
def t_IMPORT(t):
    r"import\s+\".*?\" "
    t.value = t.value.split('"')[1]  # Extraer el nombre del archivo
    return t


# Regla para ignorar espacios y tabulaciones
t_ignore = " \t"


# Regla para manejar errores
def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)


# Construir el lexer
lexer = lex.lex()
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
lexer.input(programa)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)
