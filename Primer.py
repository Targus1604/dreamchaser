import sys
from PyQt6 import QtWidgets, uic
from analisisLexico import lexer
from preprocesador import preprocesar_codigo
from ensamblador import ensamblador
from MainWindow import Ui_MainWindow
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
from computadora import Computadora


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.Abrir.clicked.connect(self.open_file_dialog)
        self.Compilar.clicked.connect(self.analizar_codigo)
        self.Guardar.clicked.connect(self.guardar_archivo)
        self.Preprocesar.clicked.connect(self.preprocesar)
        self.Abrir_2.clicked.connect(self.open_file_dialog2)
        self.Compilar.clicked.connect(self.analizar_codigo)
        self.Guardar_2.clicked.connect(self.guardar_archivo2)
        self.Ensamblar.clicked.connect(self.ensamblar)
        self.Enlazar.clicked.connect(self.enlazar_cargar)

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

    def preprocesar(self):
        texto = self.Editor.toPlainText()

        result = preprocesar_codigo(texto)

        self.Preprocesado.setPlainText(result)

    def analizar_codigo(self):
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

        # Asignar modelo al QTableView (TablaAnalisis)
        self.TablaAnalisis.setModel(model)

    def ensamblar(self):
        codigo = self.CodigoEnsamblador.toPlainText()
        codigo_formateado = codigo.splitlines()
        codigo_ensamblado = "\n".join(ensamblador(codigo_formateado))
        self.ResultadoEnsamblador.setPlainText(codigo_ensamblado)

    def enlazar_cargar(self):
        # Obtener el código desde ResultadoEnsamblador (QPlainTextEdit)
        codigo = self.ResultadoEnsamblador.toPlainText()
        codigo_formateado = codigo.splitlines()  # Convertirlo en lista de líneas

        # Crear instancia de Computadora
        compu = Computadora()
        memoria = compu.cargar_codigo(codigo_formateado, direccion_de_inicio=3)

        # Crear modelo para la tabla
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Binario"])  # Columnas

        # Llenar la tabla con datos de memoria
        for instr in memoria:
            row = [QStandardItem(str(instr))]  # Instrucción en binario

            # Hacer cada celda de solo lectura
            for item in row:
                item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

            model.appendRow(row)

        # Asignar modelo a la tabla
        self.SalidaEnlazarCargar.setModel(model)
        # Ajustar tamaño de las columnas
        self.SalidaEnlazarCargar.setColumnWidth(0, 350)  # Columna "Dirección"


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
