import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QScrollArea, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QMouseEvent


class ScrollArea(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        content_widget = QWidget()
        self.setWidget(content_widget)

        self.start_pos = None
        self.vertical_scroll_start_value = 0

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_pos = event.position().toPoint()
            self.vertical_scroll_start_value = self.verticalScrollBar().value()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.start_pos is not None:
            delta = event.position().toPoint() - self.start_pos
            new_value = self.vertical_scroll_start_value - delta.y()
            self.verticalScrollBar().setValue(new_value)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_pos = None
        super().mouseReleaseEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mouse Event Scroll Example")
        self.resize(400, 300)

        scroll_area = ScrollArea()
        self.setCentralWidget(scroll_area)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
