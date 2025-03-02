import sys

from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QFileDialog, QTableWidgetItem

from analisisLexico import lexer
from computadora import Computadora
from ensamblador import ensamblador
from MainWindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.computadora = Computadora()  # Crear la instancia de Computadora aquí

        self.inicializar()

        self.Abrir.clicked.connect(self.open_file_dialog)
        self.Guardar.clicked.connect(self.guardar_archivo)
        self.Abrir_2.clicked.connect(self.open_file_dialog2)
        self.Compilar.clicked.connect(self.compilar)
        self.Guardar_2.clicked.connect(self.guardar_archivo2)
        self.Ensamblar.clicked.connect(self.ensamblar)
        self.Enlazar.clicked.connect(self.enlazar_cargar)
        self.Reiniciar.clicked.connect(self.inicializar)
        self.Sig_instruccion.clicked.connect(self.siguiente_instruccion)

    def inicializar(self):
        self.ResultadoEnsamblador.clear()
        self.CodigoEnsamblador.clear()
        # ResultadoEnsamblador QTextBrowser
        # Crear múltiples líneas de 32 ceros
        lineas = ["0" * 32 for _ in range(20)]  # Genera 10 líneas con 32 ceros cada una

        # Unir todas las líneas con saltos de línea
        contenido = "\n".join(lineas)

        # Establecer el contenido en el QTextBrowser
        self.ResultadoEnsamblador.setPlainText(contenido)

        # Tabla de REGISTROS
        self.Tabla_Registros.setRowCount(8)  # A y B
        self.Tabla_Registros.setColumnCount(2)  # Binario y Decimal
        self.actualizar_registros()

        # Tabla de INDICADORES ALU
        self.Tabla_Alu.setRowCount(5)  # C, Z, N, P, D
        self.Tabla_Alu.setColumnCount(2)  # Binario y Decimal
        self.actualizar_indicadores_alu()

        # Tabla de UNIDAD DE CONTROL
        self.Tabla_Unidad_Control.setRowCount(1)  # IC, CP
        self.Tabla_Unidad_Control.setColumnCount(1)  # Binario
        self.actualizar_unidad_control()

        # Tabla RAM
        filas = self.SalidaEnlazarCargar.rowCount()  # Obtener número de filas

        for fila in range(filas):
            # Crear un QTableWidgetItem con 32 ceros
            item_binario = QTableWidgetItem("0" * 32)

            # Hacer que la celda sea solo lectura
            item_binario.setFlags(
                Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
            )

            # Insertar el valor en la columna 0
            self.SalidaEnlazarCargar.setItem(fila, 0, item_binario)

        # Ajustar tamaño de la columna para que se vea bien
        self.SalidaEnlazarCargar.setColumnWidth(
            0, 500
        )  # Ajusta el ancho según sea necesario
        self.Tabla_Registros.resizeColumnsToContents()
        self.Tabla_Alu.resizeColumnsToContents()
        self.Tabla_Unidad_Control.resizeColumnsToContents()

    def actualizar_unidad_control(self):
        nombres_control = ["PC"]
        valores_control = [
            self.computadora.pc,
        ]

        control = [
            (
                nombre,
                str(valor),
                str(valor),
            )
            for nombre, valor in zip(nombres_control, valores_control)
        ]

        for fila, (nombre, binario, decimal) in enumerate(control):
            self.Tabla_Unidad_Control.setVerticalHeaderItem(
                fila, QTableWidgetItem(nombre)
            )
            self.Tabla_Unidad_Control.setItem(fila, 0, QTableWidgetItem(binario))

    def actualizar_registros(self):
        nombres_registros = ["A", "B", "C", "D", "E", "F", "G", "H"]
        registros = [
            (
                nombre,
                format(self.computadora.registros[i], "032b"),
                str(self.computadora.registros[i]),
            )
            for i, nombre in enumerate(nombres_registros)
        ]

        for fila, (registro, binario, decimal) in enumerate(registros):
            self.Tabla_Registros.setVerticalHeaderItem(fila, QTableWidgetItem(registro))
            self.Tabla_Registros.setItem(fila, 0, QTableWidgetItem(binario))
            self.Tabla_Registros.setItem(fila, 1, QTableWidgetItem(decimal))

    def actualizar_indicadores_alu(self):
        nombres_indicadores = ["C", "Z", "N", "P", "D"]
        valores_indicadores = [
            self.computadora.bandera_carry,
            self.computadora.bandera_zero,
            self.computadora.bandera_neg,
            self.computadora.bandera_par,
            self.computadora.bandera_desb,
        ]

        indicadores = [
            (
                nombre,
                format(valor, "03b"),
                str(valor),
            )
            for nombre, valor in zip(nombres_indicadores, valores_indicadores)
        ]

        for fila, (nombre, binario, decimal) in enumerate(indicadores):
            self.Tabla_Alu.setVerticalHeaderItem(fila, QTableWidgetItem(nombre))
            self.Tabla_Alu.setItem(fila, 0, QTableWidgetItem(binario))
            self.Tabla_Alu.setItem(fila, 1, QTableWidgetItem(decimal))

    def siguiente_instruccion(self):
        self.computadora.ejecutar_instruccion()
        self.actualizar_unidad_control()
        self.actualizar_registros()
        self.actualizar_indicadores_alu()

    def open_file_dialog(self):
        # Abrir explorador de archivos y filtrar solo archivos .txt
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo", "", "Archivos de texto (*.txt)"
        )

        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    contenido = file.read()
                    self.Editor.setPlainText(
                        contenido
                    )  # Mostrar el contenido en el QPlainTextEdit
            except Exception as e:
                print(f"Error al leer el archivo: {e}")  # Manejo de errores

    def open_file_dialog2(self):
        # Abrir explorador de archivos y filtrar solo archivos .txt
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo", "", "Archivos de texto (*.txt)"
        )

        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    contenido = file.read()
                    self.CodigoEnsamblador.setPlainText(
                        contenido
                    )  # Mostrar el contenido en el QPlainTextEdit
            except Exception as e:
                print(f"Error al leer el archivo: {e}")  # Manejo de errores

    def guardar_archivo(self):
        # Abrir explorador de archivos para guardar
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Guardar Archivo", "", "Archivos de texto (*.txt)"
        )

        # Si el usuario seleccionó un archivo, guardarlo
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(
                        self.Editor.toPlainText()
                    )  # Escribir el contenido del Editor en el archivo
                print(
                    f"Archivo guardado en: {file_path}"
                )  # Mensaje de confirmación en consola
            except Exception as e:
                print(
                    f"Error al guardar el archivo: {e}"
                )  # Mensaje de error en caso de fallo

    def guardar_archivo2(self):
        # Abrir explorador de archivos para guardar
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Guardar Archivo", "", "Archivos de texto (*.txt)"
        )

        # Si el usuario seleccionó un archivo, guardarlo
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(
                        self.CodigoEnsamblador.toPlainText()
                    )  # Escribir el contenido del Editor en el archivo
                print(
                    f"Archivo guardado en: {file_path}"
                )  # Mensaje de confirmación en consola
            except Exception as e:
                print(
                    f"Error al guardar el archivo: {e}"
                )  # Mensaje de error en caso de fallo

    def compilar(self):
        # Obtener el texto desde QPlainTextEdit (Editor)
        texto = self.Editor.toPlainText()

        # Pasar el texto al lexer
        lexer.input(texto)

        # Crear un modelo para la tabla
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(
            ["Tipo", "Valor", "Línea", "Posición"]
        )  # Columnas

        # Procesar los tokens y agregarlos a la tabla
        while True:
            token = lexer.token()
            if not token:
                break  # Terminar cuando no hay más tokens

            # Crear fila con los atributos del token
            row = [
                QStandardItem(token.type),
                QStandardItem(str(token.value)),
                QStandardItem(str(token.lineno)),
                QStandardItem(str(token.lexpos)),
            ]

            # Hacer que cada celda sea solo de lectura
            for item in row:
                item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

            model.appendRow(row)  # Agregar fila a la tabla

    def ensamblar(self):
        codigo = self.CodigoEnsamblador.toPlainText()
        codigo_formateado = codigo.splitlines()
        codigo_ensamblado = "\n".join(ensamblador(codigo_formateado)[0])
        self.ResultadoEnsamblador.setPlainText(codigo_ensamblado)

    def enlazar_cargar(self):
        # Obtener el código desde ResultadoEnsamblador (QPlainTextEdit)
        codigo = self.ResultadoEnsamblador.toPlainText()
        codigo_formateado = codigo.splitlines()  # Convertirlo en lista de líneas

        # Obtener la dirección de inicio desde QSpinBox
        direccion_inicio = self.Localizacion.value()

        self.computadora.cargar_codigo(
            codigo_formateado, direccion_de_inicio=direccion_inicio
        )

        # Obtener memoria cargada
        memoria = self.computadora.mostrar_memoria()
        # Limpiar la tabla antes de agregar nuevos datos
        # self.SalidaEnlazarCargar.clearContents()
        # self.SalidaEnlazarCargar.setRowCount(0)

        self.SalidaEnlazarCargar.setRowCount(1024)

        # No limpiar toda la tabla, solo actualizar las filas necesarias
        for direccion, instr in memoria:
            fila = int(
                direccion
            )  # Convertir dirección en entero (asumiendo formato hexadecimal)

            if 0 <= fila < self.SalidaEnlazarCargar.rowCount():
                item_binario = QTableWidgetItem(str(instr))
                item_binario.setTextAlignment(
                    Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
                )
                item_binario.setFlags(
                    Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
                )
                self.SalidaEnlazarCargar.setItem(
                    fila, 0, item_binario
                )  # Agregar el valor en la posición correcta

        # Ajustar tamaño de la columna
        # self.SalidaEnlazarCargar.setColumnWidth(0, 500)  # Ajusta según sea necesario
        self.SalidaEnlazarCargar.resizeColumnsToContents()  # Ajusta el ancho según el contenido


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.computadora.interfaz = window
window.show()
app.exec()
