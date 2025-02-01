programaPrueba = """
importar 'libreria.txt'

const PI 3.141592654
const E 2.718281828
const MATERIA "LENGUAJES DE PROGRAMACIÓN"

# Definición de variables
a = 10
b = 20.5
c = 1e-3
d = verdadero
e = falso

# Operaciones aritméticas
suma = a + b
resta = a - b
multiplicacion = a * b
division = a / b
division_entera = a // b

# Operadores relacionales
igual = a == b
diferente = a != b
mayor = a > b
menor = a < b
mayor_igual = a >= b
menor_igual = a <= b

# Estructuras de control
si a > b
    retornar a
sino
    retornar b

mientras a < 100
    a = a + 1

funcion calcular_area(radio)
    retornar PI * radio * radio

# Llamada a la función
area = calcular_area(5)

# Comentario de prueba
# Este es un comentario que debe ser ignorado por el lexer
"""

programaPrueba2 = """
importar 'libreria.txt'
const PI 3.141592654

const E = 2.718281828
a_2 = 2.41e-2
calcular = verdadero

si calcular # Esto es un comentario
    a = PI * a # Se va a eliminar
sino a == 3
    a = E

funcion suma(a, b)
    retornar a + b
    
"""

programaPrueba3 = """
const PI 3.141592654
const MATERIA 'LENGUAJES DE PROGRAMACIÓN'
a  = 10
b = 20
    suma = a + b
"""

# Para enlazador cargador
codigo_entrada_enlazador = [
    "00000000000000000001000000000000",  # SALTO PARA PROBAR DIRECCIONES RELATIVAS
    "00000000000000010000000000000010",
    "00000000000000010000000000000100",
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
