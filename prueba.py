import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout

# Configurar la aplicación de PyQt
app = QApplication(sys.argv)

# Crear la ventana principal
class LoginForm(QWidget):
    def login(self):
        username = self.entry_username.text()
        password = self.entry_password.text()
        # Aquí puedes realizar la lógica de verificación del inicio de sesión
        
        # Ejemplo: Verificar si el usuario y la contraseña son válidos
        if username == "usuario" and password == "contraseña":
            print("Inicio de sesión exitoso")
        else:
            print("Inicio de sesión fallido")


    def __init__(self):
        super().__init__()
        self.setWindowTitle("Formulario de inicio de sesión")
        
        layout = QVBoxLayout()
        
        label_username = QLabel("Usuario:")
        layout.addWidget(label_username)
        self.entry_username = QLineEdit()
        layout.addWidget(self.entry_username)
        
        label_password = QLabel("Contraseña:")
        layout.addWidget(label_password)
        self.entry_password = QLineEdit()
        self.entry_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.entry_password)
        
        self.button_login = QPushButton("Iniciar sesión")
        self.button_login.clicked.connect(self.login)
        layout.addWidget(self.button_login)
        
        self.setLayout(layout)

# Crear una instancia del formulario de inicio de sesión
login_form = LoginForm()

# Mostrar el formulario de inicio de sesión
login_form.show()

# Ejecutar el bucle de eventos de la aplicación
sys.exit(app.exec())
