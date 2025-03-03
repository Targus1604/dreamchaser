import src.ply.yacc as yacc
from analisisLexico import constantes, lexer, tokens

# Diccionario de nombres (variables y constantes)
nombres = {}
# Diccionario de funciones
funciones = {}


class Nodo:
    def __init__(self, tipo, hijos=None, valor=None):
        self.tipo = tipo
        self.hijos = hijos if hijos else []
        self.valor = valor

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self.valor is not None:
            return f"{self.tipo}({self.valor})"
        else:
            return f"{self.tipo}({', '.join(map(str, self.hijos))})"

    def imprimir(self, nivel=0):
        """Imprime el AST con formato indentado para mejor legibilidad"""
        indentacion = "  " * nivel
        if self.valor is not None:
            print(f"{indentacion}{self.tipo}: {self.valor}")
        else:
            print(f"{indentacion}{self.tipo}")
            for hijo in self.hijos:
                hijo.imprimir(nivel + 1)


# Precedencia para operadores
precedence = (
    ("left", "IGUALDAD", "DIFERENTE", "MAYOR", "MENOR", "MAYOR_IGUAL", "MENOR_IGUAL"),
    ("left", "SUMA", "RESTA"),
    ("left", "MULTIPLICACION", "DIVISION", "DIVISION_ENTERA"),
    ("right", "NO"),  # Para el operador 'no'
)


# Ignorar completamente los espacios y nuevas líneas vacías
def p_programa(p):
    """programa : declaraciones"""
    p[0] = Nodo("programa", [p[1]])


def p_declaraciones(p):
    """declaraciones : declaraciones NUEVA_LINEA declaracion
    | declaraciones NUEVA_LINEA
    | declaracion"""
    if len(p) == 4:  # declaraciones NUEVA_LINEA declaracion
        # Solo añadimos la declaración si no es None
        if p[3] is not None:
            p[0] = Nodo("declaraciones", p[1].hijos + [p[3]])
        else:
            p[0] = p[1]
    elif len(p) == 3:  # declaraciones NUEVA_LINEA
        p[0] = p[1]
    else:  # declaracion
        p[0] = Nodo("declaraciones", [p[1]])


def p_declaracion(p):
    """declaracion : declaracion_constante
    | declaracion_asignacion
    | declaracion_importar
    | declaracion_funcion
    | declaracion_if
    | expresion"""
    p[0] = p[1]


def p_declaracion_importar(p):
    """declaracion_importar : IMPORTAR"""
    # Extraer el nombre del archivo de la cadena importar 'archivo'
    archivo = p[1].split("'")[1]
    p[0] = Nodo("importar", valor=archivo)


def p_declaracion_constante(p):
    """declaracion_constante : CONST"""
    # Extrae el nombre y valor de la constante
    parts = p[1].split(maxsplit=2)
    _, id_name, valor = parts

    # Determinar si es número o string
    if valor.startswith("'") and valor.endswith("'"):
        valor_node = Nodo("STRING", valor=valor)
    else:
        try:
            # Convertir a float para manejar decimales
            float(valor)
            valor_node = Nodo("NUMERO", valor=valor)
        except ValueError:
            print(f"Error: valor inválido para constante '{valor}'")
            valor_node = Nodo("error", valor=valor)

    p[0] = Nodo("constante", [Nodo("ID", valor=id_name), valor_node])
    constantes[id_name] = valor


def p_declaracion_asignacion(p):
    """declaracion_asignacion : ID ASIGNACION expresion
    | ID ESPACIO ASIGNACION ESPACIO expresion"""
    if len(p) == 4:
        id_name, expr = p[1], p[3]
    else:
        id_name, expr = p[1], p[5]

    nombres[id_name] = expr
    p[0] = Nodo("asignacion", [Nodo("ID", valor=id_name), expr])


