import ply.yacc as yacc
from ply_lexer import tokens

# Tabla de símbolos para almacenar variables y constantes
symbol_table = {}

# Precedencia para operadores
precedence = (
    ('right', 'POTENCIA'),  # <-- Agregamos la precedencia para potencia
    ('left', 'MULTIPLICACION', 'DIVISION', 'DIVISION_ENTERA'),
    ('left', 'SUMA', 'RESTA'),
)

# Reglas de producción
def p_programa(p):
    '''programa : importaciones constantes variables instrucciones'''
    print("Programa reconocido correctamente.")

def p_importaciones(p):
    '''importaciones : importaciones IMPORTAR CADENA
                     | empty'''
    if len(p) == 4:
        print(f"Importación: {p[3]}")

def p_constantes(p):
    '''constantes : constantes CONST IDENTIFICADOR valor
                  | empty'''
    if len(p) == 5:
        symbol_table[p[3]] = p[4]  # Guardar en la tabla de símbolos
        print(f"Constante definida: {p[3]} = {p[4]}")
    else:
        p[0] = None

def p_variables(p):
    '''variables : variables IDENTIFICADOR ASIGNACION expresion
                 | empty'''
    if len(p) == 5:
        symbol_table[p[2]] = p[4]  # Guardar en la tabla de símbolos
        print(f"Variable definida: {p[2]} = {p[4]}")
    else:
        p[0] = None

def p_valor(p):
    '''valor : NUMERO
             | VERDADERO
             | FALSO
             | CADENA
             | IDENTIFICADOR'''
    if isinstance(p[1], str) and p[1] in symbol_table:  # Si es un identificador y está en la tabla
        p[0] = symbol_table[p[1]]
    else:
        p[0] = p[1]  # Si es un número o cadena, devolverlo tal cual
    print(f"Valor reconocido: {p[0]}")

def p_instrucciones(p):
    '''instrucciones : instrucciones operacion
                     | instrucciones control
                     | instrucciones funcion
                     | instrucciones COMENTARIO
                     | empty'''
    pass

def p_operacion(p):
    '''operacion : expresion'''
    print(f"Resultado de la operación: {p[1]}")  # Mostrar el resultado final

variables = {}

def get_value(value):
    """ Convierte strings numéricos a float o busca valores en variables. """
    if isinstance(value, str):
        if value.replace('.', '', 1).isdigit():  # Si es número, convertirlo a float
            return float(value)
        elif value in variables:  # Si es una variable, obtener su valor
            return variables[value]
    return value  # Si no es número ni variable, devolverlo tal cual

variables = {}  # Diccionario para almacenar variables

def get_value(value):
    """ Convierte strings numéricos a float o busca valores en variables. """
    if isinstance(value, (int, float)):  # Si ya es un número, devolverlo directamente
        return value
    elif isinstance(value, str):
        if value.replace('.', '', 1).isdigit():  # Convertir a float si es un número válido
            return float(value)
        elif value in variables:  # Si es una variable definida, obtener su valor
            return variables[value]
        else:
            return None  # Si no está definida, devolver None
    return value


def p_expresion(p):
    '''expresion : termino
                 | expresion SUMA termino
                 | expresion RESTA termino
                 | expresion MULTIPLICACION termino
                 | expresion DIVISION termino
                 | expresion DIVISION_ENTERA termino
                 | expresion POTENCIA termino
                 | expresion IGUALDAD expresion
                 | expresion DIFERENTE expresion
                 | expresion MAYOR expresion
                 | expresion MENOR expresion
                 | expresion MAYOR_IGUAL expresion
                 | expresion MENOR_IGUAL expresion'''

    if len(p) == 2:
        p[0] = get_value(p[1])  # Obtener el valor de la variable si es necesario
    else:
        p1 = get_value(p[1])
        p3 = get_value(p[3])

        # 🚨 Evitar errores con números
        if p1 is None or p3 is None:
            if p1 is None and isinstance(p[1], str):
                print(f"Error: Variable no definida -> {p[1]}")
            if p3 is None and isinstance(p[3], str):
                print(f"Error: Variable no definida -> {p[3]}")
            p[0] = None
            return

        # Solo operar si ambos son números
        if isinstance(p1, (int, float)) and isinstance(p3, (int, float)):
            if p[2] == '+':
                p[0] = p1 + p3
            elif p[2] == '-':
                p[0] = p1 - p3
            elif p[2] == '*':
                p[0] = p1 * p3
            elif p[2] == '/':
                p[0] = p1 / p3
            elif p[2] == '//':
                p[0] = p1 // p3
            elif p[2] == '^':
                p[0] = p1 ** p3
            elif p[2] == '==':
                p[0] = p1 == p3
            elif p[2] == '!=':
                p[0] = p1 != p3
            elif p[2] == '>':
                p[0] = p1 > p3
            elif p[2] == '<':
                p[0] = p1 < p3
            elif p[2] == '>=':
                p[0] = p1 >= p3
            elif p[2] == '<=':
                p[0] = p1 <= p3
        else:
            print(f"Error: No se puede operar con {p1} y {p3}")
            p[0] = None





