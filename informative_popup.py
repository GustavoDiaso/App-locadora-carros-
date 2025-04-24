from __future__ import annotations
from PySide6 import QtWidgets, QtCore
from CSS import css

class InformativePopUp(QtWidgets.QLabel):
    def __init__(
        self,
        parent,
        title: str = "No titles here",
        information: str = "No infomations here",
    ):
        super(InformativePopUp, self).__init__(parent=parent)
        self.setFixedSize(400, 200)
        self.move(
            parent.width() // 2 - self.width() // 2,
            parent.height() // 2 - self.height() // 2,
        )
        self.setStyleSheet(css.informative_popup)

        margin_right = 30
        margin_left = 30

        self.popup_header = QtWidgets.QLabel(title, parent=self)
        self.popup_header.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.popup_header.setFixedSize(self.width(), 40)
        self.popup_header.setStyleSheet(css.popup_header)
        self.popup_header.move(0, 0)

        self.btn_close_popup = QtWidgets.QPushButton("X", parent=self)
        self.btn_close_popup.setFixedSize(20, 20)
        self.btn_close_popup.move(
            self.width() - self.btn_close_popup.width() - 10,
            self.popup_header.height() // 2 - self.btn_close_popup.height() // 2 + 1,
        )
        self.btn_close_popup.clicked.connect(self.toggle_popup)
        self.btn_close_popup.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_close_popup.setStyleSheet(css.btn_close_popup)

        self.lbl_information = QtWidgets.QLabel(information, parent=self)
        self.lbl_information.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_information.setFixedWidth(380)
        self.lbl_information.move(
            self.width() // 2 - self.lbl_information.width() // 2,
            self.height() // 2 - self.lbl_information.height() // 2 + 15,
        )
        self.lbl_information.setStyleSheet(css.informative_popup_lbl)

        self.setVisible(False)

    def toggle_popup(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()