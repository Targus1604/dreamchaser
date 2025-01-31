"""
Función que carga el código máquina retornado
por el ensamblador en memoria para ser ejecutado
"""


# Enlazador-Cargador
def enlazador_cargador(codigo_entrada, direccion_base=0x00000):
    TAMANO_MEMORIA = 2048  # Tamaño de la memoria en celdas
    mapa_memoria = {}
    direccion = direccion_base

    for instr in codigo_entrada:
        if direccion >= TAMANO_MEMORIA:
            raise MemoryError("Se ha excedido el tamaño de la memoria.")
        mapa_memoria[direccion] = instr
        direccion += 1

    return mapa_memoria
