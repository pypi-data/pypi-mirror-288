from PySide6.QtWidgets import QLineEdit, QMainWindow
from PySide6.QtCore import Qt, QEvent
from ui.test_interface import Ui_MainWindow


class KeyboardTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.lineEdit_list = self.ui.scrollAreaWidgetContents.findChildren(QLineEdit)

        self.ui.widget.set_keyboard_background("")

        self.ui.widget.hide()

        for line in self.lineEdit_list:
            line.set_keyboard_widget(self.ui.widget)
            line.set_scroll_area(self.ui.scrollArea)
