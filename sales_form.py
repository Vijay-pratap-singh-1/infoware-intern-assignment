from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QMessageBox
)
from db.database import get_connection

class SalesForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales Form")
        self.setFixedSize(400, 400)

        layout = QVBoxLayout()

        self.product_input = QLineEdit()
        self.customer_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.unit_input = QComboBox()
        self.unit_input.addItems(["Piece", "Kg", "Liter", "Pack", "Box"])
        self.rate_input = QLineEdit()
        self.tax_input = QLineEdit()
        self.total_label = QLabel("Total Rate: ₹0.00")

        calc_button = QPushButton("Calculate Total")
        calc_button.clicked.connect(self.calculate_total)

        save_button = QPushButton("Save Sale")
        save_button.clicked.connect(self.save_sale)

        layout.addWidget(QLabel("Product Name:")); layout.addWidget(self.product_input)
        layout.addWidget(QLabel("Customer Name:")); layout.addWidget(self.customer_input)
        layout.addWidget(QLabel("Quantity:")); layout.addWidget(self.quantity_input)
        layout.addWidget(QLabel("Unit of Measurement:")); layout.addWidget(self.unit_input)
        layout.addWidget(QLabel("Rate Per Unit:")); layout.addWidget(self.rate_input)
        layout.addWidget(QLabel("Tax (%):")); layout.addWidget(self.tax_input)

        layout.addWidget(calc_button)
        layout.addWidget(self.total_label)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def calculate_total(self):
        try:
            quantity = float(self.quantity_input.text())
            rate = float(self.rate_input.text())
            tax = float(self.tax_input.text())
            total = quantity * rate
            total_with_tax = total + (total * tax / 100)
            self.total_label.setText(f"Total Rate: ₹{total_with_tax:.2f}")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers.")

    def save_sale(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sales (
                    product_name, customer_name, quantity, unit,
                    rate, tax
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                self.product_input.text(),
                self.customer_input.text(),
                float(self.quantity_input.text()),
                self.unit_input.currentText(),
                float(self.rate_input.text()),
                float(self.tax_input.text())
            ))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Sale saved successfully.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
