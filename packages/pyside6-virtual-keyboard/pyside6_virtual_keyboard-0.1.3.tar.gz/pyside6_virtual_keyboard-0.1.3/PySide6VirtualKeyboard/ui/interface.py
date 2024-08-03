# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interface.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QWidget)
import PySide6VirtualKeyboard.resources.resources_rc

class Ui_KeyboardUI(object):
    def setupUi(self, KeyboardUI):
        if not KeyboardUI.objectName():
            KeyboardUI.setObjectName(u"KeyboardUI")
        KeyboardUI.resize(1920, 432)
        self.gridLayout_6 = QGridLayout(KeyboardUI)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.frame_background = QFrame(KeyboardUI)
        self.frame_background.setObjectName(u"frame_background")
        self.frame_background.setStyleSheet(u"QFrame#frame_background{\n"
"	background-color: rgba(15, 9, 92, 61);\n"
"}")
        self.frame_background.setFrameShape(QFrame.StyledPanel)
        self.frame_background.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_background)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 5, 0, 0)
        self.stackedWidget_keyboard_layout = QStackedWidget(self.frame_background)
        self.stackedWidget_keyboard_layout.setObjectName(u"stackedWidget_keyboard_layout")
        self.stackedWidget_keyboard_layout.setStyleSheet(u"QStackedWidget#stackedWidget_keyboard_layout{\n"
"	\n"
"	background-color: transparent;\n"
"}")
        self.page_abc = QWidget()
        self.page_abc.setObjectName(u"page_abc")
        self.page_abc.setStyleSheet(u"QWidget#page_abc{background-color: transparent;}")
        self.gridLayout_8 = QGridLayout(self.page_abc)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setHorizontalSpacing(0)
        self.gridLayout_8.setVerticalSpacing(5)
        self.gridLayout_8.setContentsMargins(0, 10, 0, 0)
        self.widget_numeric_button_abc = QWidget(self.page_abc)
        self.widget_numeric_button_abc.setObjectName(u"widget_numeric_button_abc")
        self.widget_numeric_button_abc.setMaximumSize(QSize(1300, 16777215))
        font = QFont()
        font.setFamilies([u"Ubuntu Condensed"])
        font.setPointSize(20)
        font.setBold(False)
        self.widget_numeric_button_abc.setFont(font)
        self.widget_numeric_button_abc.setFocusPolicy(Qt.NoFocus)
        self.widget_numeric_button_abc.setStyleSheet(u"QWidget#widget{background-color: transparent;}")
        self.gridLayout = QGridLayout(self.widget_numeric_button_abc)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(9)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.pushButton_abc_1 = QPushButton(self.widget_numeric_button_abc)
        self.pushButton_abc_1.setObjectName(u"pushButton_abc_1")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_abc_1.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_1.setSizePolicy(sizePolicy)
        self.pushButton_abc_1.setMinimumSize(QSize(110, 0))
        self.pushButton_abc_1.setFont(font)
        self.pushButton_abc_1.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_1.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout.addWidget(self.pushButton_abc_1, 0, 0, 1, 1)

        self.pushButton_abc_2 = QPushButton(self.widget_numeric_button_abc)
        self.pushButton_abc_2.setObjectName(u"pushButton_abc_2")
        sizePolicy.setHeightForWidth(self.pushButton_abc_2.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_2.setSizePolicy(sizePolicy)
        self.pushButton_abc_2.setMinimumSize(QSize(110, 0))
        self.pushButton_abc_2.setFont(font)
        self.pushButton_abc_2.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_2.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout.addWidget(self.pushButton_abc_2, 0, 1, 1, 1)

        self.pushButton_abc_3 = QPushButton(self.widget_numeric_button_abc)
        self.pushButton_abc_3.setObjectName(u"pushButton_abc_3")
        sizePolicy.setHeightForWidth(self.pushButton_abc_3.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_3.setSizePolicy(sizePolicy)
        self.pushButton_abc_3.setMinimumSize(QSize(110, 0))
        self.pushButton_abc_3.setFont(font)
        self.pushButton_abc_3.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_3.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout.addWidget(self.pushButton_abc_3, 0, 2, 1, 1)

        self.pushButton_abc_4 = QPushButton(self.widget_numeric_button_abc)
        self.pushButton_abc_4.setObjectName(u"pushButton_abc_4")
        sizePolicy.setHeightForWidth(self.pushButton_abc_4.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_4.setSizePolicy(sizePolicy)
        self.pushButton_abc_4.setMinimumSize(QSize(110, 0))
        self.pushButton_abc_4.setFont(font)
        self.pushButton_abc_4.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_4.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout.addWidget(self.pushButton_abc_4, 0, 3, 1, 1)

        self.pushButton_abc_5 = QPushButton(self.widget_numeric_button_abc)
        self.pushButton_abc_5.setObjectName(u"pushButton_abc_5")
        sizePolicy.setHeightForWidth(self.pushButton_abc_5.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_5.setSizePolicy(sizePolicy)
        self.pushButton_abc_5.setMinimumSize(QSize(110, 0))
        self.pushButton_abc_5.setFont(font)
        self.pushButton_abc_5.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_5.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout.addWidget(self.pushButton_abc_5, 0, 4, 1, 1)

        self.pushButton_abc_6 = QPushButton(self.widget_numeric_button_abc)
        self.pushButton_abc_6.setObjectName(u"pushButton_abc_6")
        sizePolicy.setHeightForWidth(self.pushButton_abc_6.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_6.setSizePolicy(sizePolicy)
        self.pushButton_abc_6.setMinimumSize(QSize(110, 0))
        self.pushButton_abc_6.setFont(font)
        self.pushButton_abc_6.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_6.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout.addWidget(self.pushButton_abc_6, 0, 5, 1, 1)

        self.pushButton_abc_7 = QPushButton(self.widget_numeric_button_abc)
        self.pushButton_abc_7.setObjectName(u"pushButton_abc_7")
        sizePolicy.setHeightForWidth(self.pushButton_abc_7.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_7.setSizePolicy(sizePolicy)
        self.pushButton_abc_7.setMinimumSize(QSize(110, 0))
        self.pushButton_abc_7.setFont(font)
        self.pushButton_abc_7.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_7.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout.addWidget(self.pushButton_abc_7, 0, 6, 1, 1)

        self.pushButton_abc_8 = QPushButton(self.widget_numeric_button_abc)
        self.pushButton_abc_8.setObjectName(u"pushButton_abc_8")
        sizePolicy.setHeightForWidth(self.pushButton_abc_8.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_8.setSizePolicy(sizePolicy)
        self.pushButton_abc_8.setMinimumSize(QSize(110, 0))
        self.pushButton_abc_8.setFont(font)
        self.pushButton_abc_8.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_8.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout.addWidget(self.pushButton_abc_8, 0, 7, 1, 1)

        self.pushButton_abc_9 = QPushButton(self.widget_numeric_button_abc)
        self.pushButton_abc_9.setObjectName(u"pushButton_abc_9")
        sizePolicy.setHeightForWidth(self.pushButton_abc_9.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_9.setSizePolicy(sizePolicy)
        self.pushButton_abc_9.setMinimumSize(QSize(110, 0))
        self.pushButton_abc_9.setFont(font)
        self.pushButton_abc_9.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_9.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout.addWidget(self.pushButton_abc_9, 0, 8, 1, 1)

        self.pushButton_abc_0 = QPushButton(self.widget_numeric_button_abc)
        self.pushButton_abc_0.setObjectName(u"pushButton_abc_0")
        sizePolicy.setHeightForWidth(self.pushButton_abc_0.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_0.setSizePolicy(sizePolicy)
        self.pushButton_abc_0.setMinimumSize(QSize(110, 0))
        self.pushButton_abc_0.setFont(font)
        self.pushButton_abc_0.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_0.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout.addWidget(self.pushButton_abc_0, 0, 9, 1, 1)


        self.gridLayout_8.addWidget(self.widget_numeric_button_abc, 0, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(293, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_3, 1, 0, 1, 1)

        self.widget_abc_1 = QWidget(self.page_abc)
        self.widget_abc_1.setObjectName(u"widget_abc_1")
        self.widget_abc_1.setFont(font)
        self.widget_abc_1.setFocusPolicy(Qt.NoFocus)
        self.widget_abc_1.setStyleSheet(u"QWidget#widget_2{background-color: transparent;}")
        self.gridLayout_2 = QGridLayout(self.widget_abc_1)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(8)
        self.gridLayout_2.setVerticalSpacing(0)
        self.gridLayout_2.setContentsMargins(5, 5, 5, 5)
        self.pushButton_abc_tr_u = QPushButton(self.widget_abc_1)
        self.pushButton_abc_tr_u.setObjectName(u"pushButton_abc_tr_u")
        sizePolicy.setHeightForWidth(self.pushButton_abc_tr_u.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_tr_u.setSizePolicy(sizePolicy)
        self.pushButton_abc_tr_u.setMinimumSize(QSize(90, 0))
        self.pushButton_abc_tr_u.setFont(font)
        self.pushButton_abc_tr_u.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_tr_u.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_2.addWidget(self.pushButton_abc_tr_u, 0, 11, 1, 1)

        self.pushButton_abc_p = QPushButton(self.widget_abc_1)
        self.pushButton_abc_p.setObjectName(u"pushButton_abc_p")
        sizePolicy.setHeightForWidth(self.pushButton_abc_p.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_p.setSizePolicy(sizePolicy)
        self.pushButton_abc_p.setMinimumSize(QSize(90, 0))
        self.pushButton_abc_p.setFont(font)
        self.pushButton_abc_p.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_p.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_2.addWidget(self.pushButton_abc_p, 0, 9, 1, 1)

        self.pushButton_abc_y = QPushButton(self.widget_abc_1)
        self.pushButton_abc_y.setObjectName(u"pushButton_abc_y")
        sizePolicy.setHeightForWidth(self.pushButton_abc_y.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_y.setSizePolicy(sizePolicy)
        self.pushButton_abc_y.setMinimumSize(QSize(90, 0))
        self.pushButton_abc_y.setFont(font)
        self.pushButton_abc_y.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_y.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_2.addWidget(self.pushButton_abc_y, 0, 5, 1, 1)

        self.pushButton_abc_e = QPushButton(self.widget_abc_1)
        self.pushButton_abc_e.setObjectName(u"pushButton_abc_e")
        sizePolicy.setHeightForWidth(self.pushButton_abc_e.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_e.setSizePolicy(sizePolicy)
        self.pushButton_abc_e.setMinimumSize(QSize(90, 0))
        self.pushButton_abc_e.setFont(font)
        self.pushButton_abc_e.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_e.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_2.addWidget(self.pushButton_abc_e, 0, 2, 1, 1)

        self.pushButton_abc_t = QPushButton(self.widget_abc_1)
        self.pushButton_abc_t.setObjectName(u"pushButton_abc_t")
        sizePolicy.setHeightForWidth(self.pushButton_abc_t.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_t.setSizePolicy(sizePolicy)
        self.pushButton_abc_t.setMinimumSize(QSize(90, 0))
        self.pushButton_abc_t.setFont(font)
        self.pushButton_abc_t.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_t.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_2.addWidget(self.pushButton_abc_t, 0, 4, 1, 1)

        self.pushButton_abc_o = QPushButton(self.widget_abc_1)
        self.pushButton_abc_o.setObjectName(u"pushButton_abc_o")
        sizePolicy.setHeightForWidth(self.pushButton_abc_o.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_o.setSizePolicy(sizePolicy)
        self.pushButton_abc_o.setMinimumSize(QSize(90, 0))
        self.pushButton_abc_o.setFont(font)
        self.pushButton_abc_o.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_o.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_2.addWidget(self.pushButton_abc_o, 0, 8, 1, 1)

        self.pushButton_abc_w = QPushButton(self.widget_abc_1)
        self.pushButton_abc_w.setObjectName(u"pushButton_abc_w")
        sizePolicy.setHeightForWidth(self.pushButton_abc_w.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_w.setSizePolicy(sizePolicy)
        self.pushButton_abc_w.setMinimumSize(QSize(90, 0))
        self.pushButton_abc_w.setFont(font)
        self.pushButton_abc_w.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_w.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_2.addWidget(self.pushButton_abc_w, 0, 1, 1, 1)

        self.pushButton_abc_q = QPushButton(self.widget_abc_1)
        self.pushButton_abc_q.setObjectName(u"pushButton_abc_q")
        sizePolicy.setHeightForWidth(self.pushButton_abc_q.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_q.setSizePolicy(sizePolicy)
        self.pushButton_abc_q.setMinimumSize(QSize(90, 0))
        self.pushButton_abc_q.setFont(font)
        self.pushButton_abc_q.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_q.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_2.addWidget(self.pushButton_abc_q, 0, 0, 1, 1)

        self.pushButton_abc_u = QPushButton(self.widget_abc_1)
        self.pushButton_abc_u.setObjectName(u"pushButton_abc_u")
        sizePolicy.setHeightForWidth(self.pushButton_abc_u.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_u.setSizePolicy(sizePolicy)
        self.pushButton_abc_u.setMinimumSize(QSize(90, 0))
        self.pushButton_abc_u.setFont(font)
        self.pushButton_abc_u.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_u.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_2.addWidget(self.pushButton_abc_u, 0, 6, 1, 1)

        self.pushButton_abc_r = QPushButton(self.widget_abc_1)
        self.pushButton_abc_r.setObjectName(u"pushButton_abc_r")
        sizePolicy.setHeightForWidth(self.pushButton_abc_r.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_r.setSizePolicy(sizePolicy)
        self.pushButton_abc_r.setMinimumSize(QSize(90, 0))
        self.pushButton_abc_r.setFont(font)
        self.pushButton_abc_r.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_r.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_2.addWidget(self.pushButton_abc_r, 0, 3, 1, 1)

        self.pushButton_abc_tr_i = QPushButton(self.widget_abc_1)
        self.pushButton_abc_tr_i.setObjectName(u"pushButton_abc_tr_i")
        sizePolicy.setHeightForWidth(self.pushButton_abc_tr_i.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_tr_i.setSizePolicy(sizePolicy)
        self.pushButton_abc_tr_i.setMinimumSize(QSize(90, 0))
        self.pushButton_abc_tr_i.setFont(font)
        self.pushButton_abc_tr_i.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_tr_i.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_2.addWidget(self.pushButton_abc_tr_i, 0, 7, 1, 1)

        self.pushButton_abc_tr_g = QPushButton(self.widget_abc_1)
        self.pushButton_abc_tr_g.setObjectName(u"pushButton_abc_tr_g")
        sizePolicy.setHeightForWidth(self.pushButton_abc_tr_g.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_tr_g.setSizePolicy(sizePolicy)
        self.pushButton_abc_tr_g.setMinimumSize(QSize(90, 0))
        self.pushButton_abc_tr_g.setFont(font)
        self.pushButton_abc_tr_g.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_tr_g.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_2.addWidget(self.pushButton_abc_tr_g, 0, 10, 1, 1)


        self.gridLayout_8.addWidget(self.widget_abc_1, 1, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(293, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_4, 1, 2, 1, 1)

        self.widget_abc_2 = QWidget(self.page_abc)
        self.widget_abc_2.setObjectName(u"widget_abc_2")
        self.widget_abc_2.setFont(font)
        self.widget_abc_2.setFocusPolicy(Qt.NoFocus)
        self.widget_abc_2.setStyleSheet(u"QWidget#widget_3{background-color: transparent;}")
        self.gridLayout_3 = QGridLayout(self.widget_abc_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(8)
        self.gridLayout_3.setVerticalSpacing(0)
        self.gridLayout_3.setContentsMargins(5, 5, 5, 5)
        self.pushButton_abc_f = QPushButton(self.widget_abc_2)
        self.pushButton_abc_f.setObjectName(u"pushButton_abc_f")
        sizePolicy.setHeightForWidth(self.pushButton_abc_f.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_f.setSizePolicy(sizePolicy)
        self.pushButton_abc_f.setMinimumSize(QSize(100, 0))
        self.pushButton_abc_f.setFont(font)
        self.pushButton_abc_f.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_f.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_3.addWidget(self.pushButton_abc_f, 0, 4, 1, 1)

        self.pushButton_abc_d = QPushButton(self.widget_abc_2)
        self.pushButton_abc_d.setObjectName(u"pushButton_abc_d")
        sizePolicy.setHeightForWidth(self.pushButton_abc_d.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_d.setSizePolicy(sizePolicy)
        self.pushButton_abc_d.setMinimumSize(QSize(100, 0))
        self.pushButton_abc_d.setFont(font)
        self.pushButton_abc_d.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_d.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_3.addWidget(self.pushButton_abc_d, 0, 3, 1, 1)

        self.pushButton_abc_g = QPushButton(self.widget_abc_2)
        self.pushButton_abc_g.setObjectName(u"pushButton_abc_g")
        sizePolicy.setHeightForWidth(self.pushButton_abc_g.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_g.setSizePolicy(sizePolicy)
        self.pushButton_abc_g.setMinimumSize(QSize(100, 0))
        self.pushButton_abc_g.setFont(font)
        self.pushButton_abc_g.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_g.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_3.addWidget(self.pushButton_abc_g, 0, 5, 1, 1)

        self.pushButton_abc_k = QPushButton(self.widget_abc_2)
        self.pushButton_abc_k.setObjectName(u"pushButton_abc_k")
        sizePolicy.setHeightForWidth(self.pushButton_abc_k.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_k.setSizePolicy(sizePolicy)
        self.pushButton_abc_k.setMinimumSize(QSize(100, 0))
        self.pushButton_abc_k.setFont(font)
        self.pushButton_abc_k.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_k.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_3.addWidget(self.pushButton_abc_k, 0, 8, 1, 1)

        self.pushButton_abc_i = QPushButton(self.widget_abc_2)
        self.pushButton_abc_i.setObjectName(u"pushButton_abc_i")
        sizePolicy.setHeightForWidth(self.pushButton_abc_i.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_i.setSizePolicy(sizePolicy)
        self.pushButton_abc_i.setMinimumSize(QSize(100, 0))
        self.pushButton_abc_i.setFont(font)
        self.pushButton_abc_i.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_i.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_3.addWidget(self.pushButton_abc_i, 0, 11, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.pushButton_abc_l = QPushButton(self.widget_abc_2)
        self.pushButton_abc_l.setObjectName(u"pushButton_abc_l")
        sizePolicy.setHeightForWidth(self.pushButton_abc_l.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_l.setSizePolicy(sizePolicy)
        self.pushButton_abc_l.setMinimumSize(QSize(100, 0))
        self.pushButton_abc_l.setFont(font)
        self.pushButton_abc_l.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_l.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_3.addWidget(self.pushButton_abc_l, 0, 9, 1, 1)

        self.pushButton_abc_h = QPushButton(self.widget_abc_2)
        self.pushButton_abc_h.setObjectName(u"pushButton_abc_h")
        sizePolicy.setHeightForWidth(self.pushButton_abc_h.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_h.setSizePolicy(sizePolicy)
        self.pushButton_abc_h.setMinimumSize(QSize(100, 0))
        self.pushButton_abc_h.setFont(font)
        self.pushButton_abc_h.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_h.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_3.addWidget(self.pushButton_abc_h, 0, 6, 1, 1)

        self.pushButton_abc_a = QPushButton(self.widget_abc_2)
        self.pushButton_abc_a.setObjectName(u"pushButton_abc_a")
        sizePolicy.setHeightForWidth(self.pushButton_abc_a.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_a.setSizePolicy(sizePolicy)
        self.pushButton_abc_a.setMinimumSize(QSize(100, 0))
        self.pushButton_abc_a.setFont(font)
        self.pushButton_abc_a.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_a.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_3.addWidget(self.pushButton_abc_a, 0, 1, 1, 1)

        self.pushButton_abc_tr_s = QPushButton(self.widget_abc_2)
        self.pushButton_abc_tr_s.setObjectName(u"pushButton_abc_tr_s")
        sizePolicy.setHeightForWidth(self.pushButton_abc_tr_s.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_tr_s.setSizePolicy(sizePolicy)
        self.pushButton_abc_tr_s.setMinimumSize(QSize(100, 0))
        self.pushButton_abc_tr_s.setFont(font)
        self.pushButton_abc_tr_s.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_tr_s.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_3.addWidget(self.pushButton_abc_tr_s, 0, 10, 1, 1)

        self.pushButton_abc_s = QPushButton(self.widget_abc_2)
        self.pushButton_abc_s.setObjectName(u"pushButton_abc_s")
        sizePolicy.setHeightForWidth(self.pushButton_abc_s.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_s.setSizePolicy(sizePolicy)
        self.pushButton_abc_s.setMinimumSize(QSize(100, 0))
        self.pushButton_abc_s.setFont(font)
        self.pushButton_abc_s.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_s.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_3.addWidget(self.pushButton_abc_s, 0, 2, 1, 1)

        self.pushButton_abc_j = QPushButton(self.widget_abc_2)
        self.pushButton_abc_j.setObjectName(u"pushButton_abc_j")
        sizePolicy.setHeightForWidth(self.pushButton_abc_j.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_j.setSizePolicy(sizePolicy)
        self.pushButton_abc_j.setMinimumSize(QSize(100, 0))
        self.pushButton_abc_j.setFont(font)
        self.pushButton_abc_j.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_j.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_3.addWidget(self.pushButton_abc_j, 0, 7, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_2, 0, 12, 1, 1)


        self.gridLayout_8.addWidget(self.widget_abc_2, 2, 1, 1, 1)

        self.widget_abc_3 = QWidget(self.page_abc)
        self.widget_abc_3.setObjectName(u"widget_abc_3")
        self.widget_abc_3.setFont(font)
        self.widget_abc_3.setFocusPolicy(Qt.NoFocus)
        self.widget_abc_3.setStyleSheet(u"QWidget#widget_4{background-color: transparent;}")
        self.gridLayout_4 = QGridLayout(self.widget_abc_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setHorizontalSpacing(8)
        self.gridLayout_4.setVerticalSpacing(0)
        self.gridLayout_4.setContentsMargins(5, 5, 5, 5)
        self.pushButton_abc_m = QPushButton(self.widget_abc_3)
        self.pushButton_abc_m.setObjectName(u"pushButton_abc_m")
        sizePolicy.setHeightForWidth(self.pushButton_abc_m.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_m.setSizePolicy(sizePolicy)
        self.pushButton_abc_m.setMinimumSize(QSize(100, 0))
        self.pushButton_abc_m.setFont(font)
        self.pushButton_abc_m.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_m.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_4.addWidget(self.pushButton_abc_m, 0, 7, 1, 1)

        self.pushButton_abc_b = QPushButton(self.widget_abc_3)
        self.pushButton_abc_b.setObjectName(u"pushButton_abc_b")
        sizePolicy.setHeightForWidth(self.pushButton_abc_b.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_b.setSizePolicy(sizePolicy)
        self.pushButton_abc_b.setMinimumSize(QSize(100, 0))
        self.pushButton_abc_b.setFont(font)
        self.pushButton_abc_b.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_b.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_4.addWidget(self.pushButton_abc_b, 0, 5, 1, 1)

        self.pushButton_abc_x = QPushButton(self.widget_abc_3)
        self.pushButton_abc_x.setObjectName(u"pushButton_abc_x")
        sizePolicy.setHeightForWidth(self.pushButton_abc_x.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_x.setSizePolicy(sizePolicy)
        self.pushButton_abc_x.setMinimumSize(QSize(100, 0))
        self.pushButton_abc_x.setFont(font)
        self.pushButton_abc_x.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_x.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_4.addWidget(self.pushButton_abc_x, 0, 2, 1, 1)

        self.pushButton_abc_v = QPushButton(self.widget_abc_3)
        self.pushButton_abc_v.setObjectName(u"pushButton_abc_v")
        sizePolicy.setHeightForWidth(self.pushButton_abc_v.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_v.setSizePolicy(sizePolicy)
        self.pushButton_abc_v.setMinimumSize(QSize(100, 0))
        self.pushButton_abc_v.setFont(font)
        self.pushButton_abc_v.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_v.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_4.addWidget(self.pushButton_abc_v, 0, 4, 1, 1)

        self.pushButton_abc_n = QPushButton(self.widget_abc_3)
        self.pushButton_abc_n.setObjectName(u"pushButton_abc_n")
        sizePolicy.setHeightForWidth(self.pushButton_abc_n.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_n.setSizePolicy(sizePolicy)
        self.pushButton_abc_n.setMinimumSize(QSize(100, 0))
        self.pushButton_abc_n.setFont(font)
        self.pushButton_abc_n.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_n.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_4.addWidget(self.pushButton_abc_n, 0, 6, 1, 1)

        self.pushButton_abc_tr_o = QPushButton(self.widget_abc_3)
        self.pushButton_abc_tr_o.setObjectName(u"pushButton_abc_tr_o")
        sizePolicy.setHeightForWidth(self.pushButton_abc_tr_o.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_tr_o.setSizePolicy(sizePolicy)
        self.pushButton_abc_tr_o.setMinimumSize(QSize(100, 0))
        self.pushButton_abc_tr_o.setFont(font)
        self.pushButton_abc_tr_o.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_tr_o.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_4.addWidget(self.pushButton_abc_tr_o, 0, 8, 1, 1)

        self.pushButton_abc_c = QPushButton(self.widget_abc_3)
        self.pushButton_abc_c.setObjectName(u"pushButton_abc_c")
        sizePolicy.setHeightForWidth(self.pushButton_abc_c.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_c.setSizePolicy(sizePolicy)
        self.pushButton_abc_c.setMinimumSize(QSize(100, 0))
        self.pushButton_abc_c.setFont(font)
        self.pushButton_abc_c.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_c.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_4.addWidget(self.pushButton_abc_c, 0, 3, 1, 1)

        self.pushButton_abc_z = QPushButton(self.widget_abc_3)
        self.pushButton_abc_z.setObjectName(u"pushButton_abc_z")
        sizePolicy.setHeightForWidth(self.pushButton_abc_z.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_z.setSizePolicy(sizePolicy)
        self.pushButton_abc_z.setMinimumSize(QSize(100, 0))
        self.pushButton_abc_z.setFont(font)
        self.pushButton_abc_z.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_z.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_4.addWidget(self.pushButton_abc_z, 0, 1, 1, 1)

        self.pushButton_abc_tr_c = QPushButton(self.widget_abc_3)
        self.pushButton_abc_tr_c.setObjectName(u"pushButton_abc_tr_c")
        sizePolicy.setHeightForWidth(self.pushButton_abc_tr_c.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_tr_c.setSizePolicy(sizePolicy)
        self.pushButton_abc_tr_c.setMinimumSize(QSize(100, 0))
        self.pushButton_abc_tr_c.setFont(font)
        self.pushButton_abc_tr_c.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_tr_c.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_4.addWidget(self.pushButton_abc_tr_c, 0, 9, 1, 1)

        self.pushButton_abc_backspace = QPushButton(self.widget_abc_3)
        self.pushButton_abc_backspace.setObjectName(u"pushButton_abc_backspace")
        sizePolicy.setHeightForWidth(self.pushButton_abc_backspace.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_backspace.setSizePolicy(sizePolicy)
        self.pushButton_abc_backspace.setMinimumSize(QSize(100, 0))
        self.pushButton_abc_backspace.setFont(font)
        self.pushButton_abc_backspace.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_backspace.setStyleSheet(u"QPushButton{\n"
"background-color: transparent;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: rgba(50, 50, 50, 209);\n"
"}")
        icon = QIcon()
        icon.addFile(u":/png/png/backspace.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_abc_backspace.setIcon(icon)
        self.pushButton_abc_backspace.setIconSize(QSize(57, 57))
        self.pushButton_abc_backspace.setFlat(True)

        self.gridLayout_4.addWidget(self.pushButton_abc_backspace, 0, 10, 1, 1)

        self.pushButton_shift = QPushButton(self.widget_abc_3)
        self.pushButton_shift.setObjectName(u"pushButton_shift")
        sizePolicy.setHeightForWidth(self.pushButton_shift.sizePolicy().hasHeightForWidth())
        self.pushButton_shift.setSizePolicy(sizePolicy)
        self.pushButton_shift.setMinimumSize(QSize(100, 0))
        self.pushButton_shift.setFont(font)
        self.pushButton_shift.setFocusPolicy(Qt.NoFocus)
        self.pushButton_shift.setStyleSheet(u"QPushButton{\n"
"background-color: transparent;\n"
"image: url(:/png/png/shift_up.png);\n"
"border-radius: 15px;} \n"
"\n"
"QPushButton:checked {\n"
"image: url(:/png/png/shift_down.png);\n"
"}")
        self.pushButton_shift.setCheckable(True)

        self.gridLayout_4.addWidget(self.pushButton_shift, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.widget_abc_3, 3, 1, 1, 1)

        self.widget_abc_4 = QWidget(self.page_abc)
        self.widget_abc_4.setObjectName(u"widget_abc_4")
        self.widget_abc_4.setFont(font)
        self.widget_abc_4.setFocusPolicy(Qt.NoFocus)
        self.widget_abc_4.setStyleSheet(u"QWidget#widget_5{background-color: transparent;}")
        self.gridLayout_5 = QGridLayout(self.widget_abc_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(5)
        self.gridLayout_5.setVerticalSpacing(0)
        self.gridLayout_5.setContentsMargins(5, 5, 5, 5)
        self.pushButton_abc_enter = QPushButton(self.widget_abc_4)
        self.pushButton_abc_enter.setObjectName(u"pushButton_abc_enter")
        sizePolicy.setHeightForWidth(self.pushButton_abc_enter.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_enter.setSizePolicy(sizePolicy)
        self.pushButton_abc_enter.setMinimumSize(QSize(130, 0))
        self.pushButton_abc_enter.setFont(font)
        self.pushButton_abc_enter.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_enter.setStyleSheet(u"QPushButton{\n"
"background-color: transparent;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: rgba(50, 50, 50, 209);\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/png/png/enter.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_abc_enter.setIcon(icon1)
        self.pushButton_abc_enter.setIconSize(QSize(85, 85))
        self.pushButton_abc_enter.setFlat(True)

        self.gridLayout_5.addWidget(self.pushButton_abc_enter, 0, 4, 1, 1)

        self.pushButton_abc_dot = QPushButton(self.widget_abc_4)
        self.pushButton_abc_dot.setObjectName(u"pushButton_abc_dot")
        sizePolicy.setHeightForWidth(self.pushButton_abc_dot.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_dot.setSizePolicy(sizePolicy)
        self.pushButton_abc_dot.setMinimumSize(QSize(130, 0))
        font1 = QFont()
        font1.setFamilies([u"Ubuntu Condensed"])
        font1.setPointSize(20)
        font1.setBold(True)
        self.pushButton_abc_dot.setFont(font1)
        self.pushButton_abc_dot.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_dot.setStyleSheet(u"QPushButton{\n"
"background-color: transparent;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: rgba(50, 50, 50, 209);\n"
"}")
        self.pushButton_abc_dot.setFlat(True)

        self.gridLayout_5.addWidget(self.pushButton_abc_dot, 0, 3, 1, 1)

        self.pushButton_abc_to_123 = QPushButton(self.widget_abc_4)
        self.pushButton_abc_to_123.setObjectName(u"pushButton_abc_to_123")
        sizePolicy.setHeightForWidth(self.pushButton_abc_to_123.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_to_123.setSizePolicy(sizePolicy)
        self.pushButton_abc_to_123.setMinimumSize(QSize(130, 0))
        self.pushButton_abc_to_123.setFont(font)
        self.pushButton_abc_to_123.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_to_123.setStyleSheet(u"QPushButton{\n"
"background-color: transparent;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: rgba(50, 50, 50, 209);\n"
"}")
        self.pushButton_abc_to_123.setFlat(True)

        self.gridLayout_5.addWidget(self.pushButton_abc_to_123, 0, 0, 1, 1)

        self.pushButton_abc_comma = QPushButton(self.widget_abc_4)
        self.pushButton_abc_comma.setObjectName(u"pushButton_abc_comma")
        sizePolicy.setHeightForWidth(self.pushButton_abc_comma.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_comma.setSizePolicy(sizePolicy)
        self.pushButton_abc_comma.setMinimumSize(QSize(130, 0))
        self.pushButton_abc_comma.setFont(font1)
        self.pushButton_abc_comma.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_comma.setStyleSheet(u"QPushButton{\n"
"background-color: transparent;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: rgba(50, 50, 50, 209);\n"
"}")
        self.pushButton_abc_comma.setFlat(True)

        self.gridLayout_5.addWidget(self.pushButton_abc_comma, 0, 1, 1, 1)

        self.pushButton_abc_space = QPushButton(self.widget_abc_4)
        self.pushButton_abc_space.setObjectName(u"pushButton_abc_space")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_abc_space.sizePolicy().hasHeightForWidth())
        self.pushButton_abc_space.setSizePolicy(sizePolicy1)
        self.pushButton_abc_space.setMinimumSize(QSize(130, 0))
        self.pushButton_abc_space.setFont(font)
        self.pushButton_abc_space.setFocusPolicy(Qt.NoFocus)
        self.pushButton_abc_space.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"padding-top: 60px;\n"
"border-radius: 15px;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")
        self.pushButton_abc_space.setIconSize(QSize(100, 68))

        self.gridLayout_5.addWidget(self.pushButton_abc_space, 0, 2, 1, 1)


        self.gridLayout_8.addWidget(self.widget_abc_4, 4, 1, 1, 1)

        self.stackedWidget_keyboard_layout.addWidget(self.page_abc)
        self.page_numeric = QWidget()
        self.page_numeric.setObjectName(u"page_numeric")
        self.page_numeric.setStyleSheet(u"QWidget#page_numeric{background-color: transparent;}")
        self.gridLayout_14 = QGridLayout(self.page_numeric)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setHorizontalSpacing(0)
        self.gridLayout_14.setVerticalSpacing(5)
        self.gridLayout_14.setContentsMargins(0, 10, 0, 0)
        self.widget_123_3 = QWidget(self.page_numeric)
        self.widget_123_3.setObjectName(u"widget_123_3")
        self.widget_123_3.setFont(font)
        self.widget_123_3.setFocusPolicy(Qt.NoFocus)
        self.widget_123_3.setStyleSheet(u"QWidget#widget_5{background-color: transparent;}")
        self.gridLayout_12 = QGridLayout(self.widget_123_3)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setHorizontalSpacing(5)
        self.gridLayout_12.setVerticalSpacing(0)
        self.gridLayout_12.setContentsMargins(5, 5, 5, 5)
        self.pushButton_123_enter = QPushButton(self.widget_123_3)
        self.pushButton_123_enter.setObjectName(u"pushButton_123_enter")
        sizePolicy.setHeightForWidth(self.pushButton_123_enter.sizePolicy().hasHeightForWidth())
        self.pushButton_123_enter.setSizePolicy(sizePolicy)
        self.pushButton_123_enter.setMinimumSize(QSize(130, 0))
        self.pushButton_123_enter.setFont(font)
        self.pushButton_123_enter.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_enter.setStyleSheet(u"QPushButton{\n"
"background-color: transparent;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: rgba(50, 50, 50, 209);\n"
"}")
        self.pushButton_123_enter.setIcon(icon1)
        self.pushButton_123_enter.setIconSize(QSize(85, 85))
        self.pushButton_123_enter.setFlat(True)

        self.gridLayout_12.addWidget(self.pushButton_123_enter, 0, 4, 1, 1)

        self.pushButton_123_dot = QPushButton(self.widget_123_3)
        self.pushButton_123_dot.setObjectName(u"pushButton_123_dot")
        sizePolicy.setHeightForWidth(self.pushButton_123_dot.sizePolicy().hasHeightForWidth())
        self.pushButton_123_dot.setSizePolicy(sizePolicy)
        self.pushButton_123_dot.setMinimumSize(QSize(130, 0))
        self.pushButton_123_dot.setFont(font1)
        self.pushButton_123_dot.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_dot.setStyleSheet(u"QPushButton{\n"
"background-color: transparent;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: rgba(50, 50, 50, 209);\n"
"}")
        self.pushButton_123_dot.setFlat(True)

        self.gridLayout_12.addWidget(self.pushButton_123_dot, 0, 3, 1, 1)

        self.pushButton_123_to_abc = QPushButton(self.widget_123_3)
        self.pushButton_123_to_abc.setObjectName(u"pushButton_123_to_abc")
        sizePolicy.setHeightForWidth(self.pushButton_123_to_abc.sizePolicy().hasHeightForWidth())
        self.pushButton_123_to_abc.setSizePolicy(sizePolicy)
        self.pushButton_123_to_abc.setMinimumSize(QSize(130, 0))
        self.pushButton_123_to_abc.setFont(font)
        self.pushButton_123_to_abc.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_to_abc.setStyleSheet(u"QPushButton{\n"
"background-color: transparent;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: rgba(50, 50, 50, 209);\n"
"}")
        self.pushButton_123_to_abc.setFlat(True)

        self.gridLayout_12.addWidget(self.pushButton_123_to_abc, 0, 0, 1, 1)

        self.pushButton_123_comma = QPushButton(self.widget_123_3)
        self.pushButton_123_comma.setObjectName(u"pushButton_123_comma")
        sizePolicy.setHeightForWidth(self.pushButton_123_comma.sizePolicy().hasHeightForWidth())
        self.pushButton_123_comma.setSizePolicy(sizePolicy)
        self.pushButton_123_comma.setMinimumSize(QSize(130, 0))
        self.pushButton_123_comma.setFont(font1)
        self.pushButton_123_comma.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_comma.setStyleSheet(u"QPushButton{\n"
"background-color: transparent;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: rgba(50, 50, 50, 209);\n"
"}")
        self.pushButton_123_comma.setFlat(True)

        self.gridLayout_12.addWidget(self.pushButton_123_comma, 0, 1, 1, 1)

        self.pushButton_123_space = QPushButton(self.widget_123_3)
        self.pushButton_123_space.setObjectName(u"pushButton_123_space")
        sizePolicy1.setHeightForWidth(self.pushButton_123_space.sizePolicy().hasHeightForWidth())
        self.pushButton_123_space.setSizePolicy(sizePolicy1)
        self.pushButton_123_space.setMinimumSize(QSize(130, 0))
        self.pushButton_123_space.setFont(font)
        self.pushButton_123_space.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_space.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"padding-top: 60px;\n"
"border-radius: 15px;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")
        self.pushButton_123_space.setIconSize(QSize(100, 68))

        self.gridLayout_12.addWidget(self.pushButton_123_space, 0, 2, 1, 1)


        self.gridLayout_14.addWidget(self.widget_123_3, 3, 1, 1, 1)

        self.widget_123_2 = QWidget(self.page_numeric)
        self.widget_123_2.setObjectName(u"widget_123_2")
        self.widget_123_2.setFont(font)
        self.widget_123_2.setFocusPolicy(Qt.NoFocus)
        self.widget_123_2.setStyleSheet(u"QWidget#widget_4{background-color: transparent;}")
        self.gridLayout_9 = QGridLayout(self.widget_123_2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setHorizontalSpacing(8)
        self.gridLayout_9.setVerticalSpacing(0)
        self.gridLayout_9.setContentsMargins(5, 5, 5, 5)
        self.pushButton_123_forward_slash = QPushButton(self.widget_123_2)
        self.pushButton_123_forward_slash.setObjectName(u"pushButton_123_forward_slash")
        sizePolicy.setHeightForWidth(self.pushButton_123_forward_slash.sizePolicy().hasHeightForWidth())
        self.pushButton_123_forward_slash.setSizePolicy(sizePolicy)
        self.pushButton_123_forward_slash.setMinimumSize(QSize(100, 0))
        self.pushButton_123_forward_slash.setFont(font)
        self.pushButton_123_forward_slash.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_forward_slash.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_9.addWidget(self.pushButton_123_forward_slash, 0, 5, 1, 1)

        self.pushButton_123_single_quote = QPushButton(self.widget_123_2)
        self.pushButton_123_single_quote.setObjectName(u"pushButton_123_single_quote")
        sizePolicy.setHeightForWidth(self.pushButton_123_single_quote.sizePolicy().hasHeightForWidth())
        self.pushButton_123_single_quote.setSizePolicy(sizePolicy)
        self.pushButton_123_single_quote.setMinimumSize(QSize(100, 0))
        self.pushButton_123_single_quote.setFont(font)
        self.pushButton_123_single_quote.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_single_quote.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_9.addWidget(self.pushButton_123_single_quote, 0, 3, 1, 1)

        self.pushButton_123_colon = QPushButton(self.widget_123_2)
        self.pushButton_123_colon.setObjectName(u"pushButton_123_colon")
        sizePolicy.setHeightForWidth(self.pushButton_123_colon.sizePolicy().hasHeightForWidth())
        self.pushButton_123_colon.setSizePolicy(sizePolicy)
        self.pushButton_123_colon.setMinimumSize(QSize(100, 0))
        self.pushButton_123_colon.setFont(font)
        self.pushButton_123_colon.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_colon.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_9.addWidget(self.pushButton_123_colon, 0, 4, 1, 1)

        self.pushButton_123_plus = QPushButton(self.widget_123_2)
        self.pushButton_123_plus.setObjectName(u"pushButton_123_plus")
        sizePolicy.setHeightForWidth(self.pushButton_123_plus.sizePolicy().hasHeightForWidth())
        self.pushButton_123_plus.setSizePolicy(sizePolicy)
        self.pushButton_123_plus.setMinimumSize(QSize(100, 0))
        self.pushButton_123_plus.setFont(font)
        self.pushButton_123_plus.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_plus.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_9.addWidget(self.pushButton_123_plus, 0, 8, 1, 1)

        self.pushButton_123_backspace = QPushButton(self.widget_123_2)
        self.pushButton_123_backspace.setObjectName(u"pushButton_123_backspace")
        sizePolicy.setHeightForWidth(self.pushButton_123_backspace.sizePolicy().hasHeightForWidth())
        self.pushButton_123_backspace.setSizePolicy(sizePolicy)
        self.pushButton_123_backspace.setMinimumSize(QSize(100, 0))
        self.pushButton_123_backspace.setFont(font)
        self.pushButton_123_backspace.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_backspace.setStyleSheet(u"QPushButton{\n"
"background-color: transparent;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: rgba(50, 50, 50, 209);\n"
"}")
        self.pushButton_123_backspace.setIcon(icon)
        self.pushButton_123_backspace.setIconSize(QSize(68, 68))
        self.pushButton_123_backspace.setFlat(True)

        self.gridLayout_9.addWidget(self.pushButton_123_backspace, 0, 9, 1, 1)

        self.pushButton_123_question = QPushButton(self.widget_123_2)
        self.pushButton_123_question.setObjectName(u"pushButton_123_question")
        sizePolicy.setHeightForWidth(self.pushButton_123_question.sizePolicy().hasHeightForWidth())
        self.pushButton_123_question.setSizePolicy(sizePolicy)
        self.pushButton_123_question.setMinimumSize(QSize(100, 0))
        self.pushButton_123_question.setFont(font)
        self.pushButton_123_question.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_question.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_9.addWidget(self.pushButton_123_question, 0, 7, 1, 1)

        self.pushButton_123_double_quote = QPushButton(self.widget_123_2)
        self.pushButton_123_double_quote.setObjectName(u"pushButton_123_double_quote")
        sizePolicy.setHeightForWidth(self.pushButton_123_double_quote.sizePolicy().hasHeightForWidth())
        self.pushButton_123_double_quote.setSizePolicy(sizePolicy)
        self.pushButton_123_double_quote.setMinimumSize(QSize(100, 0))
        self.pushButton_123_double_quote.setFont(font)
        self.pushButton_123_double_quote.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_double_quote.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_9.addWidget(self.pushButton_123_double_quote, 0, 1, 1, 1)

        self.pushButton_123_exclamation = QPushButton(self.widget_123_2)
        self.pushButton_123_exclamation.setObjectName(u"pushButton_123_exclamation")
        sizePolicy.setHeightForWidth(self.pushButton_123_exclamation.sizePolicy().hasHeightForWidth())
        self.pushButton_123_exclamation.setSizePolicy(sizePolicy)
        self.pushButton_123_exclamation.setMinimumSize(QSize(100, 0))
        self.pushButton_123_exclamation.setFont(font)
        self.pushButton_123_exclamation.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_exclamation.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_9.addWidget(self.pushButton_123_exclamation, 0, 6, 1, 1)

        self.pushButton_123_star = QPushButton(self.widget_123_2)
        self.pushButton_123_star.setObjectName(u"pushButton_123_star")
        sizePolicy.setHeightForWidth(self.pushButton_123_star.sizePolicy().hasHeightForWidth())
        self.pushButton_123_star.setSizePolicy(sizePolicy)
        self.pushButton_123_star.setMinimumSize(QSize(100, 0))
        self.pushButton_123_star.setFont(font)
        self.pushButton_123_star.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_star.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_9.addWidget(self.pushButton_123_star, 0, 2, 1, 1)

        self.pushButton_123_to_symbols = QPushButton(self.widget_123_2)
        self.pushButton_123_to_symbols.setObjectName(u"pushButton_123_to_symbols")
        sizePolicy.setHeightForWidth(self.pushButton_123_to_symbols.sizePolicy().hasHeightForWidth())
        self.pushButton_123_to_symbols.setSizePolicy(sizePolicy)
        self.pushButton_123_to_symbols.setMinimumSize(QSize(130, 0))
        self.pushButton_123_to_symbols.setFont(font)
        self.pushButton_123_to_symbols.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_to_symbols.setStyleSheet(u"QPushButton{\n"
"background-color: transparent;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: rgba(50, 50, 50, 209);\n"
"}")
        self.pushButton_123_to_symbols.setFlat(True)

        self.gridLayout_9.addWidget(self.pushButton_123_to_symbols, 0, 0, 1, 1)


        self.gridLayout_14.addWidget(self.widget_123_2, 2, 1, 1, 1)

        self.widget_123_1 = QWidget(self.page_numeric)
        self.widget_123_1.setObjectName(u"widget_123_1")
        self.widget_123_1.setFont(font)
        self.widget_123_1.setFocusPolicy(Qt.NoFocus)
        self.widget_123_1.setStyleSheet(u"QWidget#widget_2{background-color: transparent;}")
        self.gridLayout_11 = QGridLayout(self.widget_123_1)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setHorizontalSpacing(8)
        self.gridLayout_11.setVerticalSpacing(0)
        self.gridLayout_11.setContentsMargins(5, 5, 5, 5)
        self.pushButton_123_at = QPushButton(self.widget_123_1)
        self.pushButton_123_at.setObjectName(u"pushButton_123_at")
        sizePolicy.setHeightForWidth(self.pushButton_123_at.sizePolicy().hasHeightForWidth())
        self.pushButton_123_at.setSizePolicy(sizePolicy)
        self.pushButton_123_at.setMinimumSize(QSize(90, 0))
        self.pushButton_123_at.setFont(font)
        self.pushButton_123_at.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_at.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_11.addWidget(self.pushButton_123_at, 0, 0, 1, 1)

        self.pushButton_123_underscore = QPushButton(self.widget_123_1)
        self.pushButton_123_underscore.setObjectName(u"pushButton_123_underscore")
        sizePolicy.setHeightForWidth(self.pushButton_123_underscore.sizePolicy().hasHeightForWidth())
        self.pushButton_123_underscore.setSizePolicy(sizePolicy)
        self.pushButton_123_underscore.setMinimumSize(QSize(90, 0))
        self.pushButton_123_underscore.setFont(font)
        self.pushButton_123_underscore.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_underscore.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_11.addWidget(self.pushButton_123_underscore, 0, 3, 1, 1)

        self.pushButton_123_hash = QPushButton(self.widget_123_1)
        self.pushButton_123_hash.setObjectName(u"pushButton_123_hash")
        sizePolicy.setHeightForWidth(self.pushButton_123_hash.sizePolicy().hasHeightForWidth())
        self.pushButton_123_hash.setSizePolicy(sizePolicy)
        self.pushButton_123_hash.setMinimumSize(QSize(90, 0))
        self.pushButton_123_hash.setFont(font)
        self.pushButton_123_hash.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_hash.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_11.addWidget(self.pushButton_123_hash, 0, 1, 1, 1)

        self.pushButton_123_hyphen = QPushButton(self.widget_123_1)
        self.pushButton_123_hyphen.setObjectName(u"pushButton_123_hyphen")
        sizePolicy.setHeightForWidth(self.pushButton_123_hyphen.sizePolicy().hasHeightForWidth())
        self.pushButton_123_hyphen.setSizePolicy(sizePolicy)
        self.pushButton_123_hyphen.setMinimumSize(QSize(90, 0))
        self.pushButton_123_hyphen.setFont(font)
        self.pushButton_123_hyphen.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_hyphen.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_11.addWidget(self.pushButton_123_hyphen, 0, 4, 1, 1)

        self.pushButton_123_right_parenthesis = QPushButton(self.widget_123_1)
        self.pushButton_123_right_parenthesis.setObjectName(u"pushButton_123_right_parenthesis")
        sizePolicy.setHeightForWidth(self.pushButton_123_right_parenthesis.sizePolicy().hasHeightForWidth())
        self.pushButton_123_right_parenthesis.setSizePolicy(sizePolicy)
        self.pushButton_123_right_parenthesis.setMinimumSize(QSize(90, 0))
        self.pushButton_123_right_parenthesis.setFont(font)
        self.pushButton_123_right_parenthesis.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_right_parenthesis.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_11.addWidget(self.pushButton_123_right_parenthesis, 0, 6, 1, 1)

        self.pushButton_123_left_parenthesis = QPushButton(self.widget_123_1)
        self.pushButton_123_left_parenthesis.setObjectName(u"pushButton_123_left_parenthesis")
        sizePolicy.setHeightForWidth(self.pushButton_123_left_parenthesis.sizePolicy().hasHeightForWidth())
        self.pushButton_123_left_parenthesis.setSizePolicy(sizePolicy)
        self.pushButton_123_left_parenthesis.setMinimumSize(QSize(90, 0))
        self.pushButton_123_left_parenthesis.setFont(font)
        self.pushButton_123_left_parenthesis.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_left_parenthesis.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_11.addWidget(self.pushButton_123_left_parenthesis, 0, 5, 1, 1)

        self.pushButton_123_percent = QPushButton(self.widget_123_1)
        self.pushButton_123_percent.setObjectName(u"pushButton_123_percent")
        sizePolicy.setHeightForWidth(self.pushButton_123_percent.sizePolicy().hasHeightForWidth())
        self.pushButton_123_percent.setSizePolicy(sizePolicy)
        self.pushButton_123_percent.setMinimumSize(QSize(90, 0))
        self.pushButton_123_percent.setFont(font)
        self.pushButton_123_percent.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_percent.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_11.addWidget(self.pushButton_123_percent, 0, 8, 1, 1)

        self.pushButton_123_ampersand = QPushButton(self.widget_123_1)
        self.pushButton_123_ampersand.setObjectName(u"pushButton_123_ampersand")
        sizePolicy.setHeightForWidth(self.pushButton_123_ampersand.sizePolicy().hasHeightForWidth())
        self.pushButton_123_ampersand.setSizePolicy(sizePolicy)
        self.pushButton_123_ampersand.setMinimumSize(QSize(90, 0))
        self.pushButton_123_ampersand.setFont(font)
        self.pushButton_123_ampersand.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_ampersand.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_11.addWidget(self.pushButton_123_ampersand, 0, 2, 1, 1)

        self.pushButton_123_equal = QPushButton(self.widget_123_1)
        self.pushButton_123_equal.setObjectName(u"pushButton_123_equal")
        sizePolicy.setHeightForWidth(self.pushButton_123_equal.sizePolicy().hasHeightForWidth())
        self.pushButton_123_equal.setSizePolicy(sizePolicy)
        self.pushButton_123_equal.setMinimumSize(QSize(90, 0))
        self.pushButton_123_equal.setFont(font)
        self.pushButton_123_equal.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_equal.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_11.addWidget(self.pushButton_123_equal, 0, 7, 1, 1)

        self.pushButton_123_tl = QPushButton(self.widget_123_1)
        self.pushButton_123_tl.setObjectName(u"pushButton_123_tl")
        sizePolicy.setHeightForWidth(self.pushButton_123_tl.sizePolicy().hasHeightForWidth())
        self.pushButton_123_tl.setSizePolicy(sizePolicy)
        self.pushButton_123_tl.setMinimumSize(QSize(90, 0))
        self.pushButton_123_tl.setFont(font)
        self.pushButton_123_tl.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_tl.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_11.addWidget(self.pushButton_123_tl, 0, 9, 1, 1)


        self.gridLayout_14.addWidget(self.widget_123_1, 1, 1, 1, 1)

        self.widget_numeric_button_123 = QWidget(self.page_numeric)
        self.widget_numeric_button_123.setObjectName(u"widget_numeric_button_123")
        self.widget_numeric_button_123.setFont(font)
        self.widget_numeric_button_123.setFocusPolicy(Qt.NoFocus)
        self.widget_numeric_button_123.setStyleSheet(u"QWidget#widget{background-color: transparent;}")
        self.gridLayout_10 = QGridLayout(self.widget_numeric_button_123)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setHorizontalSpacing(9)
        self.gridLayout_10.setVerticalSpacing(0)
        self.gridLayout_10.setContentsMargins(5, 5, 5, 5)
        self.pushButton_123_1 = QPushButton(self.widget_numeric_button_123)
        self.pushButton_123_1.setObjectName(u"pushButton_123_1")
        sizePolicy.setHeightForWidth(self.pushButton_123_1.sizePolicy().hasHeightForWidth())
        self.pushButton_123_1.setSizePolicy(sizePolicy)
        self.pushButton_123_1.setMinimumSize(QSize(110, 0))
        self.pushButton_123_1.setFont(font)
        self.pushButton_123_1.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_1.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_10.addWidget(self.pushButton_123_1, 0, 0, 1, 1)

        self.pushButton_123_2 = QPushButton(self.widget_numeric_button_123)
        self.pushButton_123_2.setObjectName(u"pushButton_123_2")
        sizePolicy.setHeightForWidth(self.pushButton_123_2.sizePolicy().hasHeightForWidth())
        self.pushButton_123_2.setSizePolicy(sizePolicy)
        self.pushButton_123_2.setMinimumSize(QSize(110, 0))
        self.pushButton_123_2.setFont(font)
        self.pushButton_123_2.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_2.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_10.addWidget(self.pushButton_123_2, 0, 1, 1, 1)

        self.pushButton_123_3 = QPushButton(self.widget_numeric_button_123)
        self.pushButton_123_3.setObjectName(u"pushButton_123_3")
        sizePolicy.setHeightForWidth(self.pushButton_123_3.sizePolicy().hasHeightForWidth())
        self.pushButton_123_3.setSizePolicy(sizePolicy)
        self.pushButton_123_3.setMinimumSize(QSize(110, 0))
        self.pushButton_123_3.setFont(font)
        self.pushButton_123_3.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_3.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_10.addWidget(self.pushButton_123_3, 0, 2, 1, 1)

        self.pushButton_123_4 = QPushButton(self.widget_numeric_button_123)
        self.pushButton_123_4.setObjectName(u"pushButton_123_4")
        sizePolicy.setHeightForWidth(self.pushButton_123_4.sizePolicy().hasHeightForWidth())
        self.pushButton_123_4.setSizePolicy(sizePolicy)
        self.pushButton_123_4.setMinimumSize(QSize(110, 0))
        self.pushButton_123_4.setFont(font)
        self.pushButton_123_4.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_4.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_10.addWidget(self.pushButton_123_4, 0, 3, 1, 1)

        self.pushButton_123_5 = QPushButton(self.widget_numeric_button_123)
        self.pushButton_123_5.setObjectName(u"pushButton_123_5")
        sizePolicy.setHeightForWidth(self.pushButton_123_5.sizePolicy().hasHeightForWidth())
        self.pushButton_123_5.setSizePolicy(sizePolicy)
        self.pushButton_123_5.setMinimumSize(QSize(110, 0))
        self.pushButton_123_5.setFont(font)
        self.pushButton_123_5.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_5.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_10.addWidget(self.pushButton_123_5, 0, 4, 1, 1)

        self.pushButton_123_6 = QPushButton(self.widget_numeric_button_123)
        self.pushButton_123_6.setObjectName(u"pushButton_123_6")
        sizePolicy.setHeightForWidth(self.pushButton_123_6.sizePolicy().hasHeightForWidth())
        self.pushButton_123_6.setSizePolicy(sizePolicy)
        self.pushButton_123_6.setMinimumSize(QSize(110, 0))
        self.pushButton_123_6.setFont(font)
        self.pushButton_123_6.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_6.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_10.addWidget(self.pushButton_123_6, 0, 5, 1, 1)

        self.pushButton_123_7 = QPushButton(self.widget_numeric_button_123)
        self.pushButton_123_7.setObjectName(u"pushButton_123_7")
        sizePolicy.setHeightForWidth(self.pushButton_123_7.sizePolicy().hasHeightForWidth())
        self.pushButton_123_7.setSizePolicy(sizePolicy)
        self.pushButton_123_7.setMinimumSize(QSize(110, 0))
        self.pushButton_123_7.setFont(font)
        self.pushButton_123_7.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_7.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_10.addWidget(self.pushButton_123_7, 0, 6, 1, 1)

        self.pushButton_123_8 = QPushButton(self.widget_numeric_button_123)
        self.pushButton_123_8.setObjectName(u"pushButton_123_8")
        sizePolicy.setHeightForWidth(self.pushButton_123_8.sizePolicy().hasHeightForWidth())
        self.pushButton_123_8.setSizePolicy(sizePolicy)
        self.pushButton_123_8.setMinimumSize(QSize(110, 0))
        self.pushButton_123_8.setFont(font)
        self.pushButton_123_8.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_8.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_10.addWidget(self.pushButton_123_8, 0, 7, 1, 1)

        self.pushButton_123_9 = QPushButton(self.widget_numeric_button_123)
        self.pushButton_123_9.setObjectName(u"pushButton_123_9")
        sizePolicy.setHeightForWidth(self.pushButton_123_9.sizePolicy().hasHeightForWidth())
        self.pushButton_123_9.setSizePolicy(sizePolicy)
        self.pushButton_123_9.setMinimumSize(QSize(110, 0))
        self.pushButton_123_9.setFont(font)
        self.pushButton_123_9.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_9.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_10.addWidget(self.pushButton_123_9, 0, 8, 1, 1)

        self.pushButton_123_0 = QPushButton(self.widget_numeric_button_123)
        self.pushButton_123_0.setObjectName(u"pushButton_123_0")
        sizePolicy.setHeightForWidth(self.pushButton_123_0.sizePolicy().hasHeightForWidth())
        self.pushButton_123_0.setSizePolicy(sizePolicy)
        self.pushButton_123_0.setMinimumSize(QSize(110, 0))
        self.pushButton_123_0.setFont(font)
        self.pushButton_123_0.setFocusPolicy(Qt.NoFocus)
        self.pushButton_123_0.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_10.addWidget(self.pushButton_123_0, 0, 9, 1, 1)


        self.gridLayout_14.addWidget(self.widget_numeric_button_123, 0, 1, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(360, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_11, 1, 2, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(361, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_6, 1, 0, 1, 1)

        self.stackedWidget_keyboard_layout.addWidget(self.page_numeric)
        self.page_symbol = QWidget()
        self.page_symbol.setObjectName(u"page_symbol")
        self.page_symbol.setStyleSheet(u"QWidget#page_symbol{background-color: transparent;}")
        self.gridLayout_19 = QGridLayout(self.page_symbol)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_19.setHorizontalSpacing(0)
        self.gridLayout_19.setVerticalSpacing(5)
        self.gridLayout_19.setContentsMargins(0, 10, 0, 0)
        self.widget_sym_1 = QWidget(self.page_symbol)
        self.widget_sym_1.setObjectName(u"widget_sym_1")
        self.widget_sym_1.setFont(font)
        self.widget_sym_1.setFocusPolicy(Qt.NoFocus)
        self.widget_sym_1.setStyleSheet(u"QWidget#widget{background-color: transparent;}")
        self.gridLayout_15 = QGridLayout(self.widget_sym_1)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setHorizontalSpacing(9)
        self.gridLayout_15.setVerticalSpacing(0)
        self.gridLayout_15.setContentsMargins(5, 5, 5, 5)
        self.pushButton_sym_three_quarter = QPushButton(self.widget_sym_1)
        self.pushButton_sym_three_quarter.setObjectName(u"pushButton_sym_three_quarter")
        sizePolicy.setHeightForWidth(self.pushButton_sym_three_quarter.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_three_quarter.setSizePolicy(sizePolicy)
        self.pushButton_sym_three_quarter.setMinimumSize(QSize(110, 0))
        self.pushButton_sym_three_quarter.setFont(font)
        self.pushButton_sym_three_quarter.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_three_quarter.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_15.addWidget(self.pushButton_sym_three_quarter, 0, 10, 1, 1)

        self.pushButton_sym_plus = QPushButton(self.widget_sym_1)
        self.pushButton_sym_plus.setObjectName(u"pushButton_sym_plus")
        sizePolicy.setHeightForWidth(self.pushButton_sym_plus.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_plus.setSizePolicy(sizePolicy)
        self.pushButton_sym_plus.setMinimumSize(QSize(110, 0))
        self.pushButton_sym_plus.setFont(font)
        self.pushButton_sym_plus.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_plus.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_15.addWidget(self.pushButton_sym_plus, 0, 5, 1, 1)

        self.pushButton_sym_dollar = QPushButton(self.widget_sym_1)
        self.pushButton_sym_dollar.setObjectName(u"pushButton_sym_dollar")
        sizePolicy.setHeightForWidth(self.pushButton_sym_dollar.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_dollar.setSizePolicy(sizePolicy)
        self.pushButton_sym_dollar.setMinimumSize(QSize(110, 0))
        self.pushButton_sym_dollar.setFont(font)
        self.pushButton_sym_dollar.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_dollar.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_15.addWidget(self.pushButton_sym_dollar, 0, 6, 1, 1)

        self.pushButton_sym_euro = QPushButton(self.widget_sym_1)
        self.pushButton_sym_euro.setObjectName(u"pushButton_sym_euro")
        sizePolicy.setHeightForWidth(self.pushButton_sym_euro.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_euro.setSizePolicy(sizePolicy)
        self.pushButton_sym_euro.setMinimumSize(QSize(100, 0))
        self.pushButton_sym_euro.setFont(font)
        self.pushButton_sym_euro.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_euro.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_15.addWidget(self.pushButton_sym_euro, 0, 7, 1, 1)

        self.pushButton_sym_double_quote = QPushButton(self.widget_sym_1)
        self.pushButton_sym_double_quote.setObjectName(u"pushButton_sym_double_quote")
        sizePolicy.setHeightForWidth(self.pushButton_sym_double_quote.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_double_quote.setSizePolicy(sizePolicy)
        self.pushButton_sym_double_quote.setMinimumSize(QSize(110, 0))
        self.pushButton_sym_double_quote.setFont(font)
        self.pushButton_sym_double_quote.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_double_quote.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_15.addWidget(self.pushButton_sym_double_quote, 0, 0, 1, 1)

        self.pushButton_sym_one_half = QPushButton(self.widget_sym_1)
        self.pushButton_sym_one_half.setObjectName(u"pushButton_sym_one_half")
        sizePolicy.setHeightForWidth(self.pushButton_sym_one_half.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_one_half.setSizePolicy(sizePolicy)
        self.pushButton_sym_one_half.setMinimumSize(QSize(110, 0))
        self.pushButton_sym_one_half.setFont(font)
        self.pushButton_sym_one_half.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_one_half.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_15.addWidget(self.pushButton_sym_one_half, 0, 9, 1, 1)

        self.pushButton_sym_hash = QPushButton(self.widget_sym_1)
        self.pushButton_sym_hash.setObjectName(u"pushButton_sym_hash")
        sizePolicy.setHeightForWidth(self.pushButton_sym_hash.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_hash.setSizePolicy(sizePolicy)
        self.pushButton_sym_hash.setMinimumSize(QSize(110, 0))
        self.pushButton_sym_hash.setFont(font)
        self.pushButton_sym_hash.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_hash.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_15.addWidget(self.pushButton_sym_hash, 0, 4, 1, 1)

        self.pushButton_sym_percent = QPushButton(self.widget_sym_1)
        self.pushButton_sym_percent.setObjectName(u"pushButton_sym_percent")
        sizePolicy.setHeightForWidth(self.pushButton_sym_percent.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_percent.setSizePolicy(sizePolicy)
        self.pushButton_sym_percent.setMinimumSize(QSize(110, 0))
        self.pushButton_sym_percent.setFont(font)
        self.pushButton_sym_percent.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_percent.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_15.addWidget(self.pushButton_sym_percent, 0, 8, 1, 1)

        self.pushButton_sym_exclamation = QPushButton(self.widget_sym_1)
        self.pushButton_sym_exclamation.setObjectName(u"pushButton_sym_exclamation")
        sizePolicy.setHeightForWidth(self.pushButton_sym_exclamation.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_exclamation.setSizePolicy(sizePolicy)
        self.pushButton_sym_exclamation.setMinimumSize(QSize(110, 0))
        self.pushButton_sym_exclamation.setFont(font)
        self.pushButton_sym_exclamation.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_exclamation.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_15.addWidget(self.pushButton_sym_exclamation, 0, 1, 1, 1)

        self.pushButton_sym_caret = QPushButton(self.widget_sym_1)
        self.pushButton_sym_caret.setObjectName(u"pushButton_sym_caret")
        sizePolicy.setHeightForWidth(self.pushButton_sym_caret.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_caret.setSizePolicy(sizePolicy)
        self.pushButton_sym_caret.setMinimumSize(QSize(110, 0))
        self.pushButton_sym_caret.setFont(font)
        self.pushButton_sym_caret.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_caret.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_15.addWidget(self.pushButton_sym_caret, 0, 3, 1, 1)

        self.pushButton_sym_single_quote = QPushButton(self.widget_sym_1)
        self.pushButton_sym_single_quote.setObjectName(u"pushButton_sym_single_quote")
        sizePolicy.setHeightForWidth(self.pushButton_sym_single_quote.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_single_quote.setSizePolicy(sizePolicy)
        self.pushButton_sym_single_quote.setMinimumSize(QSize(110, 0))
        self.pushButton_sym_single_quote.setFont(font)
        self.pushButton_sym_single_quote.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_single_quote.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_15.addWidget(self.pushButton_sym_single_quote, 0, 2, 1, 1)


        self.gridLayout_19.addWidget(self.widget_sym_1, 0, 1, 1, 1)

        self.widget_sym_2 = QWidget(self.page_symbol)
        self.widget_sym_2.setObjectName(u"widget_sym_2")
        self.widget_sym_2.setFont(font)
        self.widget_sym_2.setFocusPolicy(Qt.NoFocus)
        self.widget_sym_2.setStyleSheet(u"QWidget#widget_2{background-color: transparent;}")
        self.gridLayout_16 = QGridLayout(self.widget_sym_2)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setHorizontalSpacing(8)
        self.gridLayout_16.setVerticalSpacing(0)
        self.gridLayout_16.setContentsMargins(5, 5, 5, 5)
        self.pushButton_sym_backslash = QPushButton(self.widget_sym_2)
        self.pushButton_sym_backslash.setObjectName(u"pushButton_sym_backslash")
        sizePolicy.setHeightForWidth(self.pushButton_sym_backslash.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_backslash.setSizePolicy(sizePolicy)
        self.pushButton_sym_backslash.setMinimumSize(QSize(90, 0))
        self.pushButton_sym_backslash.setFont(font)
        self.pushButton_sym_backslash.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_backslash.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_16.addWidget(self.pushButton_sym_backslash, 0, 11, 1, 1)

        self.pushButton_sym_question = QPushButton(self.widget_sym_2)
        self.pushButton_sym_question.setObjectName(u"pushButton_sym_question")
        sizePolicy.setHeightForWidth(self.pushButton_sym_question.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_question.setSizePolicy(sizePolicy)
        self.pushButton_sym_question.setMinimumSize(QSize(90, 0))
        self.pushButton_sym_question.setFont(font)
        self.pushButton_sym_question.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_question.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_16.addWidget(self.pushButton_sym_question, 0, 9, 1, 1)

        self.pushButton_sym_right_parenthesis = QPushButton(self.widget_sym_2)
        self.pushButton_sym_right_parenthesis.setObjectName(u"pushButton_sym_right_parenthesis")
        sizePolicy.setHeightForWidth(self.pushButton_sym_right_parenthesis.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_right_parenthesis.setSizePolicy(sizePolicy)
        self.pushButton_sym_right_parenthesis.setMinimumSize(QSize(90, 0))
        self.pushButton_sym_right_parenthesis.setFont(font)
        self.pushButton_sym_right_parenthesis.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_right_parenthesis.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_16.addWidget(self.pushButton_sym_right_parenthesis, 0, 5, 1, 1)

        self.pushButton_sym_left_curly_brace = QPushButton(self.widget_sym_2)
        self.pushButton_sym_left_curly_brace.setObjectName(u"pushButton_sym_left_curly_brace")
        sizePolicy.setHeightForWidth(self.pushButton_sym_left_curly_brace.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_left_curly_brace.setSizePolicy(sizePolicy)
        self.pushButton_sym_left_curly_brace.setMinimumSize(QSize(90, 0))
        self.pushButton_sym_left_curly_brace.setFont(font)
        self.pushButton_sym_left_curly_brace.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_left_curly_brace.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_16.addWidget(self.pushButton_sym_left_curly_brace, 0, 2, 1, 1)

        self.pushButton_sym_left_parenthesis = QPushButton(self.widget_sym_2)
        self.pushButton_sym_left_parenthesis.setObjectName(u"pushButton_sym_left_parenthesis")
        sizePolicy.setHeightForWidth(self.pushButton_sym_left_parenthesis.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_left_parenthesis.setSizePolicy(sizePolicy)
        self.pushButton_sym_left_parenthesis.setMinimumSize(QSize(90, 0))
        self.pushButton_sym_left_parenthesis.setFont(font)
        self.pushButton_sym_left_parenthesis.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_left_parenthesis.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_16.addWidget(self.pushButton_sym_left_parenthesis, 0, 4, 1, 1)

        self.pushButton_sym_equal = QPushButton(self.widget_sym_2)
        self.pushButton_sym_equal.setObjectName(u"pushButton_sym_equal")
        sizePolicy.setHeightForWidth(self.pushButton_sym_equal.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_equal.setSizePolicy(sizePolicy)
        self.pushButton_sym_equal.setMinimumSize(QSize(90, 0))
        self.pushButton_sym_equal.setFont(font)
        self.pushButton_sym_equal.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_equal.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_16.addWidget(self.pushButton_sym_equal, 0, 8, 1, 1)

        self.pushButton_sym_forward_slash = QPushButton(self.widget_sym_2)
        self.pushButton_sym_forward_slash.setObjectName(u"pushButton_sym_forward_slash")
        sizePolicy.setHeightForWidth(self.pushButton_sym_forward_slash.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_forward_slash.setSizePolicy(sizePolicy)
        self.pushButton_sym_forward_slash.setMinimumSize(QSize(90, 0))
        self.pushButton_sym_forward_slash.setFont(font)
        self.pushButton_sym_forward_slash.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_forward_slash.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_16.addWidget(self.pushButton_sym_forward_slash, 0, 1, 1, 1)

        self.pushButton_sym_ampersand = QPushButton(self.widget_sym_2)
        self.pushButton_sym_ampersand.setObjectName(u"pushButton_sym_ampersand")
        sizePolicy.setHeightForWidth(self.pushButton_sym_ampersand.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_ampersand.setSizePolicy(sizePolicy)
        self.pushButton_sym_ampersand.setMinimumSize(QSize(90, 0))
        self.pushButton_sym_ampersand.setFont(font)
        self.pushButton_sym_ampersand.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_ampersand.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_16.addWidget(self.pushButton_sym_ampersand, 0, 0, 1, 1)

        self.pushButton_sym_left_square_bracket = QPushButton(self.widget_sym_2)
        self.pushButton_sym_left_square_bracket.setObjectName(u"pushButton_sym_left_square_bracket")
        sizePolicy.setHeightForWidth(self.pushButton_sym_left_square_bracket.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_left_square_bracket.setSizePolicy(sizePolicy)
        self.pushButton_sym_left_square_bracket.setMinimumSize(QSize(90, 0))
        self.pushButton_sym_left_square_bracket.setFont(font)
        self.pushButton_sym_left_square_bracket.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_left_square_bracket.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_16.addWidget(self.pushButton_sym_left_square_bracket, 0, 6, 1, 1)

        self.pushButton_sym_right_curly_brace = QPushButton(self.widget_sym_2)
        self.pushButton_sym_right_curly_brace.setObjectName(u"pushButton_sym_right_curly_brace")
        sizePolicy.setHeightForWidth(self.pushButton_sym_right_curly_brace.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_right_curly_brace.setSizePolicy(sizePolicy)
        self.pushButton_sym_right_curly_brace.setMinimumSize(QSize(90, 0))
        self.pushButton_sym_right_curly_brace.setFont(font)
        self.pushButton_sym_right_curly_brace.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_right_curly_brace.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_16.addWidget(self.pushButton_sym_right_curly_brace, 0, 3, 1, 1)

        self.pushButton_sym_right_square_bracket = QPushButton(self.widget_sym_2)
        self.pushButton_sym_right_square_bracket.setObjectName(u"pushButton_sym_right_square_bracket")
        sizePolicy.setHeightForWidth(self.pushButton_sym_right_square_bracket.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_right_square_bracket.setSizePolicy(sizePolicy)
        self.pushButton_sym_right_square_bracket.setMinimumSize(QSize(90, 0))
        self.pushButton_sym_right_square_bracket.setFont(font)
        self.pushButton_sym_right_square_bracket.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_right_square_bracket.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_16.addWidget(self.pushButton_sym_right_square_bracket, 0, 7, 1, 1)

        self.pushButton_sym_star = QPushButton(self.widget_sym_2)
        self.pushButton_sym_star.setObjectName(u"pushButton_sym_star")
        sizePolicy.setHeightForWidth(self.pushButton_sym_star.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_star.setSizePolicy(sizePolicy)
        self.pushButton_sym_star.setMinimumSize(QSize(90, 0))
        self.pushButton_sym_star.setFont(font)
        self.pushButton_sym_star.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_star.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_16.addWidget(self.pushButton_sym_star, 0, 10, 1, 1)


        self.gridLayout_19.addWidget(self.widget_sym_2, 1, 1, 1, 1)

        self.widget_sym_3 = QWidget(self.page_symbol)
        self.widget_sym_3.setObjectName(u"widget_sym_3")
        self.widget_sym_3.setFont(font)
        self.widget_sym_3.setFocusPolicy(Qt.NoFocus)
        self.widget_sym_3.setStyleSheet(u"QWidget#widget_3{background-color: transparent;}")
        self.gridLayout_18 = QGridLayout(self.widget_sym_3)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_18.setHorizontalSpacing(8)
        self.gridLayout_18.setVerticalSpacing(0)
        self.gridLayout_18.setContentsMargins(5, 5, 5, 5)
        self.pushButton_sym_pilcrow = QPushButton(self.widget_sym_3)
        self.pushButton_sym_pilcrow.setObjectName(u"pushButton_sym_pilcrow")
        sizePolicy.setHeightForWidth(self.pushButton_sym_pilcrow.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_pilcrow.setSizePolicy(sizePolicy)
        self.pushButton_sym_pilcrow.setMinimumSize(QSize(100, 0))
        self.pushButton_sym_pilcrow.setFont(font)
        self.pushButton_sym_pilcrow.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_pilcrow.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_18.addWidget(self.pushButton_sym_pilcrow, 0, 9, 1, 1)

        self.pushButton_sym_tl = QPushButton(self.widget_sym_3)
        self.pushButton_sym_tl.setObjectName(u"pushButton_sym_tl")
        sizePolicy.setHeightForWidth(self.pushButton_sym_tl.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_tl.setSizePolicy(sizePolicy)
        self.pushButton_sym_tl.setMinimumSize(QSize(100, 0))
        self.pushButton_sym_tl.setFont(font)
        self.pushButton_sym_tl.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_tl.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_18.addWidget(self.pushButton_sym_tl, 0, 10, 1, 1)

        self.pushButton_sym_semi_colon = QPushButton(self.widget_sym_3)
        self.pushButton_sym_semi_colon.setObjectName(u"pushButton_sym_semi_colon")
        sizePolicy.setHeightForWidth(self.pushButton_sym_semi_colon.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_semi_colon.setSizePolicy(sizePolicy)
        self.pushButton_sym_semi_colon.setMinimumSize(QSize(100, 0))
        self.pushButton_sym_semi_colon.setFont(font)
        self.pushButton_sym_semi_colon.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_semi_colon.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_18.addWidget(self.pushButton_sym_semi_colon, 0, 5, 1, 1)

        self.pushButton_sym_tilde = QPushButton(self.widget_sym_3)
        self.pushButton_sym_tilde.setObjectName(u"pushButton_sym_tilde")
        sizePolicy.setHeightForWidth(self.pushButton_sym_tilde.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_tilde.setSizePolicy(sizePolicy)
        self.pushButton_sym_tilde.setMinimumSize(QSize(100, 0))
        self.pushButton_sym_tilde.setFont(font)
        self.pushButton_sym_tilde.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_tilde.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_18.addWidget(self.pushButton_sym_tilde, 0, 3, 1, 1)

        self.pushButton_sym_hyphen = QPushButton(self.widget_sym_3)
        self.pushButton_sym_hyphen.setObjectName(u"pushButton_sym_hyphen")
        sizePolicy.setHeightForWidth(self.pushButton_sym_hyphen.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_hyphen.setSizePolicy(sizePolicy)
        self.pushButton_sym_hyphen.setMinimumSize(QSize(100, 0))
        self.pushButton_sym_hyphen.setFont(font)
        self.pushButton_sym_hyphen.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_hyphen.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_18.addWidget(self.pushButton_sym_hyphen, 0, 1, 1, 1)

        self.pushButton_sym_colon = QPushButton(self.widget_sym_3)
        self.pushButton_sym_colon.setObjectName(u"pushButton_sym_colon")
        sizePolicy.setHeightForWidth(self.pushButton_sym_colon.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_colon.setSizePolicy(sizePolicy)
        self.pushButton_sym_colon.setMinimumSize(QSize(100, 0))
        self.pushButton_sym_colon.setFont(font)
        self.pushButton_sym_colon.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_colon.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_18.addWidget(self.pushButton_sym_colon, 0, 7, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(50, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_5, 0, 0, 1, 1)

        self.pushButton_sym_backtick = QPushButton(self.widget_sym_3)
        self.pushButton_sym_backtick.setObjectName(u"pushButton_sym_backtick")
        sizePolicy.setHeightForWidth(self.pushButton_sym_backtick.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_backtick.setSizePolicy(sizePolicy)
        self.pushButton_sym_backtick.setMinimumSize(QSize(100, 0))
        self.pushButton_sym_backtick.setFont(font)
        self.pushButton_sym_backtick.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_backtick.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_18.addWidget(self.pushButton_sym_backtick, 0, 6, 1, 1)

        self.pushButton_sym_or = QPushButton(self.widget_sym_3)
        self.pushButton_sym_or.setObjectName(u"pushButton_sym_or")
        sizePolicy.setHeightForWidth(self.pushButton_sym_or.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_or.setSizePolicy(sizePolicy)
        self.pushButton_sym_or.setMinimumSize(QSize(100, 0))
        self.pushButton_sym_or.setFont(font)
        self.pushButton_sym_or.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_or.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_18.addWidget(self.pushButton_sym_or, 0, 4, 1, 1)

        self.pushButton_sym_underscore = QPushButton(self.widget_sym_3)
        self.pushButton_sym_underscore.setObjectName(u"pushButton_sym_underscore")
        sizePolicy.setHeightForWidth(self.pushButton_sym_underscore.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_underscore.setSizePolicy(sizePolicy)
        self.pushButton_sym_underscore.setMinimumSize(QSize(100, 0))
        self.pushButton_sym_underscore.setFont(font)
        self.pushButton_sym_underscore.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_underscore.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_18.addWidget(self.pushButton_sym_underscore, 0, 2, 1, 1)

        self.pushButton_sym_left_arrow = QPushButton(self.widget_sym_3)
        self.pushButton_sym_left_arrow.setObjectName(u"pushButton_sym_left_arrow")
        sizePolicy.setHeightForWidth(self.pushButton_sym_left_arrow.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_left_arrow.setSizePolicy(sizePolicy)
        self.pushButton_sym_left_arrow.setMinimumSize(QSize(100, 0))
        self.pushButton_sym_left_arrow.setFont(font)
        self.pushButton_sym_left_arrow.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_left_arrow.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_18.addWidget(self.pushButton_sym_left_arrow, 0, 11, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(50, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_7, 0, 12, 1, 1)


        self.gridLayout_19.addWidget(self.widget_sym_3, 2, 1, 1, 1)

        self.widget_sym_4 = QWidget(self.page_symbol)
        self.widget_sym_4.setObjectName(u"widget_sym_4")
        self.widget_sym_4.setFont(font)
        self.widget_sym_4.setFocusPolicy(Qt.NoFocus)
        self.widget_sym_4.setStyleSheet(u"QWidget#widget_4{background-color: transparent;}")
        self.gridLayout_13 = QGridLayout(self.widget_sym_4)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setHorizontalSpacing(8)
        self.gridLayout_13.setVerticalSpacing(0)
        self.gridLayout_13.setContentsMargins(5, 5, 5, 5)
        self.pushButton_sym_multiplication = QPushButton(self.widget_sym_4)
        self.pushButton_sym_multiplication.setObjectName(u"pushButton_sym_multiplication")
        sizePolicy.setHeightForWidth(self.pushButton_sym_multiplication.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_multiplication.setSizePolicy(sizePolicy)
        self.pushButton_sym_multiplication.setMinimumSize(QSize(100, 0))
        self.pushButton_sym_multiplication.setFont(font)
        self.pushButton_sym_multiplication.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_multiplication.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_13.addWidget(self.pushButton_sym_multiplication, 0, 7, 1, 1)

        self.pushButton_sym_eng = QPushButton(self.widget_sym_4)
        self.pushButton_sym_eng.setObjectName(u"pushButton_sym_eng")
        sizePolicy.setHeightForWidth(self.pushButton_sym_eng.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_eng.setSizePolicy(sizePolicy)
        self.pushButton_sym_eng.setMinimumSize(QSize(100, 0))
        self.pushButton_sym_eng.setFont(font)
        self.pushButton_sym_eng.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_eng.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_13.addWidget(self.pushButton_sym_eng, 0, 8, 1, 1)

        self.pushButton_sym_backspace = QPushButton(self.widget_sym_4)
        self.pushButton_sym_backspace.setObjectName(u"pushButton_sym_backspace")
        sizePolicy.setHeightForWidth(self.pushButton_sym_backspace.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_backspace.setSizePolicy(sizePolicy)
        self.pushButton_sym_backspace.setMinimumSize(QSize(100, 0))
        self.pushButton_sym_backspace.setFont(font)
        self.pushButton_sym_backspace.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_backspace.setStyleSheet(u"QPushButton{\n"
"background-color: transparent;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: rgba(50, 50, 50, 209);\n"
"}")
        self.pushButton_sym_backspace.setIcon(icon)
        self.pushButton_sym_backspace.setIconSize(QSize(57, 57))
        self.pushButton_sym_backspace.setFlat(True)

        self.gridLayout_13.addWidget(self.pushButton_sym_backspace, 0, 10, 1, 1)

        self.pushButton_sym_micro = QPushButton(self.widget_sym_4)
        self.pushButton_sym_micro.setObjectName(u"pushButton_sym_micro")
        sizePolicy.setHeightForWidth(self.pushButton_sym_micro.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_micro.setSizePolicy(sizePolicy)
        self.pushButton_sym_micro.setMinimumSize(QSize(100, 0))
        self.pushButton_sym_micro.setFont(font)
        self.pushButton_sym_micro.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_micro.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_13.addWidget(self.pushButton_sym_micro, 0, 6, 1, 1)

        self.pushButton_sym_cent = QPushButton(self.widget_sym_4)
        self.pushButton_sym_cent.setObjectName(u"pushButton_sym_cent")
        sizePolicy.setHeightForWidth(self.pushButton_sym_cent.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_cent.setSizePolicy(sizePolicy)
        self.pushButton_sym_cent.setMinimumSize(QSize(100, 0))
        self.pushButton_sym_cent.setFont(font)
        self.pushButton_sym_cent.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_cent.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_13.addWidget(self.pushButton_sym_cent, 0, 5, 1, 1)

        self.pushButton_sym_left_guillemet = QPushButton(self.widget_sym_4)
        self.pushButton_sym_left_guillemet.setObjectName(u"pushButton_sym_left_guillemet")
        sizePolicy.setHeightForWidth(self.pushButton_sym_left_guillemet.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_left_guillemet.setSizePolicy(sizePolicy)
        self.pushButton_sym_left_guillemet.setMinimumSize(QSize(100, 0))
        self.pushButton_sym_left_guillemet.setFont(font)
        self.pushButton_sym_left_guillemet.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_left_guillemet.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_13.addWidget(self.pushButton_sym_left_guillemet, 0, 3, 1, 1)

        self.pushButton_sym_feminine_ordinal_indicator = QPushButton(self.widget_sym_4)
        self.pushButton_sym_feminine_ordinal_indicator.setObjectName(u"pushButton_sym_feminine_ordinal_indicator")
        sizePolicy.setHeightForWidth(self.pushButton_sym_feminine_ordinal_indicator.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_feminine_ordinal_indicator.setSizePolicy(sizePolicy)
        self.pushButton_sym_feminine_ordinal_indicator.setMinimumSize(QSize(100, 0))
        self.pushButton_sym_feminine_ordinal_indicator.setFont(font)
        self.pushButton_sym_feminine_ordinal_indicator.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_feminine_ordinal_indicator.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_13.addWidget(self.pushButton_sym_feminine_ordinal_indicator, 0, 2, 1, 1)

        self.pushButton_sym_right_guillemet = QPushButton(self.widget_sym_4)
        self.pushButton_sym_right_guillemet.setObjectName(u"pushButton_sym_right_guillemet")
        sizePolicy.setHeightForWidth(self.pushButton_sym_right_guillemet.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_right_guillemet.setSizePolicy(sizePolicy)
        self.pushButton_sym_right_guillemet.setMinimumSize(QSize(100, 0))
        self.pushButton_sym_right_guillemet.setFont(font)
        self.pushButton_sym_right_guillemet.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_right_guillemet.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_13.addWidget(self.pushButton_sym_right_guillemet, 0, 4, 1, 1)

        self.pushButton_sym_eszett = QPushButton(self.widget_sym_4)
        self.pushButton_sym_eszett.setObjectName(u"pushButton_sym_eszett")
        sizePolicy.setHeightForWidth(self.pushButton_sym_eszett.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_eszett.setSizePolicy(sizePolicy)
        self.pushButton_sym_eszett.setMinimumSize(QSize(100, 0))
        self.pushButton_sym_eszett.setFont(font)
        self.pushButton_sym_eszett.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_eszett.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_13.addWidget(self.pushButton_sym_eszett, 0, 1, 1, 1)

        self.pushButton_sym_to_abc = QPushButton(self.widget_sym_4)
        self.pushButton_sym_to_abc.setObjectName(u"pushButton_sym_to_abc")
        sizePolicy.setHeightForWidth(self.pushButton_sym_to_abc.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_to_abc.setSizePolicy(sizePolicy)
        self.pushButton_sym_to_abc.setMinimumSize(QSize(130, 0))
        self.pushButton_sym_to_abc.setFont(font)
        self.pushButton_sym_to_abc.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_to_abc.setStyleSheet(u"QPushButton{\n"
"background-color: transparent;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: rgba(50, 50, 50, 209);\n"
"}")
        self.pushButton_sym_to_abc.setFlat(True)

        self.gridLayout_13.addWidget(self.pushButton_sym_to_abc, 0, 0, 1, 1)

        self.pushButton_sym_pound = QPushButton(self.widget_sym_4)
        self.pushButton_sym_pound.setObjectName(u"pushButton_sym_pound")
        sizePolicy.setHeightForWidth(self.pushButton_sym_pound.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_pound.setSizePolicy(sizePolicy)
        self.pushButton_sym_pound.setMinimumSize(QSize(100, 0))
        self.pushButton_sym_pound.setFont(font)
        self.pushButton_sym_pound.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_pound.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"\n"
"border-radius: 15px;\n"
"} QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")

        self.gridLayout_13.addWidget(self.pushButton_sym_pound, 0, 9, 1, 1)


        self.gridLayout_19.addWidget(self.widget_sym_4, 3, 1, 1, 1)

        self.widget_sym_5 = QWidget(self.page_symbol)
        self.widget_sym_5.setObjectName(u"widget_sym_5")
        self.widget_sym_5.setFont(font)
        self.widget_sym_5.setFocusPolicy(Qt.NoFocus)
        self.widget_sym_5.setStyleSheet(u"QWidget#widget_5{background-color: transparent;}")
        self.gridLayout_17 = QGridLayout(self.widget_sym_5)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setHorizontalSpacing(5)
        self.gridLayout_17.setVerticalSpacing(0)
        self.gridLayout_17.setContentsMargins(5, 5, 5, 5)
        self.pushButton_sym_enter = QPushButton(self.widget_sym_5)
        self.pushButton_sym_enter.setObjectName(u"pushButton_sym_enter")
        sizePolicy.setHeightForWidth(self.pushButton_sym_enter.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_enter.setSizePolicy(sizePolicy)
        self.pushButton_sym_enter.setMinimumSize(QSize(130, 0))
        self.pushButton_sym_enter.setFont(font)
        self.pushButton_sym_enter.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_enter.setStyleSheet(u"QPushButton{\n"
"background-color: transparent;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: rgba(50, 50, 50, 209);\n"
"}")
        self.pushButton_sym_enter.setIcon(icon1)
        self.pushButton_sym_enter.setIconSize(QSize(85, 85))
        self.pushButton_sym_enter.setFlat(True)

        self.gridLayout_17.addWidget(self.pushButton_sym_enter, 0, 4, 1, 1)

        self.pushButton_sym_dot = QPushButton(self.widget_sym_5)
        self.pushButton_sym_dot.setObjectName(u"pushButton_sym_dot")
        sizePolicy.setHeightForWidth(self.pushButton_sym_dot.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_dot.setSizePolicy(sizePolicy)
        self.pushButton_sym_dot.setMinimumSize(QSize(130, 0))
        self.pushButton_sym_dot.setFont(font1)
        self.pushButton_sym_dot.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_dot.setStyleSheet(u"QPushButton{\n"
"background-color: transparent;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: rgba(50, 50, 50, 209);\n"
"}")
        self.pushButton_sym_dot.setFlat(True)

        self.gridLayout_17.addWidget(self.pushButton_sym_dot, 0, 3, 1, 1)

        self.pushButton_sym_to_123 = QPushButton(self.widget_sym_5)
        self.pushButton_sym_to_123.setObjectName(u"pushButton_sym_to_123")
        sizePolicy.setHeightForWidth(self.pushButton_sym_to_123.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_to_123.setSizePolicy(sizePolicy)
        self.pushButton_sym_to_123.setMinimumSize(QSize(130, 0))
        self.pushButton_sym_to_123.setFont(font)
        self.pushButton_sym_to_123.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_to_123.setStyleSheet(u"QPushButton{\n"
"background-color: transparent;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: rgba(50, 50, 50, 209);\n"
"}")
        self.pushButton_sym_to_123.setFlat(True)

        self.gridLayout_17.addWidget(self.pushButton_sym_to_123, 0, 0, 1, 1)

        self.pushButton_sym_comma = QPushButton(self.widget_sym_5)
        self.pushButton_sym_comma.setObjectName(u"pushButton_sym_comma")
        sizePolicy.setHeightForWidth(self.pushButton_sym_comma.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_comma.setSizePolicy(sizePolicy)
        self.pushButton_sym_comma.setMinimumSize(QSize(130, 0))
        self.pushButton_sym_comma.setFont(font1)
        self.pushButton_sym_comma.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_comma.setStyleSheet(u"QPushButton{\n"
"background-color: transparent;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: rgba(50, 50, 50, 209);\n"
"}")
        self.pushButton_sym_comma.setFlat(True)

        self.gridLayout_17.addWidget(self.pushButton_sym_comma, 0, 1, 1, 1)

        self.pushButton_sym_space = QPushButton(self.widget_sym_5)
        self.pushButton_sym_space.setObjectName(u"pushButton_sym_space")
        sizePolicy1.setHeightForWidth(self.pushButton_sym_space.sizePolicy().hasHeightForWidth())
        self.pushButton_sym_space.setSizePolicy(sizePolicy1)
        self.pushButton_sym_space.setMinimumSize(QSize(130, 0))
        self.pushButton_sym_space.setFont(font)
        self.pushButton_sym_space.setFocusPolicy(Qt.NoFocus)
        self.pushButton_sym_space.setStyleSheet(u"QPushButton{\n"
"background-color: rgba(71, 68, 68, 209);\n"
"padding-top: 60px;\n"
"border-radius: 15px;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: rgba(50, 50, 50, 209);\n"
"}")
        self.pushButton_sym_space.setIconSize(QSize(100, 68))

        self.gridLayout_17.addWidget(self.pushButton_sym_space, 0, 2, 1, 1)


        self.gridLayout_19.addWidget(self.widget_sym_5, 4, 1, 1, 1)

        self.horizontalSpacer_12 = QSpacerItem(306, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_12, 1, 0, 1, 1)

        self.horizontalSpacer_13 = QSpacerItem(306, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_13, 1, 2, 1, 1)

        self.stackedWidget_keyboard_layout.addWidget(self.page_symbol)

        self.gridLayout_7.addWidget(self.stackedWidget_keyboard_layout, 0, 0, 1, 2)


        self.gridLayout_6.addWidget(self.frame_background, 0, 0, 1, 1)


        self.retranslateUi(KeyboardUI)

        self.stackedWidget_keyboard_layout.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(KeyboardUI)
    # setupUi

    def retranslateUi(self, KeyboardUI):
        KeyboardUI.setWindowTitle(QCoreApplication.translate("KeyboardUI", u"Form", None))
        self.pushButton_abc_1.setText(QCoreApplication.translate("KeyboardUI", u"1", None))
        self.pushButton_abc_2.setText(QCoreApplication.translate("KeyboardUI", u"2", None))
        self.pushButton_abc_3.setText(QCoreApplication.translate("KeyboardUI", u"3", None))
        self.pushButton_abc_4.setText(QCoreApplication.translate("KeyboardUI", u"4", None))
        self.pushButton_abc_5.setText(QCoreApplication.translate("KeyboardUI", u"5", None))
        self.pushButton_abc_6.setText(QCoreApplication.translate("KeyboardUI", u"6", None))
        self.pushButton_abc_7.setText(QCoreApplication.translate("KeyboardUI", u"7", None))
        self.pushButton_abc_8.setText(QCoreApplication.translate("KeyboardUI", u"8", None))
        self.pushButton_abc_9.setText(QCoreApplication.translate("KeyboardUI", u"9", None))
        self.pushButton_abc_0.setText(QCoreApplication.translate("KeyboardUI", u"0", None))
        self.pushButton_abc_tr_u.setText(QCoreApplication.translate("KeyboardUI", u"\u00dc", None))
        self.pushButton_abc_p.setText(QCoreApplication.translate("KeyboardUI", u"P", None))
        self.pushButton_abc_y.setText(QCoreApplication.translate("KeyboardUI", u"Y", None))
        self.pushButton_abc_e.setText(QCoreApplication.translate("KeyboardUI", u"E", None))
        self.pushButton_abc_t.setText(QCoreApplication.translate("KeyboardUI", u"T", None))
        self.pushButton_abc_o.setText(QCoreApplication.translate("KeyboardUI", u"O", None))
        self.pushButton_abc_w.setText(QCoreApplication.translate("KeyboardUI", u"W", None))
        self.pushButton_abc_q.setText(QCoreApplication.translate("KeyboardUI", u"Q", None))
        self.pushButton_abc_u.setText(QCoreApplication.translate("KeyboardUI", u"U", None))
        self.pushButton_abc_r.setText(QCoreApplication.translate("KeyboardUI", u"R", None))
        self.pushButton_abc_tr_i.setText(QCoreApplication.translate("KeyboardUI", u"I", None))
        self.pushButton_abc_tr_g.setText(QCoreApplication.translate("KeyboardUI", u"\u011e", None))
        self.pushButton_abc_f.setText(QCoreApplication.translate("KeyboardUI", u"F", None))
        self.pushButton_abc_d.setText(QCoreApplication.translate("KeyboardUI", u"D", None))
        self.pushButton_abc_g.setText(QCoreApplication.translate("KeyboardUI", u"G", None))
        self.pushButton_abc_k.setText(QCoreApplication.translate("KeyboardUI", u"K", None))
        self.pushButton_abc_i.setText(QCoreApplication.translate("KeyboardUI", u"\u0130", None))
        self.pushButton_abc_l.setText(QCoreApplication.translate("KeyboardUI", u"L", None))
        self.pushButton_abc_h.setText(QCoreApplication.translate("KeyboardUI", u"H", None))
        self.pushButton_abc_a.setText(QCoreApplication.translate("KeyboardUI", u"A", None))
        self.pushButton_abc_tr_s.setText(QCoreApplication.translate("KeyboardUI", u"\u015e", None))
        self.pushButton_abc_s.setText(QCoreApplication.translate("KeyboardUI", u"S", None))
        self.pushButton_abc_j.setText(QCoreApplication.translate("KeyboardUI", u"J", None))
        self.pushButton_abc_m.setText(QCoreApplication.translate("KeyboardUI", u"M", None))
        self.pushButton_abc_b.setText(QCoreApplication.translate("KeyboardUI", u"B", None))
        self.pushButton_abc_x.setText(QCoreApplication.translate("KeyboardUI", u"X", None))
        self.pushButton_abc_v.setText(QCoreApplication.translate("KeyboardUI", u"V", None))
        self.pushButton_abc_n.setText(QCoreApplication.translate("KeyboardUI", u"N", None))
        self.pushButton_abc_tr_o.setText(QCoreApplication.translate("KeyboardUI", u"\u00d6", None))
        self.pushButton_abc_c.setText(QCoreApplication.translate("KeyboardUI", u"C", None))
        self.pushButton_abc_z.setText(QCoreApplication.translate("KeyboardUI", u"Z", None))
        self.pushButton_abc_tr_c.setText(QCoreApplication.translate("KeyboardUI", u"\u00c7", None))
        self.pushButton_abc_backspace.setText("")
        self.pushButton_shift.setText("")
        self.pushButton_abc_dot.setText(QCoreApplication.translate("KeyboardUI", u".", None))
        self.pushButton_abc_to_123.setText(QCoreApplication.translate("KeyboardUI", u"123", None))
        self.pushButton_abc_comma.setText(QCoreApplication.translate("KeyboardUI", u",", None))
        self.pushButton_abc_space.setText("")
        self.pushButton_123_dot.setText(QCoreApplication.translate("KeyboardUI", u".", None))
        self.pushButton_123_to_abc.setText(QCoreApplication.translate("KeyboardUI", u"abc", None))
        self.pushButton_123_comma.setText(QCoreApplication.translate("KeyboardUI", u",", None))
        self.pushButton_123_space.setText("")
        self.pushButton_123_forward_slash.setText(QCoreApplication.translate("KeyboardUI", u"/", None))
        self.pushButton_123_single_quote.setText(QCoreApplication.translate("KeyboardUI", u"'", None))
        self.pushButton_123_colon.setText(QCoreApplication.translate("KeyboardUI", u":", None))
        self.pushButton_123_plus.setText(QCoreApplication.translate("KeyboardUI", u"+", None))
        self.pushButton_123_backspace.setText("")
        self.pushButton_123_question.setText(QCoreApplication.translate("KeyboardUI", u"?", None))
        self.pushButton_123_double_quote.setText(QCoreApplication.translate("KeyboardUI", u"\"", None))
        self.pushButton_123_exclamation.setText(QCoreApplication.translate("KeyboardUI", u"!", None))
        self.pushButton_123_star.setText(QCoreApplication.translate("KeyboardUI", u"*", None))
        self.pushButton_123_to_symbols.setText(QCoreApplication.translate("KeyboardUI", u"{&&=", None))
        self.pushButton_123_at.setText(QCoreApplication.translate("KeyboardUI", u"@", None))
        self.pushButton_123_underscore.setText(QCoreApplication.translate("KeyboardUI", u"_", None))
        self.pushButton_123_hash.setText(QCoreApplication.translate("KeyboardUI", u"#", None))
        self.pushButton_123_hyphen.setText(QCoreApplication.translate("KeyboardUI", u"-", None))
        self.pushButton_123_right_parenthesis.setText(QCoreApplication.translate("KeyboardUI", u")", None))
        self.pushButton_123_left_parenthesis.setText(QCoreApplication.translate("KeyboardUI", u"(", None))
        self.pushButton_123_percent.setText(QCoreApplication.translate("KeyboardUI", u"%", None))
        self.pushButton_123_ampersand.setText(QCoreApplication.translate("KeyboardUI", u"&&", None))
        self.pushButton_123_equal.setText(QCoreApplication.translate("KeyboardUI", u"=", None))
        self.pushButton_123_tl.setText(QCoreApplication.translate("KeyboardUI", u"\u20ba", None))
        self.pushButton_123_1.setText(QCoreApplication.translate("KeyboardUI", u"1", None))
        self.pushButton_123_2.setText(QCoreApplication.translate("KeyboardUI", u"2", None))
        self.pushButton_123_3.setText(QCoreApplication.translate("KeyboardUI", u"3", None))
        self.pushButton_123_4.setText(QCoreApplication.translate("KeyboardUI", u"4", None))
        self.pushButton_123_5.setText(QCoreApplication.translate("KeyboardUI", u"5", None))
        self.pushButton_123_6.setText(QCoreApplication.translate("KeyboardUI", u"6", None))
        self.pushButton_123_7.setText(QCoreApplication.translate("KeyboardUI", u"7", None))
        self.pushButton_123_8.setText(QCoreApplication.translate("KeyboardUI", u"8", None))
        self.pushButton_123_9.setText(QCoreApplication.translate("KeyboardUI", u"9", None))
        self.pushButton_123_0.setText(QCoreApplication.translate("KeyboardUI", u"0", None))
        self.pushButton_sym_three_quarter.setText(QCoreApplication.translate("KeyboardUI", u"\u00be", None))
        self.pushButton_sym_plus.setText(QCoreApplication.translate("KeyboardUI", u"+", None))
        self.pushButton_sym_dollar.setText(QCoreApplication.translate("KeyboardUI", u"$", None))
        self.pushButton_sym_euro.setText(QCoreApplication.translate("KeyboardUI", u"\u20ac", None))
        self.pushButton_sym_double_quote.setText(QCoreApplication.translate("KeyboardUI", u"\"", None))
        self.pushButton_sym_one_half.setText(QCoreApplication.translate("KeyboardUI", u"\u00bd", None))
        self.pushButton_sym_hash.setText(QCoreApplication.translate("KeyboardUI", u"#", None))
        self.pushButton_sym_percent.setText(QCoreApplication.translate("KeyboardUI", u"%", None))
        self.pushButton_sym_exclamation.setText(QCoreApplication.translate("KeyboardUI", u"!", None))
        self.pushButton_sym_caret.setText(QCoreApplication.translate("KeyboardUI", u"^", None))
        self.pushButton_sym_single_quote.setText(QCoreApplication.translate("KeyboardUI", u"'", None))
        self.pushButton_sym_backslash.setText(QCoreApplication.translate("KeyboardUI", u"\\", None))
        self.pushButton_sym_question.setText(QCoreApplication.translate("KeyboardUI", u"?", None))
        self.pushButton_sym_right_parenthesis.setText(QCoreApplication.translate("KeyboardUI", u")", None))
        self.pushButton_sym_left_curly_brace.setText(QCoreApplication.translate("KeyboardUI", u"{", None))
        self.pushButton_sym_left_parenthesis.setText(QCoreApplication.translate("KeyboardUI", u"(", None))
        self.pushButton_sym_equal.setText(QCoreApplication.translate("KeyboardUI", u"=", None))
        self.pushButton_sym_forward_slash.setText(QCoreApplication.translate("KeyboardUI", u"/", None))
        self.pushButton_sym_ampersand.setText(QCoreApplication.translate("KeyboardUI", u"&&", None))
        self.pushButton_sym_left_square_bracket.setText(QCoreApplication.translate("KeyboardUI", u"[", None))
        self.pushButton_sym_right_curly_brace.setText(QCoreApplication.translate("KeyboardUI", u"}", None))
        self.pushButton_sym_right_square_bracket.setText(QCoreApplication.translate("KeyboardUI", u"]", None))
        self.pushButton_sym_star.setText(QCoreApplication.translate("KeyboardUI", u"*", None))
        self.pushButton_sym_pilcrow.setText(QCoreApplication.translate("KeyboardUI", u"\u00b6", None))
        self.pushButton_sym_tl.setText(QCoreApplication.translate("KeyboardUI", u"\u20ba", None))
        self.pushButton_sym_semi_colon.setText(QCoreApplication.translate("KeyboardUI", u"\u03a3", None))
        self.pushButton_sym_tilde.setText(QCoreApplication.translate("KeyboardUI", u"~", None))
        self.pushButton_sym_hyphen.setText(QCoreApplication.translate("KeyboardUI", u"-", None))
        self.pushButton_sym_colon.setText(QCoreApplication.translate("KeyboardUI", u":", None))
        self.pushButton_sym_backtick.setText(QCoreApplication.translate("KeyboardUI", u"`", None))
        self.pushButton_sym_or.setText(QCoreApplication.translate("KeyboardUI", u"|", None))
        self.pushButton_sym_underscore.setText(QCoreApplication.translate("KeyboardUI", u"_", None))
        self.pushButton_sym_left_arrow.setText(QCoreApplication.translate("KeyboardUI", u"\u2190", None))
        self.pushButton_sym_multiplication.setText(QCoreApplication.translate("KeyboardUI", u"\u00d7", None))
        self.pushButton_sym_eng.setText(QCoreApplication.translate("KeyboardUI", u"n", None))
        self.pushButton_sym_backspace.setText("")
        self.pushButton_sym_micro.setText(QCoreApplication.translate("KeyboardUI", u"\u00b5", None))
        self.pushButton_sym_cent.setText(QCoreApplication.translate("KeyboardUI", u"\u00a2", None))
        self.pushButton_sym_left_guillemet.setText(QCoreApplication.translate("KeyboardUI", u"\u00ab", None))
        self.pushButton_sym_feminine_ordinal_indicator.setText(QCoreApplication.translate("KeyboardUI", u"\u00aa", None))
        self.pushButton_sym_right_guillemet.setText(QCoreApplication.translate("KeyboardUI", u"\u00bb", None))
        self.pushButton_sym_eszett.setText(QCoreApplication.translate("KeyboardUI", u"\u00df", None))
        self.pushButton_sym_to_abc.setText(QCoreApplication.translate("KeyboardUI", u"abc", None))
        self.pushButton_sym_pound.setText(QCoreApplication.translate("KeyboardUI", u"\u00a3", None))
        self.pushButton_sym_dot.setText(QCoreApplication.translate("KeyboardUI", u".", None))
        self.pushButton_sym_to_123.setText(QCoreApplication.translate("KeyboardUI", u"123", None))
        self.pushButton_sym_comma.setText(QCoreApplication.translate("KeyboardUI", u",", None))
        self.pushButton_sym_space.setText("")
    # retranslateUi

