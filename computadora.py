from enlazadorCargador import enlazador_cargador
from utils.programas import codigo_entrada_enlazador


class Computadora:
    def __init__(self, tamano_memoria=2048):
        # Simula la memoria (cada celda de memoria almacena un entero de 32 bits)
        self.memoria = ["0" * 32 for _ in range(tamano_memoria)]
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
        self.interfaz = None
        self.longitud_programa = 0

        """----------------------------------------------------------------------------------------------------

        OPERACIONES DE DREAMCHASER

        -------------------------------------------------------------------------------------------------------"""

        self.operaciones_registro_memoria = {
            65536: self.cargar,  # CARGAR
            98304: self.almacenar,  # ALMACENAR
        }
        self.operaciones_registro_valor = {
            16384: self.lsl,  # LSL
            32768: self.lsr,  #  LSR
            49152: self.asr,  # ASR
            81920: self.cargar_valor,  # CARGAR VALOR
            114688: self.rotacionl,  # ROTACION IZQUIERDA
            131072: self.rotacionr,  # ROTACION DERECHA
        }

        self.operaciones_salto = {
            2048: self.saltar_si_cero,  # SALTAR SI CERO
            4096: self.saltar_si_positivo,  # SALTARSIPOS
            6144: self.saltar_si_negativo,  # SALTARSINEG
            8192: self.saltar_si_par,  # SALTARSIPAR
            10240: self.saltar_si_carry,  # SALTARSICARRY
            12288: self.saltar_si_desbordamiento,  # SALTARSIDES
            14336: self.saltar,  # SALTAR
            16384: self.saltar_si_no_desbordamiento,  # SALTASINODES
        }

        self.operaciones_registros = {
            64: self.or_,  # OR
            128: self.and_,  # AND
            192: self.xor_,  # XOR
            256: self.not_,  # NOT
            320: self.sumar,  # SUMAR
            384: self.restar,  # RESTAR
            448: self.multiplicar,  # MULT
            512: self.dividir,  # DIV
            576: self.copiar,  # COPIAR
            640: self.comparar,  # COMP
            704: self.intercambiar,  # INTERCAMBIAR
            832: self.modulo,  # MOD
        }

    """-------------------------
    ENLAZADOR - CARGADOR
    -------------------------
    """

    # Carga el código binario proporcionado por el ensamblador de manera contigua en memoria
    # Comenzando desde el 0
    def cargar_codigo(self, codigo_entrada, direccion_de_inicio=0x0000):
        mapa_memoria = enlazador_cargador(codigo_entrada, direccion_de_inicio)
        for direccion, instr in mapa_memoria.items():
            self.memoria[direccion] = instr
        self.longitud_programa = len(codigo_entrada)
        return self.memoria

    def mostrar_memoria(self):
        memoria_ocupada = []

        for direccion, instr in enumerate(self.memoria):
            if instr != 0:
                memoria_ocupada.append(
                    (f"{direccion}", instr)
                )  # Dirección en Hex, valor binario

        if not memoria_ocupada:
            return [("No hay instrucciones en memoria", "")]  # Mensaje en la tabla

        return memoria_ocupada  # Retorna la lista de tuplas

    def ejecutar_instruccion(self):
        if self.pc < len(self.memoria):
            instruccion = int(self.memoria[self.pc], 2)
            mensaje = f"Ejecutando instrucción en PC={self.pc}: {self.memoria[self.pc]}"
            print(mensaje)
            self.interfaz.actualizar_consola(mensaje)
            if instruccion == 0b00000000000000000000000000000000:
                mensaje = "PARAR Ejecución finalizada."
                print(mensaje)
                self.interfaz.actualizar_consola(mensaje, "green")
                return
            else:
                try:
                    self.decodificar_y_ejecutar(instruccion)
                except KeyError:
                    mensaje = f"Error: Instrucción desconocida en PC={self.pc}: {self.memoria[self.pc]}"
                    print(mensaje)
                    self.interfaz.actualizar_consola(mensaje, color="red")
                    return
                self.pc += 1
                self.actualizar_interfaz()

    def actualizar_interfaz(self):
        if self.interfaz:
            self.interfaz.actualizar_registros()
            self.interfaz.actualizar_indicadores_alu()
            self.interfaz.actualizar_unidad_control()

    """
    ---------------------------------------------------------------------------------------------------------


    FORMATO DE OPERACIONES Y ASIGNACIÓN DE OPCODE DREAMCHASER


    ---------------------------------------------------------------------------------------------------------
    """

    def decodificar_y_ejecutar(self, instruccion):
        """Carga y almacenamiento entre registro y memoria"""
        opcode = instruccion & 0xFFFFC000
        opcode1 = instruccion & 0xFFFFC000
        opcode2 = instruccion & 0xFFFFF800
        opcode3 = instruccion & 0xFFFFFFC0
        reg1 = (instruccion & 0x00003800) >> 11  # Registro 1
        direccion = instruccion & 0x000007FF  # direccion de memoria

        # Llamar la función correspondiente al opcode, si existe
        if opcode in self.operaciones_registro_memoria:
            self.operaciones_registro_memoria[opcode](reg1, direccion)
        elif opcode1 in self.operaciones_registro_valor:
            """Carga y almacenamiento entre registro y memoria"""
            reg1 = (instruccion & 0x00003800) >> 11  # Registro 1
            valor = instruccion & 0x000007FF  # Valor inmediato
            self.operaciones_registro_valor[opcode1](reg1, valor)
        elif opcode2 in self.operaciones_salto:
            """Operaciones de salto"""
            direccion = instruccion & 0x000007FF  # dirección de salto
            self.operaciones_salto[opcode2](direccion)
        elif opcode3 in self.operaciones_registros:
            reg1 = (instruccion & 0x00000038) >> 3
            reg2 = instruccion & 0x00000007
            self.operaciones_registros[opcode3](reg1, reg2)
        else:
            mensaje = f"Operación desconocida: {opcode}"
            print(mensaje)
            self.interfaz.actualizar_consola(mensaje)

    """--------------------------------------------
    OPERACIONES ENTRE REGISTRO Y MEMORIA
    ------------------------------------------------"""

    def cargar(self, reg1, direccion):
        """CARGAR R1, M[valor]"""
        self.registros[reg1] = int(self.memoria[direccion], 2)
        mensaje = f"CARGAR: Registro {reg1} cargado con valor de memoria en dirección {direccion}"
        print(mensaje)
        self.interfaz.actualizar_consola(mensaje)

    def almacenar(self, reg1, direccion):
        """ALMACENAR R1, M[valor]"""
        self.memoria[direccion] = format(self.registros[reg1], "032b")
        mensaje = f"ALMACENAR: Valor del registro {reg1} almacenado en memoria en dirección {direccion}"
        print(mensaje)
        self.interfaz.actualizar_consola(mensaje)

    """---------------------------------------------
    OPERACIONES ENTRE REGISTRO Y VALORES
    ------------------------------------------------"""

    def lsl(self, reg1, valor):
        """LSL R1, valor"""
        self.registros[reg1] = self.registros[reg1] << valor
        mensaje = (
            f"LSL: Registro {reg1} desplazado a la izquierda por {valor} posiciones"
        )
        print(mensaje)
        self.interfaz.actualizar_consola(mensaje)

    def lsr(self, reg1, valor):
        """LSR (Logical Shift Right) R1, valor"""
        # Desplazamiento lógico a la derecha
        self.registros[reg1] = (self.registros[reg1] & 0xFFFFFFFF) >> valor
        mensaje = f"LSR: Registro {reg1} desplazado a la derecha por {valor} posiciones"
        print(mensaje)
        self.interfaz.actualizar_consola(mensaje)

    def asr(self, reg1, valor):
        """ASR R1, valor"""
        self.registros[reg1] = self.registros[reg1] >> valor
        mensaje = f"ASR: Registro {reg1} desplazado aritméticamente a la derecha por {valor} posiciones"
        print(mensaje)
        self.interfaz.actualizar_consola(mensaje)

    def cargar_valor(self, reg1, valor):
        """CARGAR VALOR R1, valor"""
        self.registros[reg1] = valor
        mensaje = f"CARGAR VALOR: Registro {reg1} cargado con valor {valor}"
        print(mensaje)
        self.interfaz.actualizar_consola(mensaje)

    def rotacionl(self, reg1, valor):
        """ROTACION IZQUIERDA R1, valor"""
        self.registros[reg1] = (self.registros[reg1] << valor) | (
            self.registros[reg1] >> (32 - valor)
        )
        mensaje = f"ROTACION IZQUIERDA: Registro {reg1} rotado a la izquierda por {valor} posiciones"
        print(mensaje)
        self.interfaz.actualizar_consola(mensaje)

    def rotacionr(self, reg1, valor):
        """ROTACION DERECHA R1, valor"""
        self.registros[reg1] = (self.registros[reg1] >> valor) | (
            self.registros[reg1] << (32 - valor)
        )
        mensaje = f"ROTACION DERECHA: Registro {reg1} rotado a la derecha por {valor} posiciones"
        print(mensaje)
        self.interfaz.actualizar_consola(mensaje)

    """-------------------------------
    OPERACIONES DE SALTO
    ----------------------------------"""

    def saltar_si_cero(self, direccion):
        """SALTAR SI CERO M[valor]"""
        if self.bandera_zero == 1:
            self.pc = direccion - 1
            mensaje = f"SALTAR SI CERO: Saltando a dirección {direccion} porque bandera zero está activa"
            print(mensaje)
            self.interfaz.actualizar_consola(mensaje)

    def saltar_si_positivo(self, direccion):
        """SALTAR SI POSITIVO M[valor]"""
        if self.bandera_neg == 0:
            self.pc = direccion - 1
            mensaje = f"SALTAR SI POSITIVO: Saltando a dirección {direccion} porque bandera negativo no está activa"
            print(mensaje)
            self.interfaz.actualizar_consola(mensaje)

    def saltar_si_negativo(self, direccion):
        """SALTAR SI NEGATIVO M[valor]"""
        if self.bandera_neg == 1:
            self.pc = direccion - 1
            mensaje = f"SALTAR SI NEGATIVO: Saltando a dirección {direccion} porque bandera negativo está activa"
            print(mensaje)
            self.interfaz.actualizar_consola(mensaje)

    def saltar_si_par(self, direccion):
        """SALTAR SI PAR M[valor]"""
        if self.bandera_par == 1:
            self.pc = direccion - 1
            mensaje = f"SALTAR SI PAR: Saltando a dirección {direccion} porque bandera par está activa"
            print(mensaje)
            self.interfaz.actualizar_consola(mensaje)

    def saltar_si_carry(self, direccion):
        """SALTAR SI CARRY M[valor]"""
        if self.bandera_carry == 1:
            self.pc = direccion - 1
            mensaje = f"SALTAR SI CARRY: Saltando a dirección {direccion} porque bandera carry está activa"
            print(mensaje)
            self.interfaz.actualizar_consola(mensaje)

    def saltar_si_desbordamiento(self, direccion):
        """SALTAR SI DESBORDAMIENTO M[valor]"""
        if self.bandera_desb == 1:
            self.pc = direccion - 1
            mensaje = f"SALTAR SI DESBORDAMIENTO: Saltando a dirección {direccion} porque bandera desbordamiento está activa"
            print(mensaje)
            self.interfaz.actualizar_consola(mensaje)

    def saltar(self, direccion):
        """SALTAR M[valor]"""
        self.pc = direccion - 1
        mensaje = f"SALTAR: Saltando a dirección {direccion}"
        print(mensaje)
        self.interfaz.actualizar_consola(mensaje)

    def saltar_si_no_desbordamiento(self, direccion):
        """SALTAR SI NO DESBORDAMIENTO M[valor]"""
        if self.bandera_desb == 0:
            self.pc = direccion - 1
            mensaje = f"SALTAR SI NO DESBORDAMIENTO: Saltando a dirección {direccion} porque bandera desbordamiento no está activa"
            print(mensaje)
            self.interfaz.actualizar_consola(mensaje)

    """-----------------------------------------------------------------
    OPERACIONES ENTRE REGISTROS R1 Y R2 CON ACTUALIZACIÓN DE BANDERAS
    ----------------------------------------------------------------------"""

    def or_(self, reg1, reg2):
        """OR R1, R2"""
        self.registros[reg1] = self.registros[reg1] | self.registros[reg2]
        mensaje = f"OR: Registro {reg1} OR con Registro {reg2}"
        print(mensaje)
        self.interfaz.actualizar_consola(mensaje)

    def and_(self, reg1, reg2):
        """AND R1, R2"""
        self.registros[reg1] = self.registros[reg1] & self.registros[reg2]
        mensaje = f"AND: Registro {reg1} AND con Registro {reg2}"
        print(mensaje)
        self.interfaz.actualizar_consola(mensaje)

    def xor_(self, reg1, reg2):
        """XOR R1, R2"""
        self.registros[reg1] = self.registros[reg1] ^ self.registros[reg2]
        mensaje = f"XOR: Registro {reg1} XOR con Registro {reg2}"
        print(mensaje)
        self.interfaz.actualizar_consola(mensaje)

    def not_(self, reg1):
        """NOT R1"""
        self.registros[reg1] = ~self.registros[reg1]
        mensaje = f"NOT: Registro {reg1} negado"
        print(mensaje)
        self.interfaz.actualizar_consola(mensaje)

    def sumar(self, reg1, reg2):
        """SUMAR R1, R2"""
        resultado = self.registros[reg1] + self.registros[reg2]
        self.bandera_carry = 1 if resultado > 0xFFFFFFFF else 0
        # Esto permite que la bandera de desbordamiento se active si el resultado es inconsistente
        self.bandera_desb = 1 if resultado > 0xFFFFFFFF else 0
        self.bandera_par = 1 if resultado % 2 == 0 else 0
        self.bandera_neg = 1 if resultado < 0 else 0
        self.bandera_zero = 1 if resultado == 0 else 0
        if (
            self.registros[reg1] > 0 and self.registros[reg2] > 0 and resultado < 0
        ) or (self.registros[reg1] < 0 and self.registros[reg2] < 0 and resultado >= 0):
            self.bandera_desb = 1
        self.registros[reg1] = (
            resultado & 0xFFFFFFFF
        )  # Solo se almacenan los 32 bits menos significativos
        mensaje = f"SUMAR: Registro {reg1} sumado con Registro {reg2}, resultado {self.registros[reg1]}"
        print(mensaje)
        self.interfaz.actualizar_consola(mensaje)

    def restar(self, reg1, reg2):
        """RESTAR R1, R2"""
        resultado = self.registros[reg1] - self.registros[reg2]
        self.bandera_carry = 1 if resultado < 0 else 0
        # Esto permite que la bandera de desbordamiento se active si el resultado es inconsistente
        self.bandera_par = 1 if resultado % 2 == 0 else 0
        self.bandera_neg = 1 if resultado < 0 else 0
        self.bandera_zero = 1 if resultado == 0 else 0
        if (
            self.registros[reg1] > 0 and self.registros[reg2] > 0 and resultado < 0
        ) or (self.registros[reg1] < 0 and self.registros[reg2] < 0 and resultado >= 0):
            self.bandera_desb = 1
        self.registros[reg1] = resultado & 0xFFFFFFFF
        mensaje = f"RESTAR: Registro {reg1} restado con Registro {reg2}, resultado {self.registros[reg1]} "
        print(mensaje)
        self.interfaz.actualizar_consola(mensaje)

    def multiplicar(self, reg1, reg2):
        """MULT R1, R2"""
        resultado = self.registros[reg1] * self.registros[reg2]
        self.bandera_carry = 1 if resultado > 0xFFFFFFFF else 0
        self.bandera_zero = 1 if resultado == 0 else 0
        self.bandera_par = 1 if resultado % 2 == 0 else 0
        self.bandera_neg = 1 if resultado < 0 else 0
        if (
            self.registros[reg1] > 0 and self.registros[reg2] > 0 and resultado < 0
        ) or (self.registros[reg1] < 0 and self.registros[reg2] < 0 and resultado >= 0):
            self.bandera_desb = 1
        self.registros[reg1] = resultado & 0xFFFFFFFF
        mensaje = f"MULTIPLICAR: Registro {reg1} multiplicado con Registro {reg2}, resultado {self.registros[reg1]}"
        print(mensaje)
        self.interfaz.actualizar_consola(mensaje)

    def dividir(self, reg1, reg2):
        """DIV R1, R2"""
        if self.registros[reg2] == 0:
            mensaje = (
                f"Error: División por cero en la operación DIV entre R{reg1} y R{reg2}"
            )
            print(mensaje)
            self.interfaz.actualizar_consola(mensaje, color="red")
            return

        cociente = self.registros[reg1] // self.registros[reg2]
        residuo = self.registros[reg1] % self.registros[reg2]

        self.bandera_carry = 1 if cociente > 0xFFFFFFFF else 0
        self.bandera_zero = 1 if cociente == 0 else 0
        self.bandera_par = 1 if cociente % 2 == 0 else 0
        self.bandera_neg = 1 if cociente < 0 else 0
        if (self.registros[reg1] > 0 and self.registros[reg2] > 0 and cociente < 0) or (
            self.registros[reg1] < 0 and self.registros[reg2] < 0 and cociente >= 0
        ):
            self.bandera_desb = 1

        self.registros[reg1] = cociente & 0xFFFFFFFF
        self.registros[reg2] = residuo & 0xFFFFFFFF
        mensaje = f"DIVIDIR: Registro {reg1} dividido por Registro {reg2}, cociente {self.registros[reg1]}, residuo {self.registros[reg2]}"
        print(mensaje)
        self.interfaz.actualizar_consola(mensaje)

    def copiar(self, reg1, reg2):
        """COPIAR R1, R2"""
        self.registros[reg2] = self.registros[reg1]
        mensaje = f"COPIAR: Registro {reg1} copiado a Registro {reg2}"
        print(mensaje)
        self.interfaz.actualizar_consola(mensaje)

    def comparar(self, reg1, reg2):
        """COMP R1, R2"""
        resultado = self.registros[reg1] - self.registros[reg2]
        self.bandera_zero = 1 if resultado == 0 else 0
        self.bandera_neg = 1 if resultado < 0 else 0
        self.bandera_carry = 1 if resultado < 0 else 0
        mensaje = f"COMPARAR: Registro {reg1} comparado con Registro {reg2}, resultado {resultado}"
        print(mensaje)
        self.interfaz.actualizar_consola(mensaje)

    def intercambiar(self, reg1, reg2):
        """INTERCAMBIAR R1, R2"""
        self.registros[reg1], self.registros[reg2] = (
            self.registros[reg2],
            self.registros[reg1],
        )
        mensaje = f"INTERCAMBIAR: Registro {reg1} intercambiado con Registro {reg2}"
        print(mensaje)
        self.interfaz.actualizar_consola(mensaje)

    def modulo(self, reg1, reg2):
        """MOD R1, R2"""
        if self.registros[reg2] == 0:
            mensaje = (
                f"Error: División por cero en la operación MOD entre R{reg1} y R{reg2}"
            )
            print(mensaje)
            self.interfaz.actualizar_consola(mensaje, color="red")
            return
        resultado = self.registros[reg1] % self.registros[reg2]
        self.bandera_carry = 1 if resultado > 0xFFFFFFFF else 0
        self.bandera_zero = 1 if resultado == 0 else 0
        self.bandera_par = 1 if resultado % 2 == 0 else 0
        self.bandera_neg = 1 if resultado < 0 else 0
        self.registros[reg1] = resultado & 0xFFFFFFFF
        mensaje = f"MODULO: Registro {reg1} módulo Registro {reg2}, resultado {self.registros[reg1]}"
        print(mensaje)
        self.interfaz.actualizar_consola(mensaje)

    """
    IMPRIMIR ESTADO DEL COMPUTADOR A TRAVÉS DEL CUAL SE PUEDEN INTERPRETAR RESULTADOS
    """

    def imprimir_estado(self, direccion_inicio=0, programa=[]):
        """Imprime el estado actual de DREAMCHASER"""
        print("Registros:", self.registros)
        print(
            "------------------------------------------------------------\n"
            "Banderas:\n"
        )
        print("Bandera Carry:", self.bandera_carry)
        print("Bandera Zero:", self.bandera_zero)
        print("Bandera Negativo:", self.bandera_neg)
        print("Bandera Par:", self.bandera_par)
        print("Bandera Desbordamiento:", self.bandera_desb)
        print("------------------------------------------------------------\n")
        print("------------------------------------------------------------\n")
        print(
            f"A continuación se muestran las primeras 16 instrucciones del programa en la memoria del computador"
        )

        print(
            "Memoria:", self.memoria[direccion_inicio : direccion_inicio + 16]
        )  # Solo las primeras 16 celdas
        print("------------------------------------------------------------\n")
        print("------------------------------------------------------------\n")
        print(
            "A continuación se muestran las siguientes 16 instrucciones luego de la agregar las instrucciones al computador, deben corresponder con el espacio en el que se modifiquen instrucciones"
        )
        print("Memoria:", self.memoria[len(programa) : len(programa) + 16])
        print("------------------------------------------------------------\n")
        print()


# A. Euclides
# Crear una instancia de la computadora
comp = Computadora()
