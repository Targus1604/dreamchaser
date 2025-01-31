# Enlazador-Cargador
def enlazador_cargador(codigo_entrada, direccion_base=0x00000):
    TAMANO_MEMORIA = 2048  # Tamaño de la memoria en celdas
    mapa_memoria = {}
    direccion = direccion_base
    codigo_ejecutable = []

    for instr in codigo_entrada:
        if direccion >= TAMANO_MEMORIA:
            raise MemoryError("Se ha excedido el tamaño de la memoria.")
        mapa_memoria[direccion] = instr
        codigo_ejecutable.append(f"{direccion:04X}: {instr}")
        direccion += 1

    return codigo_ejecutable, mapa_memoria


# Entrada código máquina (32 bits por instrucción)
codigo_entrada = [
    "00000001000100100000000000000000",  # ADD R1, R2
    "00000010000100100000000000000000",  # STORE R1, R2
    "00000010000100100000000000000000",  # STORE R1, R2
]

# Ejecutar enlazador-cargador
codigo_ejecutar, mapa_memoria = enlazador_cargador(codigo_entrada)

# Salida del enlazador-cargador
for line in codigo_ejecutar:
    print(line)

print("Memoria", mapa_memoria)
