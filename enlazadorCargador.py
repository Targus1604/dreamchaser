# Enlazador-Cargador
def linker_loader(object_code, base_address=0x1000):
    memory_map = {}
    address = base_address
    executable_code = []

    for instr in object_code:
        memory_map[address] = instr
        executable_code.append(f"{address:04X}: {instr}")
        address += 1

    return executable_code, memory_map


# Entrada código máquina
object_code = ["0001 0001 0010", "0010 0001 0010"]  # ADD R1, R2  # STORE R1, R2

# Ejecutar enlazador-cargador
exe_code, mem_map = linker_loader(object_code)

# Salida del enlazador-cargador
for line in exe_code:
    print(line)

print(mem_map)
