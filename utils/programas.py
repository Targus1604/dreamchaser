programaPrueba = """
importar 'libreria.txt'

const PI = 3.141592654
const E = 2.718281828

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
const PI = 3.141592654

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
