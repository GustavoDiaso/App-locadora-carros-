from PySide6 import QtWidgets, QtCore, QtGui
from datetime import datetime
from CSS import header_css
import re
from pathlib import Path

class Header(QtWidgets.QLabel):
    def __init__(self, parent):
        super(Header, self).__init__(parent)

        user_screen = QtGui.QGuiApplication.primaryScreen()
        user_screen_geometry = user_screen.availableGeometry()
        self.setFixedSize(
            user_screen_geometry.width(), int(user_screen_geometry.height() * (1/7))
        )
        self.move(0, 0)

        self.setStyleSheet(header_css.header)

        self.logo = QtWidgets.QLabel(parent=self)
        self.logo.setPixmap(QtGui.QPixmap(Path(__file__).parent / 'images/CompanyLogo.png').scaled(100, 100))
        self.logo.setFixedSize(100, 100)
        self.logo.move(50, self.height()//2 - self.logo.height()//2)

        self.lbl_company_name = QtWidgets.QLabel("RENTACAR.COM",parent=self)
        self.lbl_company_name.setStyleSheet(header_css.lbl_company_name)
        self.lbl_company_name.setFixedWidth(len(self.lbl_company_name.text()) * 12)
        self.lbl_company_name.move(
            self.width() - self.lbl_company_name.width() - 50,
            self.height() // 2 - self.lbl_company_name.height() // 2
        )

        self.header_options_section = QtWidgets.QLabel(parent=self)
        self.header_options_section.setStyleSheet(header_css.header_options_section)
        self.header_options_section.setFixedSize(
            430,
            60
        )
        self.header_options_section.move(
            self.width() // 2 - self.header_options_section.width() // 2 - 40,
            self.height() // 2 - self.header_options_section.height() // 2
        )

        self.grid = QtWidgets.QGridLayout(parent=self.header_options_section)

        self.lbl_rent_car = QtWidgets.QPushButton("Alugar carro")
        self.lbl_rent_car.setFixedSize(len(self.lbl_rent_car.text()) * 9, 30)
        self.lbl_rent_car.setStyleSheet(header_css.lbl_options)
        self.lbl_rent_car.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.grid.addWidget(self.lbl_rent_car, 0, 0)

        self.lbl_rented_cars = QtWidgets.QPushButton("Carros alugados")
        self.lbl_rented_cars.setFixedSize(len(self.lbl_rented_cars.text()) * 9, 30)
        self.lbl_rented_cars.setStyleSheet(header_css.lbl_options)
        self.lbl_rented_cars.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.grid.addWidget(self.lbl_rented_cars, 0, 1)

        self.lbl_exit = QtWidgets.QPushButton("Sair", parent=self.header_options_section)
        self.lbl_exit.setFixedSize(len(self.lbl_exit.text()) * 9, 30)
        self.lbl_exit.setStyleSheet(header_css.lbl_options)
        self.lbl_exit.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.grid.addWidget(self.lbl_exit, 0, 2)

        self.grid.setHorizontalSpacing(40)