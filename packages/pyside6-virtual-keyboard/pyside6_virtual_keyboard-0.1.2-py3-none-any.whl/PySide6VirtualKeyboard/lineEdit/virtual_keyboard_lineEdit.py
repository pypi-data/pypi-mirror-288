from PySide6.QtGui import QFocusEvent, QMouseEvent
from PySide6.QtWidgets import QLineEdit, QWidget, QScrollArea
from PySide6.QtCore import Qt, Slot, QPoint, QElapsedTimer
from PySide6VirtualKeyboard.keyboard.virtual_keyboard import VirtualKeyboard


class VirtualKeyboardLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        self.__parent = parent
        print(f"parent {self.__parent}")
        self.__keyboard = None

        self.__scroll_area = None

        self.__is_editing_finished = True

        self.__parent.installEventFilter(self)

        self.__keyboard_hide_timer = QElapsedTimer()

    def set_keyboard_widget(self, keyboard: VirtualKeyboard):
        self.__keyboard = keyboard
        self.__keyboard.return_pressed.connect(self.return_pressed_handler)

    def set_scroll_area(self, scroll_area: QScrollArea):
        self.__scroll_area = scroll_area

    def return_pressed_handler(self):
        self.__keyboard.hide()
        self.clearFocus()

    def focusInEvent(self, event):
        if self.__keyboard:
            self.__keyboard.show()
            self.__keyboard.set_input_line_edit(self)
            self.__is_editing_finished = False

            current_pos = QPoint(self.pos().x(), self.pos().y())
            print(f"current_pos {current_pos}")
            print(f"focus in event : {self.objectName()}")
            self.__scroll_area.verticalScrollBar().setValue(self.pos().y() - 50)

        super().focusInEvent(event)

    def focusOutEvent(self, event: QFocusEvent):

        self.__keyboard.hide()
        self.__is_editing_finished = True
        self.clearFocus()
        print(f"is editing finished: {self.__is_editing_finished}")

        super().focusOutEvent(event)

    def eventFilter(self, watched, event):
        if event.type() == QMouseEvent.Type.MouseButtonPress:
            if not self.__keyboard.geometry().contains(event.globalPosition().toPoint()):
                print(f"klavye dışına tıklandı: {self.objectName()} ")

                self.__keyboard_hide_timer.start()

        if event.type() == QMouseEvent.Type.MouseButtonRelease:
            if self.__keyboard_hide_timer.isValid() and self.__keyboard_hide_timer.elapsed() < 250:
                print("keyboard hide event")
                self.__is_editing_finished = True
                self.__keyboard.hide()
                self.clearFocus()
                self.__keyboard_hide_timer.invalidate()
        return super().eventFilter(watched, event)
