"""Smoke test that Qt Designer files still load."""

import os
import sys
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)


class UiLoadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from PyQt5.QtWidgets import QApplication

        cls.app = QApplication.instance() or QApplication(["chatbook-test"])

    def test_all_forms_load(self):
        from PyQt5 import uic

        os.chdir(ROOT)
        for name in (
            "Login.ui",
            "Register.ui",
            "error.ui",
            "createChatRoom.ui",
            "MainWindow.ui",
            "MainWindowAdmin.ui",
        ):
            window = uic.loadUi(name)
            self.assertIsNotNone(window)
            window.close()

    def test_login_and_main_widgets_exist(self):
        from PyQt5 import uic

        os.chdir(ROOT)
        login = uic.loadUi("Login.ui")
        main = uic.loadUi("MainWindow.ui")
        admin = uic.loadUi("MainWindowAdmin.ui")
        for widget in (
            login.lineEdit,
            login.lineEdit_2,
            login.pushButton,
            main.button_send,
            main.lineEdit,
            main.label_2,
            main.scrollAreaWidgetContents_2,
            admin.button_send,
            admin.lineEdit,
            admin.scrollAreaWidgetContents_4,
        ):
            self.assertIsNotNone(widget)
        login.close()
        main.close()
        admin.close()


if __name__ == "__main__":
    unittest.main()
