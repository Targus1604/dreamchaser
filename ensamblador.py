# Define opcode segun tipo de operacion
especiales = {"PARAR": "00000000000000000000000000000000"}

carga_memoria = {
    "CARGAR": "000000000000000100",  # Operación CARGAR (18 bits)
    "ALMACENAR": "000000000000000110",  # Operación ALMACENAR (18 bits) }]
}

carga_operacion_valor = {
    "CARGARVALOR": "000000000000000101",  # Operación CARGARVALOR (20 bits)
    "LSL": "000000000000000001",
    "LSR": "000000000000000010",
    "ASR": "000000000000000011",
    "ROTACIONL": "000000000000000111",
    "ROTACIONR": "000000000000001000",
}

# Diccionario de operaciones de salto (21 bits)
saltos = {
    "SALTAR": "000000000000000000111",  # SALTAR (21 bits)
    "SALTARSICERO": "000000000000000000001",  # SALTAR SI CERO
    "SALTARSIPOS": "000000000000000000010",  # SALTAR SI POSITIVO
    "SALTARSINEG": "000000000000000000011",  # SALTAR SI NEGATIVO
    "SALTARSIPAR": "000000000000000000100",  # SALTAR SI PAR
    "SALTARSICARRY": "000000000000000000101",  # SALTAR SI CARRY
    "SALTARSIDES": "000000000000000000110",  # SALTAR SI DESBORDAMIENTO
    "SALTARSINODES": "000000000000000001000",  # SALTAR SI DESBORDAMIENTO
}

operaciones_registros = {
    "OR": "00000000000000000000000001",
    "AND": "00000000000000000000000010",
    "XOR": "00000000000000000000000011",
    "NOT": "00000000000000000000000100",
    "SUMAR": "00000000000000000000000101",
    "RESTAR": "00000000000000000000000110",
    "MULT": "00000000000000000000000111",
    "DIV": "00000000000000000000001000",
    "COPIAR": "00000000000000000000001001",
    "COMP": "00000000000000000000001010",
    "INTERCAMBIAR": "00000000000000000000001011",
    "MOD": "00000000000000000000001101",
}

# Diccionario de operaciones (18 bits para la operación)
codigo_operaciones = (
    especiales | carga_memoria | carga_operacion_valor | saltos | operaciones_registros
)

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


def traducir_instruccion(instruccion):
    if instruccion == "PARAR":
        return codigo_operaciones["PARAR"]

    partes = instruccion.split()
    nombre_instruccion = partes[0]
    if nombre_instruccion not in codigo_operaciones:  # verificar si existe opcode
        raise ValueError(f"Operación desconocida: {nombre_instruccion}")
    opcode = codigo_operaciones[nombre_instruccion]

    # Determinar el resto de la instrucción
    if nombre_instruccion in carga_memoria:
        if partes[1] not in registros:
            raise ValueError(f"Registro desconocido: {partes[1]}")
        registro = registros[partes[1]]

        # Codificamos los últimos 11 bits como dirección relativa
        direccion_binaria = format(int(partes[2]) & 0x3FF, "011b")  # Solo 10 bits
        return opcode + registro + direccion_binaria

    elif nombre_instruccion in carga_operacion_valor:
        if partes[1] not in registros:
            raise ValueError(f"Registro desconocido: {partes[1]}")
        registro = registros[partes[1]]

        # Para valores inmediatos, mantener 11 bits
        valor_binario = format(int(partes[2]) & 0x7FF, "011b")  # 11 bits
        return opcode + registro + valor_binario

    elif nombre_instruccion in saltos:
        # Codificamos los últimos 11 bits como dirección relativa
        direccion_binaria = format(int(partes[1]) & 0x3FF, "011b")  # Solo 10 bits
        return opcode + direccion_binaria

    elif nombre_instruccion in operaciones_registros:
        registro1 = registros[partes[1]]
        registro2 = registros[partes[2]]
        return opcode + registro1 + registro2

    else:
        raise ValueError(f"Operación desconocida: {partes[0]}")


def ensamblador(lista_instrucciones):
    # Primera pasada: recolectar etiquetas
    etiquetas = {}
    instrucciones_limpias = []
    contador_instrucciones = 0

    for i, linea in enumerate(lista_instrucciones):
        # Si la línea contiene una etiqueta (termina con :)
        if ":" in linea:
            partes = linea.split(":", 1)
            etiqueta = partes[0].strip()
            # Se guarda de la siguiente manera {etiqueta: direccion}
            etiquetas[etiqueta] = contador_instrucciones

            # Si hay una instrucción después de la etiqueta se agrega a instrucciones limpias
            if len(partes) > 1 and partes[1].strip():
                instruccion = partes[1].strip()
                instrucciones_limpias.append(instruccion)
                contador_instrucciones += 1
        else:
            # En caso de no tener etiquetas simplemente se añade la instrucción
            instrucciones_limpias.append(linea)
            contador_instrucciones += 1

    # Segunda pasada: generar código binario con metadatos de relocalización
    resultado = []

    for i, instruccion in enumerate(instrucciones_limpias):
        partes = instruccion.split()
        nombre_instruccion = partes[0]

        # Verificar si la instrucción requiere relocalización
        requiere_relocalizacion = False
        valor_referencia = None

        # Para operaciones de salto y memoria que requieren direcciones
        if nombre_instruccion in saltos or nombre_instruccion in carga_memoria:
            # El segundo argumento podría ser una etiqueta o una dirección
            if len(partes) > 1:
                argumento = partes[-1]  # Último argumento, que podría ser la dirección

                # Si el argumento está en nuestro diccionario de etiquetas
                if argumento in etiquetas:
                    # Es una referencia a una etiqueta
                    requiere_relocalizacion = True
                    valor_referencia = etiquetas[argumento]
                    nueva_instruccion = " ".join(partes[:-1] + [str(valor_referencia)])
                elif argumento.isdigit() and int(argumento) < len(
                    instrucciones_limpias
                ):
                    # Es una dirección numérica pero parece ser interna al programa
                    requiere_relocalizacion = True
                    valor_referencia = int(argumento)
                    nueva_instruccion = instruccion
                else:
                    # Es una dirección externa, no requiere relocalización
                    nueva_instruccion = instruccion
            else:
                nueva_instruccion = instruccion
        else:
            # Otros tipos de instrucciones
            nueva_instruccion = instruccion

        # Traducir la instrucción a código binario completo
        codigo_binario = traducir_instruccion(nueva_instruccion)

        # Agregar metadatos de relocalización si es necesario
        if requiere_relocalizacion:
            # Eliminar los últimos 11 bits y reemplazarlos por el valor entre paréntesis
            codigo_base = codigo_binario[:-11]  # Todo excepto los últimos 11 bits
            resultado.append(f"{codigo_base}({valor_referencia})")
        else:
            resultado.append(codigo_binario)

    return resultado, etiquetas


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
    "SALTAR 0",
]

print(ensamblador(codigo_entrada)[0])