def p_declaracion_if(p):
    """declaracion_if : SI ESPACIO expresion
    | SI expresion"""
    if len(p) == 4:
        condicion = p[3]
    else:
        condicion = p[2]

    p[0] = Nodo(
        "si", [condicion, Nodo("bloque", [])]
    )  # Bloque vacío, se completaría más tarde


def p_declaracion_if_else(p):
    """declaracion_if : SI ESPACIO expresion NUEVA_LINEA INDENTACION declaracion NUEVA_LINEA SINO ESPACIO expresion
    | SI expresion NUEVA_LINEA INDENTACION declaracion NUEVA_LINEA SINO expresion"""
    if len(p) == 11:
        condicion_if, bloque_if, condicion_else = p[3], p[6], p[10]
    else:
        condicion_if, bloque_if, condicion_else = p[2], p[5], p[8]

    p[0] = Nodo(
        "si_sino",
        [
            Nodo("condicion_if", [condicion_if]),
            Nodo("bloque_if", [bloque_if]),
            Nodo("condicion_else", [condicion_else]),
            Nodo("bloque_else", []),  # Bloque vacío, se completaría más tarde
        ],
    )


def p_declaracion_funcion(p):
    """declaracion_funcion : FUNCION ID PARENTESIS_IZQUIERDO parametros PARENTESIS_DERECHO NUEVA_LINEA INDENTACION declaracion_retorno"""
    id_name = p[2]
    parametros = p[4]
    cuerpo = p[8]

    funciones[id_name] = {
        "parametros": parametros.hijos if hasattr(parametros, "hijos") else [],
        "cuerpo": cuerpo,
    }

    p[0] = Nodo("funcion", [Nodo("ID", valor=id_name), parametros, cuerpo])


def p_parametros(p):
    """parametros : parametros COMA ESPACIO ID
    | parametros COMA ID
    | ID
    |"""
    if len(p) == 1:  # Regla vacía
        p[0] = Nodo("parametros", [])
    elif len(p) == 2:  # Un solo parámetro
        p[0] = Nodo("parametros", [Nodo("ID", valor=p[1])])
    elif len(p) == 4:  # parametros COMA ID
        # Agregamos el nuevo parámetro a los existentes
        p[0] = Nodo("parametros", p[1].hijos + [Nodo("ID", valor=p[3])])
    else:  # len(p) == 5, parametros COMA ESPACIO ID
        p[0] = Nodo("parametros", p[1].hijos + [Nodo("ID", valor=p[4])])


def p_declaracion_retorno(p):
    """declaracion_retorno : RETORNAR expresion"""
    p[0] = Nodo("retornar", [p[2]])


def p_expresion_binaria(p):
    """expresion : expresion SUMA expresion
    | expresion RESTA expresion
    | expresion MULTIPLICACION expresion
    | expresion DIVISION expresion
    | expresion DIVISION_ENTERA expresion
    | expresion IGUALDAD expresion
    | expresion DIFERENTE expresion
    | expresion MAYOR expresion
    | expresion MENOR expresion
    | expresion MAYOR_IGUAL expresion
    | expresion MENOR_IGUAL expresion
    | expresion ESPACIO SUMA ESPACIO expresion
    | expresion ESPACIO RESTA ESPACIO expresion
    | expresion ESPACIO MULTIPLICACION ESPACIO expresion
    | expresion ESPACIO DIVISION ESPACIO expresion
    | expresion ESPACIO DIVISION_ENTERA ESPACIO expresion
    | expresion ESPACIO IGUALDAD ESPACIO expresion
    | expresion ESPACIO DIFERENTE ESPACIO expresion
    | expresion ESPACIO MAYOR ESPACIO expresion
    | expresion ESPACIO MENOR ESPACIO expresion
    | expresion ESPACIO MAYOR_IGUAL ESPACIO expresion
    | expresion ESPACIO MENOR_IGUAL ESPACIO expresion"""
    if len(p) == 4:
        operador = p[2]
        izq, der = p[1], p[3]
    else:
        operador = p[3]
        izq, der = p[1], p[5]

    p[0] = Nodo("binaria", [izq, Nodo("operador", valor=operador), der])


