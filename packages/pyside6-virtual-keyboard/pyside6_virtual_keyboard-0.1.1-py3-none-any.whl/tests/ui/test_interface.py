# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test_interface.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QGridLayout, QLabel,
    QMainWindow, QSizePolicy, QWidget)

from PySide6VirtualKeyboard.keyboard.virtual_keyboard import VirtualKeyboard
from PySide6VirtualKeyboard.lineEdit.virtual_keyboard_lineEdit import VirtualKeyboardLineEdit
from PySide6VirtualKeyboard.scrollArea.virtual_keyboard_scroll_area import VirtualKeyboardScrollArea

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1920, 1080)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.scrollArea = VirtualKeyboardScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u"background-color: rgb(119, 118, 123);")
        self.scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1886, 1284))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineEdit_9 = VirtualKeyboardLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_9.setObjectName(u"lineEdit_9")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_9.sizePolicy().hasHeightForWidth())
        self.lineEdit_9.setSizePolicy(sizePolicy)
        self.lineEdit_9.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_9.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout.addWidget(self.lineEdit_9, 5, 3, 1, 1)

        self.lineEdit_3 = VirtualKeyboardLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setMinimumSize(QSize(0, 100))
        self.lineEdit_3.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_3.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout.addWidget(self.lineEdit_3, 2, 1, 1, 1)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.label_20 = QLabel(self.scrollAreaWidgetContents)
        self.label_20.setObjectName(u"label_20")
        sizePolicy1.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_20, 6, 0, 1, 1)

        self.lineEdit_23 = VirtualKeyboardLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_23.setObjectName(u"lineEdit_23")
        sizePolicy.setHeightForWidth(self.lineEdit_23.sizePolicy().hasHeightForWidth())
        self.lineEdit_23.setSizePolicy(sizePolicy)
        self.lineEdit_23.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_23.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout.addWidget(self.lineEdit_23, 10, 3, 1, 1)

        self.label_11 = QLabel(self.scrollAreaWidgetContents)
        self.label_11.setObjectName(u"label_11")
        sizePolicy1.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_11, 4, 0, 1, 1)

        self.lineEdit_15 = VirtualKeyboardLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_15.setObjectName(u"lineEdit_15")
        sizePolicy.setHeightForWidth(self.lineEdit_15.sizePolicy().hasHeightForWidth())
        self.lineEdit_15.setSizePolicy(sizePolicy)
        self.lineEdit_15.setMinimumSize(QSize(0, 100))
        self.lineEdit_15.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_15.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout.addWidget(self.lineEdit_15, 11, 1, 1, 1)

        self.label_23 = QLabel(self.scrollAreaWidgetContents)
        self.label_23.setObjectName(u"label_23")
        sizePolicy1.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_23, 11, 0, 1, 1)

        self.label_19 = QLabel(self.scrollAreaWidgetContents)
        self.label_19.setObjectName(u"label_19")
        sizePolicy1.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_19, 7, 0, 1, 1)

        self.lineEdit_13 = VirtualKeyboardLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_13.setObjectName(u"lineEdit_13")
        sizePolicy.setHeightForWidth(self.lineEdit_13.sizePolicy().hasHeightForWidth())
        self.lineEdit_13.setSizePolicy(sizePolicy)
        self.lineEdit_13.setMinimumSize(QSize(0, 100))
        self.lineEdit_13.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_13.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout.addWidget(self.lineEdit_13, 9, 1, 1, 1)

        self.label_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName(u"label_4")
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)

        self.lineEdit_18 = VirtualKeyboardLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_18.setObjectName(u"lineEdit_18")
        sizePolicy.setHeightForWidth(self.lineEdit_18.sizePolicy().hasHeightForWidth())
        self.lineEdit_18.setSizePolicy(sizePolicy)
        self.lineEdit_18.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_18.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout.addWidget(self.lineEdit_18, 9, 3, 1, 1)

        self.lineEdit_6 = VirtualKeyboardLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        sizePolicy.setHeightForWidth(self.lineEdit_6.sizePolicy().hasHeightForWidth())
        self.lineEdit_6.setSizePolicy(sizePolicy)
        self.lineEdit_6.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_6.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout.addWidget(self.lineEdit_6, 0, 3, 1, 1)

        self.label_22 = QLabel(self.scrollAreaWidgetContents)
        self.label_22.setObjectName(u"label_22")
        sizePolicy1.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_22, 9, 0, 1, 1)

        self.lineEdit_20 = VirtualKeyboardLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_20.setObjectName(u"lineEdit_20")
        sizePolicy.setHeightForWidth(self.lineEdit_20.sizePolicy().hasHeightForWidth())
        self.lineEdit_20.setSizePolicy(sizePolicy)
        self.lineEdit_20.setMinimumSize(QSize(0, 100))
        self.lineEdit_20.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_20.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout.addWidget(self.lineEdit_20, 8, 1, 1, 1)

        self.lineEdit_4 = VirtualKeyboardLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        sizePolicy.setHeightForWidth(self.lineEdit_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_4.setSizePolicy(sizePolicy)
        self.lineEdit_4.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_4.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout.addWidget(self.lineEdit_4, 1, 3, 1, 1)

        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")
        sizePolicy1.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_6, 0, 2, 1, 1)

        self.label_12 = QLabel(self.scrollAreaWidgetContents)
        self.label_12.setObjectName(u"label_12")
        sizePolicy1.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_12, 3, 0, 1, 1)

        self.lineEdit_8 = VirtualKeyboardLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        sizePolicy.setHeightForWidth(self.lineEdit_8.sizePolicy().hasHeightForWidth())
        self.lineEdit_8.setSizePolicy(sizePolicy)
        self.lineEdit_8.setMinimumSize(QSize(0, 100))
        self.lineEdit_8.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_8.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout.addWidget(self.lineEdit_8, 4, 1, 1, 1)

        self.lineEdit_5 = VirtualKeyboardLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        sizePolicy.setHeightForWidth(self.lineEdit_5.sizePolicy().hasHeightForWidth())
        self.lineEdit_5.setSizePolicy(sizePolicy)
        self.lineEdit_5.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_5.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout.addWidget(self.lineEdit_5, 2, 3, 1, 1)

        self.label_15 = QLabel(self.scrollAreaWidgetContents)
        self.label_15.setObjectName(u"label_15")
        sizePolicy1.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_15, 8, 0, 1, 1)

        self.lineEdit_24 = VirtualKeyboardLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_24.setObjectName(u"lineEdit_24")
        sizePolicy.setHeightForWidth(self.lineEdit_24.sizePolicy().hasHeightForWidth())
        self.lineEdit_24.setSizePolicy(sizePolicy)
        self.lineEdit_24.setMinimumSize(QSize(0, 100))
        self.lineEdit_24.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_24.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout.addWidget(self.lineEdit_24, 6, 1, 1, 1)

        self.lineEdit_21 = VirtualKeyboardLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_21.setObjectName(u"lineEdit_21")
        sizePolicy.setHeightForWidth(self.lineEdit_21.sizePolicy().hasHeightForWidth())
        self.lineEdit_21.setSizePolicy(sizePolicy)
        self.lineEdit_21.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_21.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout.addWidget(self.lineEdit_21, 6, 3, 1, 1)

        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit_7 = VirtualKeyboardLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        sizePolicy.setHeightForWidth(self.lineEdit_7.sizePolicy().hasHeightForWidth())
        self.lineEdit_7.setSizePolicy(sizePolicy)
        self.lineEdit_7.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_7.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout.addWidget(self.lineEdit_7, 3, 3, 1, 1)

        self.lineEdit_16 = VirtualKeyboardLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_16.setObjectName(u"lineEdit_16")
        sizePolicy.setHeightForWidth(self.lineEdit_16.sizePolicy().hasHeightForWidth())
        self.lineEdit_16.setSizePolicy(sizePolicy)
        self.lineEdit_16.setMinimumSize(QSize(0, 100))
        self.lineEdit_16.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_16.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout.addWidget(self.lineEdit_16, 10, 1, 1, 1)

        self.lineEdit_19 = VirtualKeyboardLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_19.setObjectName(u"lineEdit_19")
        sizePolicy.setHeightForWidth(self.lineEdit_19.sizePolicy().hasHeightForWidth())
        self.lineEdit_19.setSizePolicy(sizePolicy)
        self.lineEdit_19.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_19.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout.addWidget(self.lineEdit_19, 8, 3, 1, 1)

        self.lineEdit_12 = VirtualKeyboardLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_12.setObjectName(u"lineEdit_12")
        sizePolicy.setHeightForWidth(self.lineEdit_12.sizePolicy().hasHeightForWidth())
        self.lineEdit_12.setSizePolicy(sizePolicy)
        self.lineEdit_12.setMinimumSize(QSize(0, 100))
        self.lineEdit_12.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_12.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout.addWidget(self.lineEdit_12, 3, 1, 1, 1)

        self.lineEdit = VirtualKeyboardLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QSize(0, 100))
        self.lineEdit.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.lineEdit_10 = VirtualKeyboardLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_10.setObjectName(u"lineEdit_10")
        sizePolicy.setHeightForWidth(self.lineEdit_10.sizePolicy().hasHeightForWidth())
        self.lineEdit_10.setSizePolicy(sizePolicy)
        self.lineEdit_10.setMinimumSize(QSize(0, 100))
        self.lineEdit_10.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_10.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout.addWidget(self.lineEdit_10, 5, 1, 1, 1)

        self.lineEdit_11 = VirtualKeyboardLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_11.setObjectName(u"lineEdit_11")
        sizePolicy.setHeightForWidth(self.lineEdit_11.sizePolicy().hasHeightForWidth())
        self.lineEdit_11.setSizePolicy(sizePolicy)
        self.lineEdit_11.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_11.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout.addWidget(self.lineEdit_11, 4, 3, 1, 1)

        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")
        sizePolicy1.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_5, 2, 2, 1, 1)

        self.lineEdit_17 = VirtualKeyboardLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_17.setObjectName(u"lineEdit_17")
        sizePolicy.setHeightForWidth(self.lineEdit_17.sizePolicy().hasHeightForWidth())
        self.lineEdit_17.setSizePolicy(sizePolicy)
        self.lineEdit_17.setMinimumSize(QSize(0, 100))
        self.lineEdit_17.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_17.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout.addWidget(self.lineEdit_17, 7, 1, 1, 1)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.lineEdit_14 = VirtualKeyboardLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_14.setObjectName(u"lineEdit_14")
        sizePolicy.setHeightForWidth(self.lineEdit_14.sizePolicy().hasHeightForWidth())
        self.lineEdit_14.setSizePolicy(sizePolicy)
        self.lineEdit_14.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_14.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout.addWidget(self.lineEdit_14, 11, 3, 1, 1)

        self.label_13 = QLabel(self.scrollAreaWidgetContents)
        self.label_13.setObjectName(u"label_13")
        sizePolicy1.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_13, 10, 0, 1, 1)

        self.lineEdit_2 = VirtualKeyboardLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setMinimumSize(QSize(0, 100))
        self.lineEdit_2.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_2.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)

        self.label_8 = QLabel(self.scrollAreaWidgetContents)
        self.label_8.setObjectName(u"label_8")
        sizePolicy1.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_8, 5, 0, 1, 1)

        self.lineEdit_22 = VirtualKeyboardLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_22.setObjectName(u"lineEdit_22")
        sizePolicy.setHeightForWidth(self.lineEdit_22.sizePolicy().hasHeightForWidth())
        self.lineEdit_22.setSizePolicy(sizePolicy)
        self.lineEdit_22.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_22.setContextMenuPolicy(Qt.NoContextMenu)

        self.gridLayout.addWidget(self.lineEdit_22, 7, 3, 1, 1)

        self.label_14 = QLabel(self.scrollAreaWidgetContents)
        self.label_14.setObjectName(u"label_14")
        sizePolicy1.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_14, 3, 2, 1, 1)

        self.label_16 = QLabel(self.scrollAreaWidgetContents)
        self.label_16.setObjectName(u"label_16")
        sizePolicy1.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_16, 4, 2, 1, 1)

        self.label_9 = QLabel(self.scrollAreaWidgetContents)
        self.label_9.setObjectName(u"label_9")
        sizePolicy1.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_9, 5, 2, 1, 1)

        self.label_21 = QLabel(self.scrollAreaWidgetContents)
        self.label_21.setObjectName(u"label_21")
        sizePolicy1.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_21, 6, 2, 1, 1)

        self.label_24 = QLabel(self.scrollAreaWidgetContents)
        self.label_24.setObjectName(u"label_24")
        sizePolicy1.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_24, 7, 2, 1, 1)

        self.label_17 = QLabel(self.scrollAreaWidgetContents)
        self.label_17.setObjectName(u"label_17")
        sizePolicy1.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_17, 8, 2, 1, 1)

        self.label_25 = QLabel(self.scrollAreaWidgetContents)
        self.label_25.setObjectName(u"label_25")
        sizePolicy1.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_25, 9, 2, 1, 1)

        self.label_18 = QLabel(self.scrollAreaWidgetContents)
        self.label_18.setObjectName(u"label_18")
        sizePolicy1.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_18, 10, 2, 1, 1)

        self.label_26 = QLabel(self.scrollAreaWidgetContents)
        self.label_26.setObjectName(u"label_26")
        sizePolicy1.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_26, 11, 2, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.widget = VirtualKeyboard(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 477))
        self.widget.setStyleSheet(u"background-color: transparent;")

        self.gridLayout_2.addWidget(self.widget, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi

