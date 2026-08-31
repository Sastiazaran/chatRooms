#!/usr/bin/env python3
"""Chatbook desktop client — PyQt5 UI talking to the C TCP server."""

import os
import sys
import socket

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

import utilities

HOST = os.environ.get("CHATBOOK_HOST", "127.0.0.1")
PORT = int(os.environ.get("CHATBOOK_PORT", "5000"))
ENCODING = "latin-1"


split_names = utilities.split_names
format_chat_html = utilities.format_chat_html


def clear_container(container):
    """Replace any leftover designer widgets with a clean vertical layout."""
    old = container.layout()
    if old is not None:
        while old.count():
            item = old.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.hide()
                widget.setParent(None)
                widget.deleteLater()
        return old

    for child in list(container.children()):
        if isinstance(child, QWidget) and child is not container:
            child.hide()
            child.setParent(None)
            child.deleteLater()

    layout = QVBoxLayout(container)
    layout.setContentsMargins(6, 6, 6, 6)
    layout.setSpacing(6)
    layout.setAlignment(Qt.AlignTop)
    return layout


def add_row(layout, widget):
    layout.addWidget(widget)


class ChatClient:
    def __init__(self, sock):
        self.sock = sock

    def request(self, message):
        payload = utilities.cifrar(message)
        self.sock.sendall(payload.encode(ENCODING))
        data = self.sock.recv(65536)
        if not data:
            raise ConnectionError("Server closed the connection")
        return utilities.cifrar(data.decode(ENCODING))