def p_expresion_bool(p):
    """expresion : VERDADERO
    | FALSO"""
    p[0] = Nodo("BOOLEANO", valor=p[1])


def p_expresion_parentesis(p):
    """expresion : PARENTESIS_IZQUIERDO expresion PARENTESIS_DERECHO"""
    p[0] = p[2]


def p_expresion_numero(p):
    """expresion : NUMERO"""
    p[0] = Nodo("NUMERO", valor=p[1])


def p_expresion_string(p):
    """expresion : STRING"""
    p[0] = Nodo("STRING", valor=p[1])


def p_expresion_id(p):
    """expresion : ID"""
    if p[1] in constantes:
        # Crear un nodo numérico con el valor de la constante
        if constantes[p[1]].isdigit() or (
            constantes[p[1]][0] == "-" and constantes[p[1]][1:].isdigit()
        ):
            # Es una constante numérica
            p[0] = Nodo("NUMERO", valor=constantes[p[1]])
        elif constantes[p[1]].startswith("'") and constantes[p[1]].endswith("'"):
            # Es una constante de tipo string
            p[0] = Nodo("STRING", valor=constantes[p[1]])
        else:
            # Otro tipo de constante
            p[0] = Nodo("constante_ref", valor=p[1])
    elif p[1] in nombres:
        p[0] = Nodo("variable_ref", valor=p[1])
    else:
        print(f"Error: identificador '{p[1]}' no definido")
        p[0] = Nodo("error", valor=p[1])


def p_expresion_llamada_funcion(p):
    """expresion : ID PARENTESIS_IZQUIERDO argumentos PARENTESIS_DERECHO"""
    id_name = p[1]
    argumentos = p[3]

    if id_name not in funciones:
        print(f"Error: función '{id_name}' no definida")
        p[0] = Nodo("error", valor=id_name)
    else:
        p[0] = Nodo("llamada_funcion", [Nodo("ID", valor=id_name), argumentos])


def p_argumentos(p):
    """argumentos : argumentos COMA expresion
    | expresion
    |"""
    if len(p) == 1:  # Regla vacía
        p[0] = Nodo("argumentos", [])
    elif len(p) == 2:  # Un solo argumento
        p[0] = Nodo("argumentos", [p[1]])
    else:  # len(p) == 4, argumentos COMA expresion
        p[0] = Nodo("argumentos", p[1].hijos + [p[3]])


def p_error(p):
    if p:
        print(
            f"Error de sintaxis en '{p.value}', línea {p.lineno}, posición {p.lexpos}"
        )
    else:
        print("Error de sintaxis en EOF")


# Construir el parser
parser = yacc.yacc(debug=False)


# Función para analizar un programa
def analizar(programa):
    # Reiniciar los diccionarios para evitar conflictos entre ejecuciones
    nombres.clear()
    funciones.clear()
    constantes.clear()  # Añade esta línea para limpiar las constantes

    # Analizar el programa
    lexer.lineno = 1  # Reiniciar el contador de líneas
    ast = parser.parse(programa, lexer=lexer)
    return ast


# Programa de prueba para constantes
def probar_constantes():
    programa_simple = """const NOTA 4
a = 10
b = NOTA + 1
"""

    print("\n--- PRUEBA DE CONSTANTES ---")
    # Mostrar los tokens para depuración
    print("Tokens generados:")
    lexer.input(programa_simple)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(f"Token: {tok.type}, Valor: '{tok.value}', Línea: {tok.lineno}")

    # Reiniciar el lexer
    lexer.input(programa_simple)

    # Analizar el programa
    ast = analizar(programa_simple)
    print("\nÁrbol de sintaxis abstracta (AST):")
    if ast:
        ast.imprimir()
    else:
        print("No se generó un AST.")

    print("\nConstantes:", constantes)
    print("Variables:", nombres)


if __name__ == "__main__":
    probar_constantes()
    # probar_programa_complejo()
