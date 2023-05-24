import sys
import utilities
import socket
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 5000  # The port used by the server
token = ""
username = ""

def login():
    global username, s
    username = entry_username.text()
    password = entry_password.text()
    # Aquí puedes realizar la lógica de verificación del inicio de sesión

    msg = "auth|"
    msg = username + "|" + password + "\0"
    msg = utilities.cifrar(msg)

    print("Enviando: %s " % (msg))
    s.send(msg.encode())

    data = s.recv(1024)
    data = utilities.cifrar(data.decode())

    if "Denied" in data:
        username = ""
        return 0
    else:
        return data


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # loop = True
    # while loop:
    #     if token == "":
    #         token = login(s)
    #         print(token)
    #     if token == 0:
    #         token = ""
    #     else:
    #         utilities.group(s)
    #         loop = False

    # Configurar la aplicación de PyQt
    app = QApplication(sys.argv)

    # Crear la ventana principal
    window = QWidget()
    window.setWindowTitle("Formulario de inicio de sesión")

    # Crear y colocar los widgets en la ventana usando un layout vertical
    layout = QVBoxLayout()

    label_username = QLabel("Usuario:")
    layout.addWidget(label_username)
    entry_username = QLineEdit()
    layout.addWidget(entry_username)

    label_password = QLabel("Contraseña:")
    layout.addWidget(label_password)
    entry_password = QLineEdit()
    entry_password.setEchoMode(QLineEdit.Password)
    layout.addWidget(entry_password)

    button_login = QPushButton("Iniciar sesión")
    button_login.clicked.connect(login)
    layout.addWidget(button_login)

    window.setLayout(layout)

    # Mostrar la ventana
    window.show()

    # Ejecutar el bucle de eventos de la aplicación
    sys.exit(app.exec())
