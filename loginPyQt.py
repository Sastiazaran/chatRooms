import sys
import utilities
import socket
from PyQt5.QtWidgets import (
    QMainWindow,
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
data = ""
loginFlag = False
        
# Configurar la aplicación de PyQt
app = QApplication(sys.argv)

class LoginWindow(QWidget):
    def login(self):
        global username, s, data, loginFlag
        
        username = self.entry_username.text()
        password = self.entry_password.text()
        # Aquí puedes realizar la lógica de verificación del inicio de sesión

        msg = "auth|"
        msg = msg + username + "|" + password + "\0"
        msg = utilities.cifrar(msg)

        print("Enviando: %s " % (msg))
        s.send(msg.encode())

        data = s.recv(1024)
        data = utilities.cifrar(data.decode())
        print(data)

        if "Denied" in data:
            label_warning = QLabel("Invalid credentials!")
            self.layout.addWidget(label_warning)
        else:
            loginFlag = True
            self.button_login.clicked.connect(self.openMainWindow) 

                

    def __init__(self):
        global username, data, loginFlag
        super().__init__()
        
        self.setWindowTitle("Formulario de inicio de sesión")
        # Crear y colocar los widgets en la ventana usando un layout vertical
        self.layout = QVBoxLayout()

        label_username = QLabel("Usuario:")
        self.layout.addWidget(label_username)
        self.entry_username = QLineEdit()
        self.layout.addWidget(self.entry_username)

        label_password = QLabel("Contraseña:")
        self.layout.addWidget(label_password)
        self.entry_password = QLineEdit()
        self.entry_password.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.entry_password)
        self.button_login = QPushButton("Iniciar sesión")
        if loginFlag == True:
            self.button_login.clicked.connect(self.openMainWindow) 
        else:
            self.button_login.clicked.connect(self.login)
        self.layout.addWidget(self.button_login)

        self.setLayout(self.layout)

    def openMainWindow(self):
        self.newWindow = MainWindow()
        self.newWindow.show()
        self.hide()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana Principal")
        
        layout = QVBoxLayout()
        
        label = QLabel("Ventana Principal")
        layout.addWidget(label)

        label_listOfUsers = QLabel("List of users")
        layout.addWidget(label_listOfUsers)

        button_createChatRoom = QPushButton("Create a chatroom")
        button_createChatRoom.clicked.connect(self.createChatroom)

        label_requestOfBelonging = QLabel("Request of belonging:")
        layout.addWidget(label_requestOfBelonging)
        self.entry_requestOfBelonging = QLineEdit()
        layout.addWidget(self.entry_requestOfBelonging)
        
        button = QPushButton("Ir a la otra ventana")
        button.clicked.connect(self.open_new_window)
        layout.addWidget(button)
        
        self.setLayout(layout)

    def createChatroom(self):
        pass
    
    def open_new_window(self):
        self.new_window = SecondWindow()
        self.new_window.show()
        self.hide()

class SecondWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Segunda Ventana")
        
        layout = QVBoxLayout()
        
        label = QLabel("Segunda Ventana")
        layout.addWidget(label)
        
        button = QPushButton("Volver")
        button.clicked.connect(self.go_back)
        layout.addWidget(button)
        
        self.setLayout(layout)
    
    def go_back(self):
        self.parent().show()
        self.close()


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

    # Mostrar la ventana
    window = LoginWindow()
    window.show()

    # Ejecutar el bucle de eventos de la aplicación
    sys.exit(app.exec())
