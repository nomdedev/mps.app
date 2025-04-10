from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from mps.controllers.inventario_controller import InventarioController
from mps.ui.ventana_con_estilo import VentanaConEstilo

class AgregarMaterialDialog(VentanaConEstilo):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 200)

        # Layout principal
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header con botón de cerrar
        header = QHBoxLayout()
        close_button = QPushButton("X")
        close_button.setStyleSheet("color: red; font-weight: bold;")
        close_button.clicked.connect(self.reject)
        header.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addLayout(header)

        # Campo para código
        self.codigo_input = QLineEdit()
        self.codigo_input.setPlaceholderText("Código")
        layout.addWidget(QLabel("Código:"))
        layout.addWidget(self.codigo_input)

        # Campo para descripción
        self.descripcion_input = QLineEdit()
        self.descripcion_input.setPlaceholderText("Descripción")
        layout.addWidget(QLabel("Descripción:"))
        layout.addWidget(self.descripcion_input)

        # Campo para largo (en mm)
        self.largo_input = QLineEdit()
        self.largo_input.setPlaceholderText("Largo (mm)")
        layout.addWidget(QLabel("Largo (mm):"))
        layout.addWidget(self.largo_input)

        # Botones
        button_layout = QHBoxLayout()
        self.confirm_button = QPushButton("Confirmar")
        self.confirm_button.clicked.connect(self.confirmar)
        button_layout.addWidget(self.confirm_button)

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def confirmar(self):
        """
        Valida los datos ingresados y llama al controlador para agregar el material.
        """
        codigo = self.codigo_input.text().strip()
        descripcion = self.descripcion_input.text().strip()
        largo = self.largo_input.text().strip()

        if not codigo or not descripcion or not largo.isdigit():
            QMessageBox.warning(self, "Advertencia", "Todos los campos deben ser completados correctamente.")
            return

        try:
            datos_material = {
                "codigo": codigo,
                "descripcion": descripcion,
                "largo_mm": int(largo)
            }
            self.controller.agregar_material(datos_material)
            QMessageBox.information(self, "Éxito", "Material agregado correctamente.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al agregar el material: {e}")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()


class EditarMaterialDialog(VentanaConEstilo):
    def __init__(self, material):
        super().__init__()
        self.setFixedSize(400, 300)

        # Layout principal
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header con botón de cerrar
        header = QHBoxLayout()
        close_button = QPushButton("X")
        close_button.setStyleSheet("color: red; font-weight: bold;")
        close_button.clicked.connect(self.reject)
        header.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addLayout(header)

        self.codigo_input = QLineEdit(material.codigo)
        layout.addWidget(QLabel("Código:"))
        layout.addWidget(self.codigo_input)

        self.descripcion_input = QLineEdit(material.descripcion)
        layout.addWidget(QLabel("Descripción:"))
        layout.addWidget(self.descripcion_input)

        self.largo_input = QLineEdit(str(material.largo_mm))
        layout.addWidget(QLabel("Largo (mm):"))
        layout.addWidget(self.largo_input)

        self.stock_total_input = QLineEdit(str(material.stock_total))
        layout.addWidget(QLabel("Stock Total:"))
        layout.addWidget(self.stock_total_input)

        button_layout = QHBoxLayout()
        self.confirm_button = QPushButton("Confirmar")
        self.confirm_button.clicked.connect(self.confirmar)
        button_layout.addWidget(self.confirm_button)

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def confirmar(self):
        if not self.codigo_input.text() or not self.descripcion_input.text() or not self.largo_input.text().isdigit() or not self.stock_total_input.text().isdigit():
            QMessageBox.warning(self, "Advertencia", "Todos los campos deben ser completados correctamente.")
            return
        self.accept()

    def obtener_datos(self):
        return {
            "codigo": self.codigo_input.text(),
            "descripcion": self.descripcion_input.text(),
            "largo_mm": int(self.largo_input.text()),
            "stock_total": int(self.stock_total_input.text())
        }

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()


class MovimientoMaterialDialog(VentanaConEstilo):
    def __init__(self, tipo_movimiento):
        super().__init__()
        self.setFixedSize(400, 200)

        # Layout principal
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header con botón de cerrar
        header = QHBoxLayout()
        close_button = QPushButton("X")
        close_button.setStyleSheet("color: red; font-weight: bold;")
        close_button.clicked.connect(self.reject)
        header.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addLayout(header)

        self.cantidad_input = QLineEdit()
        self.cantidad_input.setPlaceholderText("Cantidad")
        layout.addWidget(QLabel("Cantidad:"))
        layout.addWidget(self.cantidad_input)

        if tipo_movimiento == "Apartar":
            self.obra_input = QLineEdit()
            self.obra_input.setPlaceholderText("Obra")
            layout.addWidget(QLabel("Obra:"))
            layout.addWidget(self.obra_input)

        button_layout = QHBoxLayout()
        self.confirm_button = QPushButton("Confirmar")
        self.confirm_button.clicked.connect(self.confirmar)
        button_layout.addWidget(self.confirm_button)

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def confirmar(self):
        if not self.cantidad_input.text().isdigit():
            QMessageBox.warning(self, "Advertencia", "La cantidad debe ser un número válido.")
            return
        if hasattr(self, "obra_input") and not self.obra_input.text():
            QMessageBox.warning(self, "Advertencia", "Debe especificar una obra.")
            return
        self.accept()

    def obtener_datos(self):
        datos = {"cantidad": int(self.cantidad_input.text())}
        if hasattr(self, "obra_input"):
            datos["obra"] = self.obra_input.text()
        return datos

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
