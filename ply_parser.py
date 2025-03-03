import src.ply.yacc as yacc
from analisisLexico import constantes, lexer, tokens

# Diccionario de nombres (variables y constantes)
nombres = {}


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
    ("left", "SUMA", "RESTA"),
    ("left", "MULTIPLICACION", "DIVISION", "DIVISION_ENTERA"),
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
    | expresion"""
    p[0] = p[1]


def p_declaracion_constante(p):
    """declaracion_constante : CONST ID NUMERO
    | CONST ESPACIO ID ESPACIO NUMERO"""
    if len(p) == 4:
        id_name, valor = p[2], p[3]
    else:
        id_name, valor = p[3], p[5]

    constantes[id_name] = valor
    p[0] = Nodo("constante", [Nodo("ID", valor=id_name), Nodo("NUMERO", valor=valor)])


def p_declaracion_constante_string(p):
    """declaracion_constante : CONST ID STRING
    | CONST ESPACIO ID ESPACIO STRING"""
    if len(p) == 4:
        id_name, valor = p[2], p[3]
    else:
        id_name, valor = p[3], p[5]

    constantes[id_name] = valor
    p[0] = Nodo("constante", [Nodo("ID", valor=id_name), Nodo("STRING", valor=valor)])


def p_declaracion_asignacion(p):
    """declaracion_asignacion : ID ASIGNACION expresion
    | ID ESPACIO ASIGNACION ESPACIO expresion"""
    if len(p) == 4:
        id_name, expr = p[1], p[3]
    else:
        id_name, expr = p[1], p[5]

    nombres[id_name] = expr
    p[0] = Nodo("asignacion", [Nodo("ID", valor=id_name), expr])


def p_expresion_binaria(p):
    """expresion : expresion SUMA expresion
    | expresion RESTA expresion
    | expresion MULTIPLICACION expresion
    | expresion DIVISION expresion
    | expresion DIVISION_ENTERA expresion
    | expresion ESPACIO SUMA ESPACIO expresion
    | expresion ESPACIO RESTA ESPACIO expresion
    | expresion ESPACIO MULTIPLICACION ESPACIO expresion
    | expresion ESPACIO DIVISION ESPACIO expresion
    | expresion ESPACIO DIVISION_ENTERA ESPACIO expresion"""
    if len(p) == 4:
        operador = p[2]
        izq, der = p[1], p[3]
    else:
        operador = p[3]
        izq, der = p[1], p[5]

    p[0] = Nodo("binaria", [izq, Nodo("operador", valor=operador), der])


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
        p[0] = Nodo("constante_ref", valor=p[1])
    elif p[1] in nombres:
        p[0] = Nodo("variable_ref", valor=p[1])
    else:
        print(f"Error: identificador '{p[1]}' no definido")
        p[0] = Nodo("error", valor=p[1])


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
    # No limpiamos constantes porque en tu código original no las limpiabas

    # Analizar el programa
    lexer.lineno = 1  # Reiniciar el contador de líneas
    ast = parser.parse(programa, lexer=lexer)
    return ast


# Programa de prueba
def probar_parser():
    programa_minimo = """
const NOTA 4
a = 10
b = NOTA + 1
"""

    ast = analizar(programa_minimo)
    print("\nÁrbol de sintaxis abstracta (AST):")
    if ast:
        ast.imprimir()  # Usar el método de impresión indentada
    else:
        print("No se generó un AST.")

    print("\nConstantes:", constantes)
    print("Variables:", nombres)


if __name__ == "__main__":
    probar_parser()
