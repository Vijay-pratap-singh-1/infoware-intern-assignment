from db.database import init_db
init_db()
from dashboard import DashboardWindow
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from db.database import get_connection
import sys

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Infoware Login")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.check_login)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM operators WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.dashboard = DashboardWindow(username)
            self.dashboard.show() 
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
