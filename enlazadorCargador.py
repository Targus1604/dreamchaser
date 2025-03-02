"""
Función que carga el código máquina retornado
por el ensamblador en memoria para ser ejecutado
resolviendo las direcciones en los casos en que 
sea necesario
"""


def enlazador_cargador(codigo_entrada, direccion_base=0x00000):
    TAMANO_MEMORIA = 2048  # Tamaño de la memoria en celdas
    mapa_memoria = {}
    direccion = direccion_base
    if len(codigo_entrada) == 0:
        raise ValueError("El código de entrada no puede tener una longitud de 0.")

    for instr in codigo_entrada:
        if direccion >= TAMANO_MEMORIA:
            raise MemoryError(
                "Se ha excedido el tamaño de la memoria para la siguiente instrucción",
                instr,
            )

        # Verificar si la instrucción tiene metadatos de relocalización
        if "(" in instr and ")" in instr:
            # Extraer la parte base y la dirección relativa y con ello obtiene la dirección absoluta
            base, relativa = instr.split("(")
            relativa = relativa.rstrip(")")
            direccion_relativa_binaria = int(relativa)
            direccion_absoluta = direccion_base + direccion_relativa_binaria
            direccion_absoluta_binaria = format(direccion_absoluta, "011b")
            direccion_resuelta = base + direccion_absoluta_binaria
            mapa_memoria[direccion] = direccion_resuelta
        else:
            mapa_memoria[direccion] = instr

        direccion += 1

    return mapa_memoria
