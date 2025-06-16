from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QHBoxLayout, QMessageBox
)
from db.database import get_connection

class GoodsReceivingForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Goods Receiving")
        self.setFixedSize(400, 400)

        layout = QVBoxLayout()

        self.product_dropdown = QComboBox()
        self.load_products()

        self.supplier_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.unit_input = QComboBox()
        self.unit_input.addItems(["Piece", "Kg", "Liter", "Pack", "Box"])
        self.rate_input = QLineEdit()
        self.tax_input = QLineEdit()
        self.total_display = QLabel("Total: ₹0.00")

        calc_button = QPushButton("Calculate Total")
        calc_button.clicked.connect(self.calculate_total)

        save_button = QPushButton("Save Entry")
        save_button.clicked.connect(self.save_entry)

        layout.addWidget(QLabel("Select Product:")); layout.addWidget(self.product_dropdown)
        layout.addWidget(QLabel("Supplier Name:")); layout.addWidget(self.supplier_input)
        layout.addWidget(QLabel("Quantity:")); layout.addWidget(self.quantity_input)
        layout.addWidget(QLabel("Unit:")); layout.addWidget(self.unit_input)
        layout.addWidget(QLabel("Rate per Unit:")); layout.addWidget(self.rate_input)
        layout.addWidget(QLabel("Tax %:")); layout.addWidget(self.tax_input)
        layout.addWidget(calc_button)
        layout.addWidget(self.total_display)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def load_products(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT product_name FROM product_master")
        products = cursor.fetchall()
        self.product_dropdown.addItems([p[0] for p in products])
        conn.close()

    def calculate_total(self):
        try:
            qty = float(self.quantity_input.text())
            rate = float(self.rate_input.text())
            tax = float(self.tax_input.text())
            subtotal = qty * rate
            total = subtotal + (subtotal * tax / 100)
            self.total_display.setText(f"Total: ₹{total:.2f}")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers.")

    def save_entry(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO goods_receiving (product_name, supplier_name, quantity, unit, rate, tax)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            self.product_dropdown.currentText(),
            self.supplier_input.text(),
            float(self.quantity_input.text()),
            self.unit_input.currentText(),
            float(self.rate_input.text()),
            float(self.tax_input.text())
        ))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Saved", "Goods entry saved.")
        self.close()
