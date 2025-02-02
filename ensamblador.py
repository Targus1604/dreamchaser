# Diccionario de operaciones (18 bits para la operación)
codigo_operaciones = {
    "CARGAR": "000000000000000100",  # Operación CARGAR (18 bits)
    "ALMACENAR": "000000000000000110",  # Operación ALMACENAR (18 bits)
}

# Registro de selección (3 bits)
registros = {
    "R0": "000",  # Registro 0 (3 bits)
    "R1": "001",  # Registro 1 (3 bits)
    "R2": "010",  # Registro 2 (3 bits)
    "R3": "011",  # Registro 3 (3 bits)
    "R4": "100",  # Registro 4 (3 bits)
    "R5": "101",  # Registro 5 (3 bits)
    "R6": "110",  # Registro 6 (3 bits)
    "R7": "111",  # Registro 7 (3 bits)
}

# Diccionario de operaciones de salto (21 bits)
codigo_saltos = {
    "SALTAR": "000000000000000000111",  # SALTAR (21 bits)
    "SALTARSICERO": "000000000000000000001",  # SALTAR SI CERO
    "SALTARSIPOS": "000000000000000000010",  # SALTAR SI POSITIVO
    "SALTARSINEG": "000000000000000000011",  # SALTAR SI NEGATIVO
    "SALTARSIPAR": "000000000000000000100",  # SALTAR SI PAR
    "SALTARSICARRY": "000000000000000000101",  # SALTAR SI CARRY
    "SALTARSIDES": "000000000000000000110",  # SALTAR SI DESBORDAMIENTO
}

def ensamblador(lista_instrucciones):
    instrucciones_binarias = []

    for direccion, instruccion in enumerate(lista_instrucciones):
        partes = instruccion.split()
        operacion = partes[0]

        # Determinar la dirección de memoria de 10 bits (últimos 10 bits)
        direccion_binaria = format(int(partes[-1]), "011b")

        # Si la instrucción es CARGAR o ALMACENAR
        if operacion in codigo_operaciones:
            registro = partes[1]  # El registro (R)
            # Asegurarse de que el registro sea válido
            if registro not in registros:
                raise ValueError(f"Registro desconocido: {registro}")
            registro_binario = registros[registro]
            # Formar la instrucción completa de 32 bits
            binario_operacion = codigo_operaciones[operacion]  # Operación en binario (18 bits)
            instruccion_binaria = binario_operacion + registro_binario + direccion_binaria
            instrucciones_binarias.append(instruccion_binaria)

        # Si la instrucción es un salto
        elif operacion in codigo_saltos:
            # Instrucción de salto con 21 bits + dirección de 10 bits
            binario_operacion = codigo_saltos[operacion]
            # Formar la instrucción de salto completa de 32 bits
            instruccion_binaria = binario_operacion + direccion_binaria
            instrucciones_binarias.append(instruccion_binaria)

        else:
            raise ValueError(f"Operación desconocida: {operacion}")

    return instrucciones_binarias


# Prueba del ensamblador
codigo_entrada = [
    "SALTAR 0",
    "CARGAR R4 2",
    "CARGAR R5 4",
    "ALMACENAR R6 32",
    "ALMACENAR R7 40",
    "ALMACENAR R2 1",
    "SALTARSICERO 7",
    "SALTARSICARRY 72",
    "SALTARSIPAR 130",
    "SALTAR 3",
    "ALMACENAR R5 9",
    "SALTAR 0"
]

# Generar el código binario
codigo_entrada_enlazador = ensamblador(codigo_entrada)

# Mostrar el resultado esperado
print("Código de entrada para el enlazador-cargador:")
for instr in codigo_entrada_enlazador:
    print(instr)
