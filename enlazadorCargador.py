"""
Función que carga el código máquina retornado
por el ensamblador en memoria para ser ejecutado
resolviendo las direcciones en los casos en que 
sea necesario
"""


# Enlazador-Cargador
def enlazador_cargador(codigo_entrada, direccion_base=0x00000):
    operaciones_memoria = {
        "000000000000000100",  # CARGAR R,M
        "000000000000000110",  # ALMACENAR R,M
        "000000000000000000001",  # SALTARSICERO M
        "000000000000000000010",  # SALTARSIPOS M
        "000000000000000000011",  # SALTARSINEG M
        "000000000000000000100",  # SALTARSIPAR M
        "000000000000000000101",  # SALTARSICARRY M
        "000000000000000000110",  # SALTARSIDES M
        "000000000000000000111",  # SALTAR M
    }  # opcodes de operaciones de memoria

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
        if instr in operaciones_memoria:
            direccion_actual = format(direccion, "010b")
            direccion_resuelta = instr[:-10] + direccion_actual
            mapa_memoria[direccion] = instr
            direccion += 1
        else:
            mapa_memoria[direccion] = instr
            direccion += 1

    return mapa_memoria
