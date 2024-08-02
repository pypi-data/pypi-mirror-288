import sys

from PySide6.QtWidgets import QApplication

from test_ui import KeyboardTestWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("PySide6VirtualKeyboard v0.1.0")
    app_window = KeyboardTestWindow()
    app_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
