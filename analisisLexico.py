import ply.lex as lex
from utils.programas import programaPrueba  # Importa string de un programa prueba

# Palabras reservadas
palabrasReservadas = {
    "si": "SI",
    "sino": "SINO",
    "verdadero": "VERDADERO",
    "falso": "FALSO",
    "const": "CONST",
    "mientras": "MIENTRAS",
    "hacer": "HACER",
    "para": "PARA",
    "funcion": "FUNCION",
    "retornar": "RETORNAR",
    "importar": "IMPORTAR",
}

# Lista de nombres de tokens
tokens = (
    # Operadores lógicos
    "Y",
    "O",
    "NO",
    # Operadores relacionales
    "IGUALDAD",
    "DIFERENTE",
    "MAYOR",
    "MENOR",
    "MAYOR_IGUAL",
    "MENOR_IGUAL",
    "IMPORTAR",
    # Operadores aritméticos
    "SUMA",
    "RESTA",
    "MULTIPLICACION",
    "DIVISION",
    "DIVISION_ENTERA",
    # Operador de asignación
    "ASIGNACION",
    # Delimitadores
    "PARENTESIS_IZQUIERDO",
    "PARENTESIS_DERECHO",
    # Literales e identificadores
    "NUMERO",
    "STRING",
    "BOOLEANO",
    "ID",
    # Comentarios
    "COMENTARIO",
    # Espacios y tabulaciones
    "NUEVA_LINEA",
    "INDENTACION",
    +list(palabrasReservadas.values()),
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
    r"[ ]{4}"
    return t


# Regla para nuevas líneas
def t_NUEVA_LINEA(t):
    r"\n+"
    t.lexer.lineno += len(t.value)
    return t


# # Regla para espacios y tabulaciones (pero no saltos de línea)
def t_ESPACIO(t):
    r"\s"
    pass  # Ignorar espacios y tabulaciones


# Regla para comentarios
def t_COMENTARIO(t):
    r"\#.*"
    pass  # Ignorar comentarios


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


lexer.input(programaPrueba)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)
