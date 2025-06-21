from PySide6 import QtWidgets, QtCore, QtGui


def set_correct_lbl_width(target_label: QtWidgets.QLabel):
    target_label.setFixedWidth(
        QtGui.QFontMetrics(target_label.font()).horizontalAdvance(target_label.text())
    )
