from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout
from product_master import ProductMasterForm
from goods_receiving import GoodsReceivingForm
from sales_form import SalesForm  


class DashboardWindow(QWidget):
    def __init__(self, username):  
        super().__init__()
        self.setWindowTitle(f"Dashboard - {username}")
        self.setFixedSize(300, 250)

        layout = QVBoxLayout()

        self.product_master_button = QPushButton("Product Master List")
        self.product_master_button.clicked.connect(self.open_product_master)

        self.goods_receiving_button = QPushButton("Goods Receiving Form")
        self.goods_receiving_button.clicked.connect(self.open_goods_receiving)

        self.sales_button = QPushButton("Sales Form")
        self.sales_button.clicked.connect(self.open_sales_form)

        layout.addWidget(self.product_master_button)
        layout.addWidget(self.goods_receiving_button)
        layout.addWidget(self.sales_button)

        self.setLayout(layout)


    def open_product_master(self):
        self.product_master_form = ProductMasterForm()
        self.product_master_form.show()

    def open_goods_receiving(self):
        self.goods_receiving_form = GoodsReceivingForm()
        self.goods_receiving_form.show()

    def open_sales_form(self):
        self.sales_form = SalesForm()
        self.sales_form.show()
