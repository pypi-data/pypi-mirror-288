# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'show_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QLayout, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)
from . import resources_rc

class Ui_ShowDialog(object):
    def setupUi(self, ShowDialog):
        if not ShowDialog.objectName():
            ShowDialog.setObjectName(u"ShowDialog")
        ShowDialog.resize(679, 589)
        font = QFont()
        font.setPointSize(50)
        ShowDialog.setFont(font)
        icon = QIcon()
        icon.addFile(u":/images/window_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        ShowDialog.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(ShowDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.v_layout = QVBoxLayout()
        self.v_layout.setObjectName(u"v_layout")
        self.v_layout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.title_label = QLabel(ShowDialog)
        self.title_label.setObjectName(u"title_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_label.sizePolicy().hasHeightForWidth())
        self.title_label.setSizePolicy(sizePolicy)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.v_layout.addWidget(self.title_label)

        self.description_label = QLabel(ShowDialog)
        self.description_label.setObjectName(u"description_label")
        font1 = QFont()
        font1.setPointSize(20)
        self.description_label.setFont(font1)

        self.v_layout.addWidget(self.description_label)

        self.buttons_h_layout = QHBoxLayout()
        self.buttons_h_layout.setObjectName(u"buttons_h_layout")
        self.fail_button = QPushButton(ShowDialog)
        self.fail_button.setObjectName(u"fail_button")
        self.fail_button.setMaximumSize(QSize(325, 100))
        icon1 = QIcon()
        icon1.addFile(u":/images/fail_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.fail_button.setIcon(icon1)

        self.buttons_h_layout.addWidget(self.fail_button)

        self.pass_button = QPushButton(ShowDialog)
        self.pass_button.setObjectName(u"pass_button")
        self.pass_button.setMaximumSize(QSize(325, 100))
        icon2 = QIcon()
        icon2.addFile(u":/images/pass_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pass_button.setIcon(icon2)

        self.buttons_h_layout.addWidget(self.pass_button)


        self.v_layout.addLayout(self.buttons_h_layout)


        self.verticalLayout.addLayout(self.v_layout)


        self.retranslateUi(ShowDialog)

        QMetaObject.connectSlotsByName(ShowDialog)
    # setupUi

    def retranslateUi(self, ShowDialog):
        ShowDialog.setWindowTitle(QCoreApplication.translate("ShowDialog", u"Show Dialog", None))
        self.title_label.setText(QCoreApplication.translate("ShowDialog", u"Title", None))
        self.description_label.setText(QCoreApplication.translate("ShowDialog", u"Description\n"
"multiline", None))
        self.fail_button.setText(QCoreApplication.translate("ShowDialog", u"Fail", None))
        self.pass_button.setText(QCoreApplication.translate("ShowDialog", u"Pass", None))
    # retranslateUi

