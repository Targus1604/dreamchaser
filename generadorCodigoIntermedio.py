from analizadorSemantico import AnalizadorSemantico, analizar_programa


class GeneradorCodigo:
    def __init__(self):
        self.codigo = []
        self.tabla_variables = {}
        self.contador_variables = 0
        self.etiqueta_contador = 0

    def nueva_etiqueta(self):
        """Genera una nueva etiqueta única"""
        etiqueta = f"etiqueta_{self.etiqueta_contador}"
        self.etiqueta_contador += 1
        return etiqueta

    def reservar_variable(self, nombre):
        """Reserva espacio para una variable en memoria"""
        if nombre not in self.tabla_variables:
            self.tabla_variables[nombre] = self.contador_variables
            self.contador_variables += 1
        return self.tabla_variables[nombre]

    def generar_codigo(self, ast):
        """Genera código para el AST completo"""
        if ast is None:
            return

        if ast.tipo == "programa":
            # Inicializar registros y variables
            self.codigo.append("# Inicialización del programa")

            # Procesar cada declaración o instrucción
            for hijo in ast.hijos:
                self.generar_codigo(hijo)

            # Finalizar programa
            self.codigo.append("PARAR")

        elif ast.tipo == "declaraciones":
            for hijo in ast.hijos:
                self.generar_codigo(hijo)

        elif ast.tipo == "constante":
            # Declaración de constante
            id_node = ast.hijos[0]
            valor_node = ast.hijos[1]

            # Reservar espacio para la constante
            direccion = self.reservar_variable(id_node.valor)

            # Cargar el valor en un registro y almacenarlo en memoria
            if valor_node.tipo == "NUMERO":
                self.codigo.append(f"# Declaración de constante {id_node.valor}")
                self.codigo.append(f"CARGARVALOR R0 {valor_node.valor}")
                self.codigo.append(
                    f"ALMACENAR R0 {direccion + 100}"
                )  # Offset de 100 para variables

        elif ast.tipo == "asignacion":
            # Asignación de variable
            id_node = ast.hijos[0]
            expr_node = ast.hijos[1]

            # Reservar espacio para la variable
            direccion = self.reservar_variable(id_node.valor)

            # Generar código para evaluar la expresión
            self.codigo.append(f"# Asignación a variable {id_node.valor}")
            self.generar_expresion(expr_node, "R0")

            # Almacenar el resultado en la variable
            self.codigo.append(
                f"ALMACENAR R0 {direccion + 100}"
            )  # Offset de 100 para variables

        elif ast.tipo == "si":
            # Estructura condicional 'si'
            condicion = ast.hijos[0]
            bloque = ast.hijos[1]

            etiqueta_fin = self.nueva_etiqueta()

            # Evaluar la condición
            self.codigo.append(f"# Inicio de estructura condicional 'si'")
            self.generar_condicion(condicion, etiqueta_fin)

            # Bloque de código si la condición es verdadera
            self.generar_codigo(bloque)

            # Etiqueta de fin
            self.codigo.append(f"{etiqueta_fin}:")

        elif ast.tipo == "si_sino":
            # Estructura condicional 'si-sino'
            condicion = ast.hijos[0]
            bloque_si = ast.hijos[1]
            bloque_sino = ast.hijos[2]

            etiqueta_sino = self.nueva_etiqueta()
            etiqueta_fin = self.nueva_etiqueta()

            # Evaluar la condición
            self.codigo.append(f"# Inicio de estructura condicional 'si-sino'")
            self.generar_condicion(condicion, etiqueta_sino)

            # Bloque de código si la condición es verdadera
            self.generar_codigo(bloque_si)
            self.codigo.append(f"SALTAR {etiqueta_fin}")

            # Bloque de código si la condición es falsa
            self.codigo.append(f"{etiqueta_sino}:")
            self.generar_codigo(bloque_sino)

            # Etiqueta de fin
            self.codigo.append(f"{etiqueta_fin}:")

    def generar_expresion(self, nodo, registro_destino):
        """Genera código para evaluar una expresión"""
        if nodo is None:
            return

        if nodo.tipo == "NUMERO":
            # Literal numérico
            self.codigo.append(f"CARGARVALOR {registro_destino} {nodo.valor}")

        elif nodo.tipo == "variable_ref" or nodo.tipo == "constante_ref":
            # Referencia a variable o constante
            if nodo.valor in self.tabla_variables:
                direccion = self.tabla_variables[nodo.valor]
                self.codigo.append(f"CARGAR {registro_destino} {direccion + 100}")
            else:
                # Variable no declarada, manejar error
                self.codigo.append(f"# Error: Variable {nodo.valor} no declarada")
                self.codigo.append(f"CARGARVALOR {registro_destino} 0")

        elif nodo.tipo == "binaria":
            # Operación binaria
            izq_node = nodo.hijos[0]
            op_node = nodo.hijos[1]
            der_node = nodo.hijos[2]

            # Evaluar operando izquierdo en R0
            self.generar_expresion(izq_node, "R0")

            # Evaluar operando derecho en R1
            self.generar_expresion(der_node, "R1")

            # Realizar la operación según el operador
            operador = op_node.valor
            self.codigo.append(f"# Operación binaria: {operador}")

            if operador == "SUMA":
                self.codigo.append("SUMAR R0 R1")
            elif operador == "RESTA":
                self.codigo.append("RESTAR R0 R1")
            elif operador == "MULTIPLICACION":
                self.codigo.append("MULT R0 R1")
            elif operador == "DIVISION":
                self.codigo.append("DIV R0 R1")
            elif operador == "DIVISION_ENTERA":
                self.codigo.append("DIV R0 R1")
            elif operador == "MODULO":
                self.codigo.append("MOD R0 R1")
            # Aquí se pueden agregar más operadores según sea necesario

            # Si el registro destino no es R0, copiar el resultado
            if registro_destino != "R0":
                self.codigo.append(f"COPIAR {registro_destino} R0")

    def generar_condicion(self, nodo, etiqueta_salto):
        """Genera código para evaluar una condición y salta si es falsa"""
        if nodo.tipo == "binaria":
            izq_node = nodo.hijos[0]
            op_node = nodo.hijos[1]
            der_node = nodo.hijos[2]

            # Evaluar operando izquierdo en R0
            self.generar_expresion(izq_node, "R0")

            # Evaluar operando derecho en R1
            self.generar_expresion(der_node, "R1")

            # Realizar comparación
            self.codigo.append("COMP R0 R1")

            operador = op_node.valor
            if operador == "IGUALDAD":
                # Si R0 != R1, saltar (inverso de igualdad)
                self.codigo.append(f"SALTARSINEG {etiqueta_salto}")
                self.codigo.append(f"SALTARSIPOS {etiqueta_salto}")
            elif operador == "DIFERENTE":
                # Si R0 == R1 (cero después de la resta), saltar
                self.codigo.append(f"SALTARSICERO {etiqueta_salto}")
            elif operador == "MAYOR":
                # Si R0 <= R1, saltar (inverso de mayor)
                self.codigo.append(f"SALTARSICERO {etiqueta_salto}")
                self.codigo.append(f"SALTARSINEG {etiqueta_salto}")
            elif operador == "MENOR":
                # Si R0 >= R1, saltar (inverso de menor)
                self.codigo.append(f"SALTARSICERO {etiqueta_salto}")
                self.codigo.append(f"SALTARSIPOS {etiqueta_salto}")
            elif operador == "MAYOR_IGUAL":
                # Si R0 < R1, saltar (inverso de mayor o igual)
                self.codigo.append(f"SALTARSINEG {etiqueta_salto}")
            elif operador == "MENOR_IGUAL":
                # Si R0 > R1, saltar (inverso de menor o igual)
                self.codigo.append(f"SALTARSIPOS {etiqueta_salto}")

        elif nodo.tipo == "BOOLEANO":
            # Valor booleano literal
            if nodo.valor.lower() == "false":
                self.codigo.append(f"SALTAR {etiqueta_salto}")


def generar_codigo_intermedio(ast):
    """Función principal para generar código intermedio"""
    generador = GeneradorCodigo()
    generador.generar_codigo(ast)
    return generador.codigo, generador.tabla_variables


# Ejemplo de uso
def compilar_programa(codigo_fuente):
    # Realizar análisis sintáctico y semántico
    print("\n--- ANÁLISIS SINTÁCTICO Y SEMÁNTICO ---")
    ast = analizar_programa(codigo_fuente)

    if ast:
        # Generar código intermedio
        print("\n--- GENERACIÓN DE CÓDIGO INTERMEDIO ---")
        codigo, tabla_variables = generar_codigo_intermedio(ast)

        print("Tabla de variables:")
        for var, dir in tabla_variables.items():
            print(f"  {var}: {dir + 100}")

        print("\nCódigo ensamblador generado:")
        for linea in codigo:
            print(f"  {linea}")

        return codigo
    else:
        print("Error: No se pudo generar el AST.")
        return None


# Programa de prueba
programa_prueba = """const NOTA 4
a = 10
b = NOTA + 1
"""

# Compilar el programa
compilar_programa(programa_prueba)
