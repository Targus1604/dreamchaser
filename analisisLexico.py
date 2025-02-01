import ply.lex as lex
from utils.programas import programaPrueba  # Importa string de un programa prueba

# ------------------------------------------------------------
# Definición de tokens
# ------------------------------------------------------------

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
    # Palabras reservadas
    *palabrasReservadas.values(),
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
# Definiciones regulares y extensiones regulares
# ------------------------------------------------------------

# Numeros
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
# Reglas para reconocer tokens
# ------------------------------------------------------------

# Tokens a ignorar
t_ignore = "\t"  # Ignorar tabulaciones
t_ignore_COMENTARIO = r"\#.*"


# Regla para importar librerías
def t_IMPORTAR(t):
    r"importar\s+\'.*?\'"
    return t


# Reglas de expresiones regulares para tokens simples
t_SUMA = r"\+"
t_RESTA = r"-"
t_MULTIPLICACION = r"\*"
t_DIVISION = r"/"
t_ASIGNACION = r"="
t_STRING = r"\'.*?\'"


# Regla para identificadores y palabras reservadas
@lex.TOKEN(identificador)
def t_ID(t):
    t.type = palabrasReservadas.get(
        t.value, "ID"
    )  # Verificar si es una palabra reservada
    return t


@lex.TOKEN(numero_flotante_opcional)
def t_NUMERO(t):
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


t_ESPACIO = r"\s"


# Regla para manejar errores
def t_error(t):
    print(f"Caracter no reconocido '{t.value[0]}'")
    t.lexer.skip(1)


# ------------------------------------------------------------
# Construcción y ejecución del lexer
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
