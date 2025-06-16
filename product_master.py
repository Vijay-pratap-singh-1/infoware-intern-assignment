from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QComboBox, QFileDialog, QMessageBox
)
from PySide6.QtGui import QPixmap
from db.database import get_connection

class ProductMasterForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Master Form")
        self.setFixedSize(400, 500)

        layout = QVBoxLayout()

        self.barcode_input = QLineEdit()
        self.sku_input = QLineEdit()
        self.category_input = QLineEdit()
        self.subcategory_input = QLineEdit()
        self.product_name_input = QLineEdit()
        self.description_input = QTextEdit()
        self.tax_input = QLineEdit()
        self.price_input = QLineEdit()

        self.unit_input = QComboBox()
        self.unit_input.addItems(["Piece", "Kg", "Liter", "Pack", "Box"])

        self.image_label = QLabel("No Image Selected")
        self.image_path = None

        upload_button = QPushButton("Upload Image")
        upload_button.clicked.connect(self.upload_image)

        save_button = QPushButton("Save Product")
        save_button.clicked.connect(self.save_product)

        layout.addWidget(QLabel("Barcode:")); layout.addWidget(self.barcode_input)
        layout.addWidget(QLabel("SKU ID:")); layout.addWidget(self.sku_input)
        layout.addWidget(QLabel("Category:")); layout.addWidget(self.category_input)
        layout.addWidget(QLabel("Subcategory:")); layout.addWidget(self.subcategory_input)
        layout.addWidget(QLabel("Product Name:")); layout.addWidget(self.product_name_input)
        layout.addWidget(QLabel("Description:")); layout.addWidget(self.description_input)
        layout.addWidget(QLabel("Tax (%):")); layout.addWidget(self.tax_input)
        layout.addWidget(QLabel("Price:")); layout.addWidget(self.price_input)
        layout.addWidget(QLabel("Unit of Measurement:")); layout.addWidget(self.unit_input)

        layout.addWidget(self.image_label)
        layout.addWidget(upload_button)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def upload_image(self):
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg)")
        if image_path:
            self.image_path = image_path
            self.image_label.setPixmap(QPixmap(image_path).scaledToWidth(200))

    def save_product(self):
        if not all([
            self.barcode_input.text(),
            self.sku_input.text(),
            self.category_input.text(),
            self.product_name_input.text(),
            self.price_input.text()
        ]):
            QMessageBox.warning(self, "Input Error", "Please fill all required fields.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO products (
                barcode, sku_id, category, subcategory, product_name,
                description, tax, price, unit, image_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.barcode_input.text(),
            self.sku_input.text(),
            self.category_input.text(),
            self.subcategory_input.text(),
            self.product_name_input.text(),
            self.description_input.toPlainText(),
            float(self.tax_input.text()) if self.tax_input.text() else 0.0,
            float(self.price_input.text()),
            self.unit_input.currentText(),
            self.image_path or ""
        ))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Saved", "Product saved successfully.")
        self.close()