def p_termino(p):
    '''termino : valor
               | PARENTESIS_IZQUIERDO expresion PARENTESIS_DERECHO'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_control(p):
    '''control : SI expresion bloque
               | SI expresion bloque SINO bloque
               | MIENTRAS expresion bloque'''
    
    if p[1] == 'si':  # Condición si
        if p[2]:  # Evaluamos la expresión booleana
            ejecutar_bloque(p[3])
        elif len(p) == 6:  # Si hay sino
            ejecutar_bloque(p[5])

    elif p[1] == 'mientras':  # Condición mientras
        while p[2]:  # Mientras la expresión sea verdadera
            ejecutar_bloque(p[3])  # Ejecutar el bloque
            p[2] = evaluar_expresion(p[2])  # Reevaluar la condición

def p_bloque(p):
    '''bloque : LLAVE_IZQUIERDA instrucciones LLAVE_DERECHA'''
    pass


def p_funcion(p):
    '''funcion : FUNCION IDENTIFICADOR PARENTESIS_IZQUIERDO parametros PARENTESIS_DERECHO bloque'''
    pass

def p_parametros(p):
    '''parametros : empty
                  | IDENTIFICADOR
                  | parametros COMA IDENTIFICADOR'''
    pass

def p_expresion_booleana(p):
    '''expresion_booleana : expresion IGUALDAD expresion
                          | expresion DIFERENTE expresion
                          | expresion MAYOR expresion
                          | expresion MENOR expresion
                          | expresion MAYOR_IGUAL expresion
                          | expresion MENOR_IGUAL expresion
                          | expresion_booleana AND expresion_booleana
                          | expresion_booleana OR expresion_booleana
                          | NOT expresion_booleana
                          | VERDADERO
                          | FALSO'''
    if len(p) == 4:
        if p[2] == '==': p[0] = p[1] == p[3]
        elif p[2] == '!=': p[0] = p[1] != p[3]
        elif p[2] == '>': p[0] = p[1] > p[3]
        elif p[2] == '<': p[0] = p[1] < p[3]
        elif p[2] == '>=': p[0] = p[1] >= p[3]
        elif p[2] == '<=': p[0] = p[1] <= p[3]
        elif p[2] == 'and': p[0] = p[1] and p[3]
        elif p[2] == 'or': p[0] = p[1] or p[3]
    elif len(p) == 3:  # NOT expresion_booleana
        p[0] = not p[2]
    else:
        p[0] = p[1]


def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Error de sintaxis en: {p.value}")
    else:
        print("Error de sintaxis: Fin de entrada inesperado")

# Construir el analizador
parser = yacc.yacc()

# Prueba del analizador
data = """
const PI 3
const E 2.718281828
const MATERIA LENGUAJESDEPROGRAMACION


a = 10
b = 20.5
c = 1e-3
d = verdadero
e = falso

# Operadores relacionales
igual = a == b
diferente = a != b
mayor = a > b
menor = a < b
mayorIgual = a >= b
menorIgual = a <= b



suma = a + b
resta = a - b
multiplicacion = a * b
division = a / b
divisionEntera = a // b
potencia = b ^ a

2^3

#ESTE ES UN COMENTARIO


si a > b
    retornar a
sino
    retornar b

    
funcion calcularArea(radio)
    retornar PI * radio

# Llamada a la función
area = calcularArea(5)
materia2 = MATERIA

# Comentario de prueba
# Este es un comentario que debe ser ignorado por el lexer

"""

parser.parse(data)