from PySide6 import QtWidgets, QtCore, QtGui
from CSS import header_css
from pathlib import Path

class Header(QtWidgets.QLabel):
    def __init__(self, main_window):
        super(Header, self).__init__(parent=main_window)

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

        self.lbl_logged_user_name = QtWidgets.QLabel(
            f'Bem-vindo, {main_window.logged_in_user.full_name}',parent=self
        )
        self.lbl_logged_user_name.setStyleSheet(header_css.lbl_logged_user_name)
        self.lbl_logged_user_name.setFixedWidth(len(self.lbl_logged_user_name.text()) * 12)
        self.lbl_logged_user_name.move(
            self.width() - self.lbl_logged_user_name.width() - 50,
            self.height() // 2 - self.lbl_logged_user_name.height() // 2
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

        self.btn_rent_car = QtWidgets.QPushButton("Alugar carro")
        self.btn_rent_car.setFixedSize(len(self.btn_rent_car.text()) * 9, 30)
        self.btn_rent_car.setStyleSheet(header_css.lbl_options)
        self.btn_rent_car.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.grid.addWidget(self.btn_rent_car, 0, 0)

        self.btn_rented_cars = QtWidgets.QPushButton("Carros alugados")
        self.btn_rented_cars.setFixedSize(len(self.btn_rented_cars.text()) * 9, 30)
        self.btn_rented_cars.setStyleSheet(header_css.lbl_options)
        self.btn_rented_cars.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.grid.addWidget(self.btn_rented_cars, 0, 1)

        self.btn_exit = QtWidgets.QPushButton("Sair", parent=self.header_options_section)
        self.btn_exit.setFixedSize(len(self.btn_exit.text()) * 9, 30)
        self.btn_exit.setStyleSheet(header_css.lbl_options)
        self.btn_exit.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_exit.clicked.connect(self.back_to_login_window)
        self.grid.addWidget(self.btn_exit, 0, 2)

        self.grid.setHorizontalSpacing(40)


    def back_to_login_window(self):
        main_window = self.parent()
        self.hide()
        main_window.rent_a_car_window.hide()
        main_window.login_and_registration_window.show()