class ChatbookApp:
    def __init__(self, client):
        self.client = client
        self.username = ""
        self.current_room = ""
        self.users = []
        self.user_chatrooms = []
        self.all_chatrooms = []
        self.admin_rooms = []
        self.admin_mode = False

        self.login_window = uic.loadUi("Login.ui")
        self.main_window = uic.loadUi("MainWindow.ui")
        self.error_window = uic.loadUi("error.ui")
        self.create_window = uic.loadUi("createChatRoom.ui")
        self.admin_window = uic.loadUi("MainWindowAdmin.ui")
        self.register_window = uic.loadUi("Register.ui")

        for window in (
            self.login_window,
            self.main_window,
            self.error_window,
            self.create_window,
            self.admin_window,
            self.register_window,
        ):
            window.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self._wire_signals()

    def _wire_signals(self):
        self.login_window.pushButton.clicked.connect(self.gui_login)
        self.login_window.pushButton_2.clicked.connect(self.close)
        self.login_window.pushButton_3.clicked.connect(self.show_register)
        self.login_window.lineEdit.returnPressed.connect(self.gui_login)
        self.login_window.lineEdit_2.returnPressed.connect(self.gui_login)

        self.main_window.button_createChatRoom.clicked.connect(self.show_create_room)
        self.main_window.button_logOut.clicked.connect(self.return_to_login)
        self.main_window.button_send.clicked.connect(self.send_message)
        self.main_window.button_Admin.clicked.connect(self.show_admin)
        self.main_window.lineEdit.returnPressed.connect(self.send_message)

        self.error_window.pushButton.clicked.connect(self.return_to_login_from_error)

        self.create_window.button_returnButton.clicked.connect(self.create_to_main)
        self.create_window.button_createButton.clicked.connect(self.create_chat_room)
        self.create_window.lineEdit.returnPressed.connect(self.create_chat_room)

        self.admin_window.button_createChatRoom.clicked.connect(self.show_create_room)
        self.admin_window.button_logOut.clicked.connect(self.return_to_login)
        self.admin_window.button_send.clicked.connect(self.send_message)
        self.admin_window.lineEdit.returnPressed.connect(self.send_message)

        self.register_window.pushButton_3.clicked.connect(self.submit_register)
        self.register_window.pushButton.clicked.connect(self.register_to_login)
        self.register_window.pushButton_2.clicked.connect(self.close)
        self.register_window.lineEdit.returnPressed.connect(self.submit_register)
        self.register_window.lineEdit_2.returnPressed.connect(self.submit_register)

    def _active_window(self):
        return self.admin_window if self.admin_mode else self.main_window

    def refresh_data(self):
        self.users = split_names(self.client.request("getUsers|"))
        self.all_chatrooms = split_names(self.client.request("getAllChatrooms|"))
        self.user_chatrooms = split_names(
            self.client.request("getUserChatrooms|" + self.username)
        )
        self.admin_rooms = split_names(
            self.client.request("getAdminChat|" + self.username)
        )

    def populate_sidebar(self, window, show_add_buttons=False):
        people = clear_container(window.scrollAreaWidgetContents)
        rooms = clear_container(window.scrollAreaWidgetContents_2)
        all_rooms = clear_container(window.scrollAreaWidgetContents_3)

        if not self.users:
            empty = QLabel("No other users yet")
            empty.setStyleSheet("color:#6b7280;")
            add_row(people, empty)
        for name in self.users:
            if show_add_buttons:
                row = QWidget()
                row_layout = QHBoxLayout(row)
                row_layout.setContentsMargins(0, 0, 0, 0)
                label = QLabel(name)
                add_btn = QPushButton("Add")
                add_btn.setCursor(Qt.PointingHandCursor)
                add_btn.clicked.connect(lambda _, user=name: self.add_user_to_room(user))
                row_layout.addWidget(label, 1)
                row_layout.addWidget(add_btn)
                add_row(people, row)
            else:
                label = QLabel("●  " + name)
                label.setStyleSheet("color:#1c1c28; padding:4px;")
                add_row(people, label)

        if not self.user_chatrooms:
            empty = QLabel("You have not joined a room yet")
            empty.setWordWrap(True)
            empty.setStyleSheet("color:#6b7280;")
            add_row(rooms, empty)
        for room in self.user_chatrooms:
            button = QPushButton(room)
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(lambda _, name=room: self.open_chat(name))
            add_row(rooms, button)

        if not self.all_chatrooms:
            empty = QLabel("No rooms have been created")
            empty.setWordWrap(True)
            empty.setStyleSheet("color:#6b7280;")
            add_row(all_rooms, empty)
        for room in self.all_chatrooms:
            joined = room in self.user_chatrooms
            button = QPushButton("Open " + room if joined else "Join " + room)
            button.setCursor(Qt.PointingHandCursor)
            if joined:
                button.clicked.connect(lambda _, name=room: self.open_chat(name))
            else:
                button.clicked.connect(lambda _, name=room: self.join_room(name))
            add_row(all_rooms, button)

    def populate_members(self):
        container = self.admin_window.scrollAreaWidgetContents_4
        layout = clear_container(container)
        if not self.current_room:
            hint = QLabel("Open a room to manage its members.")
            hint.setWordWrap(True)
            hint.setStyleSheet("color:#6b7280; padding:8px;")
            add_row(layout, hint)
            return

        members = split_names(self.client.request("getChatUsers|" + self.current_room))
        if not members:
            hint = QLabel("This room has no members yet.")
            hint.setWordWrap(True)
            hint.setStyleSheet("color:#6b7280; padding:8px;")
            add_row(layout, hint)
            return

        for member in members:
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            label = QLabel(member)
            kick = QPushButton("Remove")
            kick.setCursor(Qt.PointingHandCursor)
            kick.setStyleSheet("background-color:#ffe5e5; color:#e5484d;")
            kick.clicked.connect(lambda _, user=member: self.remove_user_from_room(user))
            row_layout.addWidget(label, 1)
            row_layout.addWidget(kick)
            add_row(layout, row)

    def show_chat(self, raw):
        html_body = format_chat_html(raw, self.username)
        self.main_window.label_2.setHtml(html_body)
        self.admin_window.label_2.setHtml(html_body)
        title = self.current_room if self.current_room else "Select a room to start chatting"
        self.main_window.label_chat.setText(title)
        self.admin_window.label_chat.setText(title)

    def open_chat(self, room):
        if not room:
            return
        self.current_room = room
        raw = self.client.request("getChat|" + room)
        self.show_chat(raw)
        if self.admin_mode:
            self.populate_members()

    def join_room(self, room):
        response = self.client.request("addUser|" + self.username + "|" + room)
        if response.startswith("Error"):
            QMessageBox.warning(self._active_window(), "Chatbook", response)
            return
        self.refresh_data()
        self.populate_sidebar(self._active_window(), show_add_buttons=self.admin_mode)
        self.open_chat(room)

    def add_user_to_room(self, user):
        if not self.current_room:
            QMessageBox.information(
                self.admin_window, "Chatbook", "Open a room first, then add people to it."
            )
            return
        response = self.client.request("addUser|" + user + "|" + self.current_room)
        if response.startswith("Error"):
            QMessageBox.warning(self.admin_window, "Chatbook", response)
            return
        self.refresh_data()
        self.populate_sidebar(self.admin_window, show_add_buttons=True)
        self.populate_members()

    def remove_user_from_room(self, user):
        if not self.current_room:
            return
        response = self.client.request("deleteUser|" + user + "|" + self.current_room)
        if response.startswith("Error"):
            QMessageBox.warning(self.admin_window, "Chatbook", response)
            return
        self.refresh_data()
        self.populate_sidebar(self.admin_window, show_add_buttons=True)
        self.populate_members()

    def enter_main(self):
        self.admin_mode = False
        self.login_window.hide()
        self.register_window.hide()
        self.create_window.hide()
        self.admin_window.hide()
        self.error_window.hide()
        self.main_window.show()
        self.main_window.label_Nickname.setText("Welcome, " + self.username)
        self.refresh_data()
        self.populate_sidebar(self.main_window)
        if self.current_room:
            self.open_chat(self.current_room)
        else:
            self.show_chat("")

    def gui_login(self):
        username = self.login_window.lineEdit.text().strip()
        password = self.login_window.lineEdit_2.text()
        if not username or not password:
            self.login_window.label_5.setText("Please fill in both fields")
            return

        try:
            data = self.client.request("auth|" + username + "|" + password)
        except OSError as exc:
            QMessageBox.critical(self.login_window, "Chatbook", str(exc))
            return

        if "Denied" in data:
            self.gui_error()
            return

        self.username = username
        self.current_room = ""
        self.login_window.label_5.setText("")
        self.enter_main()

    def gui_error(self):
        self.login_window.hide()
        self.error_window.show()

    def return_to_login(self):
        self.admin_mode = False
        self.username = ""
        self.current_room = ""
        self.main_window.hide()
        self.admin_window.hide()
        self.create_window.hide()
        self.login_window.lineEdit_2.clear()
        self.login_window.label_5.setText("")
        self.login_window.show()

    def return_to_login_from_error(self):
        self.error_window.hide()
        self.login_window.show()

    def show_register(self):
        self.login_window.hide()
        self.register_window.label_5.setText("")
        self.register_window.lineEdit.clear()
        self.register_window.lineEdit_2.clear()
        self.register_window.show()

    def register_to_login(self):
        self.register_window.hide()
        self.login_window.show()

    def submit_register(self):
        username = self.register_window.lineEdit.text().strip()
        password = self.register_window.lineEdit_2.text()
        if not username or not password:
            self.register_window.label_5.setText("Please fill in both fields")
            return
        try:
            data = self.client.request("registrarUsuario|" + username + "|" + password)
        except OSError as exc:
            QMessageBox.critical(self.register_window, "Chatbook", str(exc))
            return

        if data.startswith("Error"):
            self.register_window.label_5.setStyleSheet("color:#e5484d; font-weight:600;")
            self.register_window.label_5.setText(data.split("|", 1)[-1])
            return

        self.register_window.hide()
        self.login_window.lineEdit.setText(username)
        self.login_window.lineEdit_2.clear()
        self.login_window.label_5.setStyleSheet("color:#30a46c; font-weight:600;")
        self.login_window.label_5.setText("Account created. You can sign in now.")
        self.login_window.show()

    def show_create_room(self):
        self.main_window.hide()
        self.admin_window.hide()
        self.create_window.lineEdit.clear()
        self.create_window.creationMessage.setText("")
        self.create_window.creationMessage_2.setText("")
        self.create_window.show()

    def create_to_main(self):
        self.create_window.hide()
        if self.admin_mode:
            self.show_admin()
        else:
            self.enter_main()

    def create_chat_room(self):
        name = self.create_window.lineEdit.text().strip()
        self.create_window.creationMessage.setText("")
        self.create_window.creationMessage_2.setText("")
        if not name:
            self.create_window.creationMessage_2.setText("Please enter a room name")
            return
        try:
            data = self.client.request("createChatRoom|" + self.username + "|" + name)
        except OSError as exc:
            QMessageBox.critical(self.create_window, "Chatbook", str(exc))
            return

        if data.startswith("Error"):
            self.create_window.creationMessage_2.setText(data.split("|", 1)[-1])
            return

        self.current_room = name
        self.create_window.hide()
        if self.admin_mode:
            self.show_admin()
        else:
            self.enter_main()
        self.open_chat(name)

    def show_admin(self):
        self.admin_mode = True
        self.main_window.hide()
        self.create_window.hide()
        self.admin_window.show()
        self.admin_window.label_Nickname.setText("Admin · " + self.username)
        self.refresh_data()
        self.populate_sidebar(self.admin_window, show_add_buttons=True)
        if self.current_room:
            self.open_chat(self.current_room)
        else:
            self.populate_members()

    def send_message(self):
        window = self._active_window()
        text = window.lineEdit.text().strip()
        if not text:
            return
        if not self.current_room:
            QMessageBox.information(window, "Chatbook", "Open a chat room first.")
            return
        try:
            self.client.request(
                "messageSent|" + self.username + "->" + text + "|" + self.current_room
            )
        except OSError as exc:
            QMessageBox.critical(window, "Chatbook", str(exc))
            return
        window.lineEdit.clear()
        self.open_chat(self.current_room)

    def close(self):
        QApplication.quit()

    def run(self):
        self.login_window.show()


def apply_theme(app):
    app.setStyle("Fusion")
    qss_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.qss")
    try:
        with open(qss_path, encoding="utf-8") as handle:
            app.setStyleSheet(handle.read())
    except OSError:
        pass


def main():
    app = QApplication(sys.argv)
    apply_theme(app)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
    except OSError as exc:
        QMessageBox.critical(
            None,
            "Chatbook",
            "Could not connect to {0}:{1}\n{2}\n\n"
            "Start the server first:\n  make -C server && ./server/tcpserver".format(
                HOST, PORT, exc
            ),
        )
        return 1

    try:
        ChatbookApp(ChatClient(sock)).run()
        return app.exec_()
    finally:
        sock.close()


if __name__ == "__main__":
    sys.exit(main())
