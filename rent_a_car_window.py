from PySide6 import QtWidgets, QtCore, QtGui
from CSS import rent_a_car_window_css as css
from pathlib import Path


class RentACarWindow(QtWidgets.QLabel):
    def __init__(self, main_window):
        super(RentACarWindow, self).__init__(parent=main_window)
        self.setStyleSheet(css.rent_a_car_window)

        user_screen = QtGui.QGuiApplication.primaryScreen()
        user_screen_geometry = user_screen.availableGeometry()
        header = main_window.header

        self.setFixedSize(
            user_screen_geometry.width(),
            user_screen_geometry.height() - header.height()
        )

        self.car_options_side_menu = CarOptionsSideMenu(self)

        self.move(0, header.height())



class CarOptionsSideMenu(QtWidgets.QLabel):
    def __init__(self, rent_a_car_window):
        super(CarOptionsSideMenu, self).__init__(parent=rent_a_car_window)
        self.setStyleSheet(css.car_options_side_menu)

        windows_navbar_bottom_height = 25

        self.setFixedSize(
            rent_a_car_window.width() * 1/3.5,
            rent_a_car_window.height() - windows_navbar_bottom_height
        )

        self.move(0,0)


        self.lbl_available_cars = QtWidgets.QLabel("Veículos disponíveis", parent=self)
        self.lbl_available_cars.setStyleSheet(css.car_options_side_menu_title)
        self.lbl_available_cars.move(30, 30)
