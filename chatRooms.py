import sys
import random
import utilities
import socket
from PyQt5 import QtWidgets, uic
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

#lists

users = []
chatrooms = []

app = QtWidgets.QApplication([])

loginWindow = uic.loadUi("Login.ui")
mainWindow = uic.loadUi("MainWindow.ui")
errorWindow = uic.loadUi("error.ui")
createChatRoom = uic.loadUi("createChatRoom.ui")

username = ""

def gui_login():
    global username
    username = loginWindow.lineEdit.text()
    password = loginWindow.lineEdit_2.text()

    print("username: " + username + " password: " + password)

    msg = "auth|"
    msg = msg + username + "|" + password + "\0"
    msg = utilities.cifrar(msg)

    print("Enviando: %s " % (msg))
    s.send(msg.encode())

    data = s.recv(1024)
    data = utilities.cifrar(data.decode())
    print(data)

    if len(username) == 0 or len(password) == 0:
        loginWindow.label_5.setText("Please enter data on all fields")
    elif "Denied" in data:
        gui_error()
    else:
        gui_entrar()

def gui_entrar():
    global username
    loginWindow.hide()
    mainWindow.show()

    mainWindow.label_Nickname.setText("Welcome " + username + " !")

    ##  Area 1 (Users)
    # Acceder al área de desplazamiento y al widget contenedor
    scroll_area = mainWindow.scrollArea
    scroll_content_widget = mainWindow.scrollAreaWidgetContents

    # Crear un layout vertical para el widget contenedor
    layout = QVBoxLayout(scroll_content_widget)

    # Ejemplo de agregar elementos dinámicamente
    for i in range(10):
        label = QLabel(f"User {i}")
        layout.addWidget(label)
        

    ##  Area 2 (Current chatrooms)
    scroll_area_2 = mainWindow.scrollArea_2
    scroll_content_widget_2 = mainWindow.scrollAreaWidgetContents_2

    # Crear un layout vertical para el widget contenedor
    layout = QVBoxLayout(scroll_content_widget_2)

    # Ejemplo de agregar elementos dinámicamente
    for i in range(10):
        label = QLabel(f"Chat Room {i}")
        button = QPushButton(f"Join {i}")
        layout.addWidget(label)
        layout.addWidget(button)


    ##  Area 3 (Current chatrooms)
    scroll_area_3 = mainWindow.scrollArea_3
    scroll_content_widget_3 = mainWindow.scrollAreaWidgetContents_3

    # Crear un layout vertical para el widget contenedor
    layout = QVBoxLayout(scroll_content_widget_3)

    # Ejemplo de agregar elementos dinámicamente
    for i in range(10):
        label = QLabel(f"Chat Room {i}")
        button = QPushButton(f"Join to {i}")
        layout.addWidget(label)
        layout.addWidget(button)

    ##

def gui_error():
    loginWindow.hide()
    errorWindow.show()

def return_to_login():
    mainWindow.hide()
    loginWindow.show()

def return_to_login_from_error():
    errorWindow.hide()
    loginWindow.show()

def createChatRoom_to_mainWindow():
    createChatRoom.hide()
    mainWindow.show()

def mainWindow_to_createChatRoom():
    mainWindow.hide()
    createChatRoom.show()

def CreateChatRoom():
    chatRoomName = createChatRoom.lineEdit.text()
    createChatRoom.creationMessage.setText("Chat room " + chatRoomName + " created successfuly!!")

def close():
    app.exit()
   
#   Funcionalidad botones

loginWindow.pushButton.clicked.connect(gui_login)
loginWindow.pushButton_2.clicked.connect(close)
mainWindow.button_createChatRoom.clicked.connect(mainWindow_to_createChatRoom)
mainWindow.button_logOut.clicked.connect(return_to_login)
errorWindow.pushButton.clicked.connect(return_to_login_from_error)
createChatRoom.button_returnButton.clicked.connect(createChatRoom_to_mainWindow)
createChatRoom.button_createButton.clicked.connect(CreateChatRoom)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    loginWindow.show()
    app.exec()