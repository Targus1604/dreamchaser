from ply_parser import analizar


class TablaSimbolos:
    def __init__(self):
        self.tabla = [{}]  # Pila de ámbitos (scopes)
        self.errores = []

    def entrar_ambito(self):
        """Crea un nuevo ámbito"""
        self.tabla.append({})

    def salir_ambito(self):
        """Sale del ámbito actual"""
        if len(self.tabla) > 1:
            self.tabla.pop()

    def declarar(self, nombre, tipo, linea=None):
        """Declara un símbolo en el ámbito actual"""
        if nombre in self.tabla[-1]:
            self.errores.append(
                f"Error semántico: Redeclaración de '{nombre}' en línea {linea}"
            )
            return False
        self.tabla[-1][nombre] = {"tipo": tipo, "linea": linea}
        return True

    def buscar(self, nombre):
        """Busca un símbolo en todos los ámbitos, del más interno al más externo"""
        for ambito in reversed(self.tabla):
            if nombre in ambito:
                return ambito[nombre]
        return None

    def obtener_errores(self):
        """Devuelve la lista de errores semánticos"""
        return self.errores


class AnalizadorSemantico:
    def __init__(self):
        self.tabla_simbolos = TablaSimbolos()
        self.tipos_operandos = {
            "NUMERO": "numerico",
            "STRING": "cadena",
            "BOOLEANO": "booleano",
        }

        # Tabla de compatibilidad de operaciones
        self.operaciones_validas = {
            "SUMA": {
                ("numerico", "numerico"): "numerico",
                ("cadena", "cadena"): "cadena",
            },
            "RESTA": {
                ("numerico", "numerico"): "numerico",
            },
            "MULTIPLICACION": {
                ("numerico", "numerico"): "numerico",
            },
            "DIVISION": {
                ("numerico", "numerico"): "numerico",
            },
            "DIVISION_ENTERA": {
                ("numerico", "numerico"): "numerico",
            },
            "IGUALDAD": {
                ("numerico", "numerico"): "booleano",
                ("cadena", "cadena"): "booleano",
                ("booleano", "booleano"): "booleano",
            },
            "DIFERENTE": {
                ("numerico", "numerico"): "booleano",
                ("cadena", "cadena"): "booleano",
                ("booleano", "booleano"): "booleano",
            },
            "MAYOR": {
                ("numerico", "numerico"): "booleano",
                ("cadena", "cadena"): "booleano",
            },
            "MENOR": {
                ("numerico", "numerico"): "booleano",
                ("cadena", "cadena"): "booleano",
            },
            "MAYOR_IGUAL": {
                ("numerico", "numerico"): "booleano",
                ("cadena", "cadena"): "booleano",
            },
            "MENOR_IGUAL": {
                ("numerico", "numerico"): "booleano",
                ("cadena", "cadena"): "booleano",
            },
        }

    def analizar(self, ast):
        """Analiza semánticamente un AST"""
        if ast is None:
            return

        if ast.tipo == "programa":
            # Procesar el programa principal
            for hijo in ast.hijos:
                self.analizar(hijo)

        elif ast.tipo == "declaraciones":
            # Procesar cada declaración
            for hijo in ast.hijos:
                self.analizar(hijo)

        elif ast.tipo == "constante":
            # Declaración de constante
            id_node = ast.hijos[0]
            valor_node = ast.hijos[1]
            tipo = self.obtener_tipo(valor_node)
            self.tabla_simbolos.declarar(id_node.valor, tipo, linea=None)

        elif ast.tipo == "asignacion":
            # Asignación de variable
            id_node = ast.hijos[0]
            expr_node = ast.hijos[1]

            # Verificar si ya existe como constante
            simbolo = self.tabla_simbolos.buscar(id_node.valor)
            if simbolo and simbolo["tipo"] == "constante":
                self.tabla_simbolos.errores.append(
                    f"Error semántico: No se puede asignar un valor a la constante '{id_node.valor}'"
                )
                return

            # Obtener el tipo de la expresión
            tipo_expr = self.evaluar_tipo_expresion(expr_node)

            # Si es una nueva variable, declararla
            if not simbolo:
                self.tabla_simbolos.declarar(id_node.valor, tipo_expr, linea=None)
            # Si es una reasignación, verificar compatibilidad de tipos
            else:
                tipo_anterior = simbolo["tipo"]
                if (
                    tipo_anterior != tipo_expr
                    and tipo_anterior != "any"
                    and tipo_expr != "any"
                ):
                    self.tabla_simbolos.errores.append(
                        f"Error semántico: No se puede asignar valor de tipo '{tipo_expr}' a variable '{id_node.valor}' de tipo '{tipo_anterior}'"
                    )

        elif ast.tipo == "binaria":
            # Operación binaria
            izq_node = ast.hijos[0]
            op_node = ast.hijos[1]
            der_node = ast.hijos[2]

            tipo_izq = self.evaluar_tipo_expresion(izq_node)
            tipo_der = self.evaluar_tipo_expresion(der_node)
            operador = op_node.valor

            # Verificar compatibilidad de tipos para la operación
            if operador in self.operaciones_validas:
                tipo_resultado = self.verificar_operacion(tipo_izq, operador, tipo_der)
                if tipo_resultado is None:
                    self.tabla_simbolos.errores.append(
                        f"Error semántico: Operación '{operador}' no válida entre tipos '{tipo_izq}' y '{tipo_der}'"
                    )

        elif ast.tipo == "si" or ast.tipo == "si_sino":
            # Estructuras de control if/else
            condicion = ast.hijos[0]
            tipo_condicion = self.evaluar_tipo_expresion(condicion)

            if tipo_condicion != "booleano" and tipo_condicion != "any":
                self.tabla_simbolos.errores.append(
                    f"Error semántico: La condición de una estructura 'si' debe ser de tipo booleano, no '{tipo_condicion}'"
                )

            # Analizar bloques de código
            for i in range(1, len(ast.hijos)):
                self.tabla_simbolos.entrar_ambito()
                self.analizar(ast.hijos[i])
                self.tabla_simbolos.salir_ambito()

        elif ast.tipo == "funcion":
            # Declaración de función
            id_node = ast.hijos[0]
            params_node = ast.hijos[1]
            cuerpo_node = ast.hijos[2]

            # Declarar la función en el ámbito actual
            self.tabla_simbolos.declarar(id_node.valor, "funcion", linea=None)

            # Crear un nuevo ámbito para los parámetros y el cuerpo
            self.tabla_simbolos.entrar_ambito()

            # Declarar los parámetros en el ámbito de la función
            if params_node.tipo == "parametros":
                for param in params_node.hijos:
                    self.tabla_simbolos.declarar(param.valor, "any", linea=None)

            # Analizar el cuerpo de la función
            self.analizar(cuerpo_node)

            # Salir del ámbito de la función
            self.tabla_simbolos.salir_ambito()

        elif ast.tipo == "llamada_funcion":
            # Llamada a función
            id_node = ast.hijos[0]
            args_node = ast.hijos[1]

            # Verificar que la función exista
            simbolo = self.tabla_simbolos.buscar(id_node.valor)
            if not simbolo:
                self.tabla_simbolos.errores.append(
                    f"Error semántico: Función '{id_node.valor}' no declarada"
                )
            elif simbolo["tipo"] != "funcion":
                self.tabla_simbolos.errores.append(
                    f"Error semántico: '{id_node.valor}' no es una función"
                )

            # Analizar los argumentos
            if args_node.tipo == "argumentos":
                for arg in args_node.hijos:
                    self.evaluar_tipo_expresion(arg)

    def obtener_tipo(self, nodo):
        """Obtiene el tipo de un nodo literal"""
        if nodo.tipo in self.tipos_operandos:
            return self.tipos_operandos[nodo.tipo]
        return "any"  # Tipo desconocido o no inferible

    def evaluar_tipo_expresion(self, nodo):
        """Evalúa el tipo de una expresión recursivamente"""
        if nodo is None:
            return "any"

        if nodo.tipo in self.tipos_operandos:
            # Tipo literal directo
            return self.tipos_operandos[nodo.tipo]

        elif nodo.tipo == "variable_ref" or nodo.tipo == "constante_ref":
            # Referencia a variable o constante
            simbolo = self.tabla_simbolos.buscar(nodo.valor)
            if simbolo:
                return simbolo["tipo"]
            else:
                self.tabla_simbolos.errores.append(
                    f"Error semántico: Variable o constante '{nodo.valor}' no declarada"
                )
                return "any"

        elif nodo.tipo == "binaria":
            # Operación binaria
            izq_node = nodo.hijos[0]
            op_node = nodo.hijos[1]
            der_node = nodo.hijos[2]

            tipo_izq = self.evaluar_tipo_expresion(izq_node)
            tipo_der = self.evaluar_tipo_expresion(der_node)
            operador = op_node.valor

            # Verificar compatibilidad y retornar tipo resultante
            return self.verificar_operacion(tipo_izq, operador, tipo_der) or "any"

        elif nodo.tipo == "llamada_funcion":
            # Llamada a función - por ahora no inferimos tipo retornado
            return "any"

        return "any"  # Tipo desconocido

    def verificar_operacion(self, tipo_izq, operador, tipo_der):
        """Verifica si una operación es válida entre dos tipos y retorna el tipo resultante"""
        if operador in self.operaciones_validas:
            par_tipos = (tipo_izq, tipo_der)
            if par_tipos in self.operaciones_validas[operador]:
                return self.operaciones_validas[operador][par_tipos]
        return None


def analizar_programa(codigo_fuente):
    print("\n--- ANÁLISIS SINTÁCTICO ---")
    ast = analizar(codigo_fuente)

    if ast:
        print("AST generado correctamente")
        ast.imprimir()

        print("\n--- ANÁLISIS SEMÁNTICO ---")
        analizador = AnalizadorSemantico()
        analizador.analizar(ast)

        errores = analizador.tabla_simbolos.obtener_errores()
        if errores:
            print("Se encontraron errores semánticos:")
            for error in errores:
                print(f"  - {error}")
        else:
            print("Análisis semántico completado sin errores.")
    else:
        print("Error: No se pudo generar el AST.")

    return ast


# Programa de prueba con varios casos semánticos
programa_prueba = """const NOTA 4
a = 10
b = NOTA + 1
"""

analizar_programa(programa_prueba)
