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
        self.registros = [0] * 8

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

    """
    -------------------------
    ENLAZADOR - CARGADOR
    -------------------------
    """

    # Carga el código binario proporcionado por el ensamblador de manera contigua en memoria
    # Comenzando desde el 0
    def cargar_codigo(self, codigo_entrada, direccion_de_inicio=0x0000):
        mapa_memoria = enlazador_cargador(codigo_entrada, direccion_de_inicio)
        for direccion, instr in mapa_memoria.items():
            self.memoria[direccion] = instr

    # Muestra únicamente las celdas de memoria con instrucciones (usar self.memoria para un paneo completo)
    def mostrar_memoria(self):
        memoria_ocupada = 0
        for direccion, instr in enumerate(self.memoria):
            if instr != 0:
                memoria_ocupada += 1
                # La dirección es mostrada en exadecimal
                print(f"{direccion:04X}: {instr}")
        if memoria_ocupada == 0:
            print("No hay instrucciones en memoria")


# Entrada código máquina (32 bits por instrucción)
codigo_entrada = [
    "00000000000000010100000000100000",
    "00000000000000010100100000000000",
    "00000000000000010101000000000001",
    "00000000000000000000100000000111",
    "00000000000000000000000101001000",
    "00000000000000000000000110000010",
    "00000000000000000011100000000011",
    "00000000000000011000100000001001",
    "00000000000000000000000000000000",
]

dreamChaser = Computadora()
dreamChaser.cargar_codigo(codigo_entrada, direccion_de_inicio=16)
dreamChaser.mostrar_memoria()
