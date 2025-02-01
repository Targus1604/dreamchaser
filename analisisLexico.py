import src.ply.lex as lex
from utils.programas import programaPrueba  # Importa string de un programa prueba

# ------------------------------------------------------------
# DEFINICIONES REGULARES Y EXTENSIONES REGULARES
# ------------------------------------------------------------

# Números
digito = r"[0-9]"
digito_parte_flotante = r"\." + digito + r"+"
digito_parte_exponente = r"[eE][+-]?" + digito + r"+"

# Letras
letra = r"[a-zA-Z_]"

# Extensiones compuestas
identificador = letra + r"(" + letra + r"|" + digito + r")*"

numero_flotante_opcional = (
    digito
    + r"("
    + digito_parte_flotante
    + r")?"
    + r"("
    + digito_parte_exponente
    + r")?"
)


# ------------------------------------------------------------
# DEFINICIÓN DE TOKENS
# ------------------------------------------------------------

# Palabras reservadas
palabrasReservadas = {
    # Estructuras de control
    "si": "SI",
    "sino": "SINO",
    "mientras": "MIENTRAS",
    "funcion": "FUNCION",
    "para": "PARA",
    # Valores de verdad
    "verdadero": "VERDADERO",
    "falso": "FALSO",
    # Operadores lógicos
    "y": "Y",
    "o": "O",
    "no": "NO",
    # Otros
    "const": "CONST",
    "retornar": "RETORNAR",
    "importar": "IMPORTAR",
}

# Lista de nombres de tokens
tokens = (
    # Palabras reservadas
    *palabrasReservadas.values(),
    # Operadores relacionales
    "IGUALDAD",
    "DIFERENTE",
    "MAYOR",
    "MENOR",
    "MAYOR_IGUAL",
    "MENOR_IGUAL",
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
    "ESPACIO",
)

# ------------------------------------------------------------
# REGLAS PARA RECONOCER TOKENS
# ------------------------------------------------------------


# Palabras reservadas
# Regla para importar librerías
def t_IMPORTAR(t):
    r"importar\s+\'.*?\'"
    return t


# Operadores relacionales
t_IGUALDAD = r"=="
t_DIFERENTE = r"!="
t_MAYOR = r">"
t_MENOR = r"<"
t_MAYOR_IGUAL = r">="
t_MENOR_IGUAL = r"<="

# Operadores aritméticos
t_SUMA = r"\+"
t_RESTA = r"-"
t_MULTIPLICACION = r"\*"
t_DIVISION = r"/"
t_DIVISION_ENTERA = r"//"

# Asignación
t_ASIGNACION = r"="

# Delimitadores
t_PARENTESIS_IZQUIERDO = r"\("
t_PARENTESIS_DERECHO = r"\)"

# Literales e identificadores


# Regla para números con flotante y notacion científica opcionales
@lex.TOKEN(numero_flotante_opcional)
def t_NUMERO(t):
    return t


t_STRING = r"\'.*?\'"
t_BOOLEANO = r"verdadero|falso"


# Regla para identificadores y palabras reservadas
@lex.TOKEN(identificador)
def t_ID(t):
    t.type = palabrasReservadas.get(
        t.value, "ID"
    )  # Verificar si es una palabra reservada
    return t


# Comentarios
t_ignore_COMENTARIO = r"\#.*"

# Espacios y tabulaciones
t_ignore = "\t"  # Ignorar tabulaciones


# Regla para indentación (4 espacios en blanco)
def t_INDENTACION(t):
    r"[ ]{4}"
    return t


# Regla para nuevas líneas
def t_NUEVA_LINEA(t):
    r"\n+"
    t.lexer.lineno += len(t.value)
    return t


t_ESPACIO = r"\s"


# Regla para manejar errores
def t_error(t):
    print(f"Caracter no reconocido '{t.value[0]}'")
    t.lexer.skip(1)


# ------------------------------------------------------------
# CONSTRUCCIÓN Y EJECUCIÓN DEL LEXER
# ------------------------------------------------------------

# Construir el lexer
lexer = lex.lex()
lexer.input(programaPrueba)

print("Análisis léxico del programa de prueba:")
print("=======================================")
print(programaPrueba)
print("=======================================\n")

# Separar tokens
while True:
    token = lexer.token()
    if not token:
        break
    print(token)
