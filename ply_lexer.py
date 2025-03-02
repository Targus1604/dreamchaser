import ply.lex as lex

# Lista de tokens
tokens = (
    'IMPORTAR', 'CONST', 'VERDADERO', 'FALSO', 'SI', 'SINO', 'MIENTRAS', 'FUNCION', 'RETORNAR',
    'SUMA', 'RESTA', 'MULTIPLICACION', 'DIVISION', 'DIVISION_ENTERA', 'POTENCIA',
    'IGUALDAD', 'DIFERENTE', 'MAYOR', 'MENOR', 'MAYOR_IGUAL', 'MENOR_IGUAL', 'ASIGNACION',
    'AND', 'OR', 'NOT',
    'PARENTESIS_IZQUIERDO', 'PARENTESIS_DERECHO', 'LLAVE_IZQUIERDA', 'LLAVE_DERECHA', 'COMA', 'PUNTO_Y_COMA',
    'COMENTARIO', 'NUMERO', 'IDENTIFICADOR', 'CADENA',
    'LEER', 'ESCRIBIR'
)

# Palabras clave
reservadas = {
    'import': 'IMPORTAR',
    'const': 'CONST',
    'true': 'VERDADERO',
    'false': 'FALSO',
    'if': 'SI',
    'else': 'SINO',
    'while': 'MIENTRAS',
    'function': 'FUNCION',
    'return': 'RETORNAR',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
    'leer': 'LEER',
    'escribir': 'ESCRIBIR'
}

# Definir tokens para caracteres especiales
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_DIVISION_ENTERA = r'//'
t_POTENCIA = r'\^'
t_IGUALDAD = r'=='
t_DIFERENTE = r'!='
t_MAYOR = r'>'
t_MENOR = r'<'
t_MAYOR_IGUAL = r'>='
t_MENOR_IGUAL = r'<='
t_ASIGNACION = r'='
t_PARENTESIS_IZQUIERDO = r'\('
t_PARENTESIS_DERECHO = r'\)'
t_LLAVE_IZQUIERDA = r'\{'
t_LLAVE_DERECHA = r'\}'
t_COMA = r','
t_PUNTO_Y_COMA = r';'
t_COMENTARIO = r'\#.*'

t_ignore = ' \t\n'

def t_NUMERO(t):
    r'\d+(\.\d+)?([eE][+-]?\d+)?'
    t.value = float(t.value)  # Convertir a número
    return t

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservadas.get(t.value, 'IDENTIFICADOR')  # Si es palabra clave, cambiar tipo
    return t

def t_CADENA(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]  # Eliminar las comillas
    return t

# Manejo de comentarios
def t_ignore_COMENTARIO(t):
    r'\#.*'
    pass  # Ignorar completamente los comentarios

def t_error(t):
    print(f"Carácter ilegal: {t.value[0]}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

lexer.input("{ }")

for tok in lexer:
    print(tok)