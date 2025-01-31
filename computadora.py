from enlazadorCargador import enlazador_cargador

"""
En esta clase se simulará DREAMCHASER teniendo los módulos construidos
-Preprocesador
-Analizador léxico
-Ensamblador
-Enlazador Cargador
"""


class Computadora:
    def __init__(self, tamano_memoria=2048):
        # Simula la memoria (cada celda de memoria almacena un entero de 32 bits)
        self.memoria = [0] * tamano_memoria

        """---------------------------------------------------------------------------------
        BANDERAS DE DREAMCHASER
        ------------------------------------------------------------------------------------"""
        # Bandera para carry
        self.bandera_carry = 0
        # Bandera para zero
        self.bandera_zero = 0
        # Bandera para negativo
        self.bandera_neg = 0
        # Bandera para par
        self.bandera_par = 0
        # Bandera para desbordamiento
        self.bandera_desb = 0
        # Puntero de instrucción (PC)
        self.pc = 0

    # Carga el código binario proporcionado por el ensamblador de manera contigua en memoria
    # Comenzando desde el 0
    def cargar_codigo(self, codigo_entrada, direccion_base=0x0000):
        mapa_memoria = enlazador_cargador(codigo_entrada, direccion_base)
        for direccion, instr in mapa_memoria.items():
            self.memoria[direccion] = instr

    # Muestra únicamente las celdas de memoria con instrucciones (usar self.memoria para un paneo completo)
    def mostrar_memoria(self):
        for direccion, instr in enumerate(self.memoria):
            if instr != 0:
                print(f"{direccion:04X}: {instr}")


# Entrada código máquina (32 bits por instrucción)
codigo_entrada = [
    "00000001000100100000000000000000",  # ADD R1, R2
    "00000010000100100000000000000000",  # STORE R1, R2
    "00000010000100100000000000000000",  # STORE R1, R2
]

dreamChaser = Computadora()
dreamChaser.cargar_codigo(codigo_entrada)
dreamChaser.mostrar_memoria()
