from PySide6.QtWidgets import QWidget, QPushButton, QLineEdit
from PySide6.QtCore import Qt, Signal, Slot

from PySide6VirtualKeyboard.ui.interface import Ui_KeyboardUI


# import PySide6VirtualKeyboard.resources.resources_rc


def to_lower_turkish(text):
    # Türkçe karakterler için küçük harf dönüşüm tablosu
    translation_table = str.maketrans("ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZQWX",
                                      "abcçdefgğhıijklmnoöprsştuüvyzqwx")
    return text.translate(translation_table)


def to_upper_turkish(text):
    # Türkçe karakterler için büyük harf dönüşüm tablosu
    translation_table = str.maketrans("abcçdefgğhıijklmnoöprsştuüvyzqwx",
                                      "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZQWX")
    return text.translate(translation_table)


class VirtualKeyboard(QWidget):
    return_pressed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__ui = Ui_KeyboardUI()
        self.__ui.setupUi(self)
        self.__ui.retranslateUi(self)

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        # Ui elements
        self.__input_line_edit = None

        self.__shift_button = self.__ui.pushButton_shift
        self.__backspace_button_abc = self.__ui.pushButton_abc_backspace

        self.__stacked_widget = self.__ui.stackedWidget_keyboard_layout

        self.__numeric_button_list_abc = self.__ui.widget_numeric_button_abc.findChildren(QPushButton)
        self.__numeric_button_list_123 = self.__ui.widget_numeric_button_123.findChildren(QPushButton)

        self.__symbol_button_list_123 = self.__ui.widget_123_1.findChildren(QPushButton) + \
                                        self.__ui.widget_123_2.findChildren(QPushButton)

        self.__symbol_button_list_sym = self.__ui.widget_sym_1.findChildren(QPushButton) + \
                                        self.__ui.widget_sym_2.findChildren(QPushButton) + \
                                        self.__ui.widget_sym_3.findChildren(QPushButton) + \
                                        self.__ui.widget_sym_4.findChildren(QPushButton)

        self.__letter_button_list = self.__ui.widget_abc_1.findChildren(QPushButton) + \
                                    self.__ui.widget_abc_2.findChildren(QPushButton) + \
                                    self.__ui.widget_abc_3.findChildren(QPushButton)

        self.__comma_button_list = [self.__ui.pushButton_abc_comma, self.__ui.pushButton_123_comma,
                                    self.__ui.pushButton_sym_comma]

        self.__dot_button_list = [self.__ui.pushButton_abc_dot, self.__ui.pushButton_123_dot,
                                  self.__ui.pushButton_sym_dot]

        # Init functions
        self.signal_connect()

    def set_keyboard_background(self, stylesheet):
        self.__ui.frame_background.setStyleSheet(stylesheet)

    def set_space_buttons_image(self, image_path):
        style_sheet = f"""
        QPushButton{{
            background-color: rgba(71, 68, 68, 209);
            padding-top: 60px;
            image: url({image_path});
            border-radius: 15px;
        }}
        QPushButton:pressed {{
            background-color: rgba(50, 50, 50, 209);
        }}
        """
        self.__ui.pushButton_abc_space.setStyleSheet(style_sheet)
        self.__ui.pushButton_123_space.setStyleSheet(style_sheet)
        self.__ui.pushButton_sym_space.setStyleSheet(style_sheet)

    def signal_connect(self):

        self.__ui.pushButton_abc_to_123.clicked.connect(lambda: self.__stacked_widget.setCurrentIndex(1))
        self.__ui.pushButton_123_to_symbols.clicked.connect(lambda: self.__stacked_widget.setCurrentIndex(2))
        self.__ui.pushButton_123_to_abc.clicked.connect(lambda: self.__stacked_widget.setCurrentIndex(0))
        self.__ui.pushButton_sym_to_abc.clicked.connect(lambda: self.__stacked_widget.setCurrentIndex(0))
        self.__ui.pushButton_sym_to_123.clicked.connect(lambda: self.__stacked_widget.setCurrentIndex(1))

        self.__shift_button.clicked.connect(self.shift_button_handler)

        self.connect_buttons(self.__letter_button_list)
        self.connect_buttons(self.__numeric_button_list_abc)
        self.connect_buttons(self.__numeric_button_list_123)
        self.connect_buttons(self.__symbol_button_list_123)
        self.connect_buttons(self.__symbol_button_list_sym)
        self.connect_buttons(self.__comma_button_list)
        self.connect_buttons(self.__dot_button_list)

        self.__ui.pushButton_abc_backspace.clicked.connect(lambda: self.__input_line_edit.backspace())
        self.__ui.pushButton_123_backspace.clicked.connect(lambda: self.__input_line_edit.backspace())
        self.__ui.pushButton_sym_backspace.clicked.connect(lambda: self.__input_line_edit.backspace())

        self.__ui.pushButton_abc_enter.clicked.connect(lambda: self.return_pressed.emit())
        self.__ui.pushButton_123_enter.clicked.connect(lambda: self.return_pressed.emit())
        self.__ui.pushButton_sym_enter.clicked.connect(lambda: self.return_pressed.emit())

        self.__ui.pushButton_abc_space.clicked.connect(lambda: self.insert_text(" "))
        self.__ui.pushButton_123_space.clicked.connect(lambda: self.insert_text(" "))
        self.__ui.pushButton_sym_space.clicked.connect(lambda: self.insert_text(" "))

    def set_input_line_edit(self, input_line: QLineEdit):
        self.__input_line_edit = input_line
        print(f"input_line: {input_line.objectName()}")

    def connect_buttons(self, button_list):
        for button in button_list:
            if len(button.text()) == 1:
                print(f"button text: {button.text()}")
                button.clicked.connect(lambda checked, text=button.text(): self.insert_text(text))

    @Slot()
    def shift_button_handler(self):
        if self.__shift_button.isChecked():
            for button in self.__letter_button_list:
                if button.text() != "":
                    button.setText(to_lower_turkish(button.text()))
        else:
            for button in self.__letter_button_list:
                if button.text() != "":
                    button.setText(to_upper_turkish(button.text()))

    @Slot()
    def insert_text(self, text):
        print(f"insert text: {text}")
        cursor = self.__input_line_edit.cursorPosition()
        self.__input_line_edit.insert(text)
        self.__input_line_edit.setCursorPosition(cursor + 1)

    @Slot()
    def hide(self):
        self.__ui.stackedWidget_keyboard_layout.setCurrentIndex(0)
        super().hide()
