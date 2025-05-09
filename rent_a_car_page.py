from PySide6 import QtWidgets, QtCore, QtGui
from CSS import rent_a_car_window_css as css
from pathlib import Path
from database import db_service
from itertools import groupby


class RentACarWindow(QtWidgets.QLabel):
    def __init__(self, main_window):
        super(RentACarWindow, self).__init__(parent=main_window)
        self.setStyleSheet(css.rent_a_car_window)

        user_screen = QtGui.QGuiApplication.primaryScreen()
        user_screen_geometry = user_screen.availableGeometry()
        header = main_window.header

        self.setFixedSize(
            user_screen_geometry.width(),
            user_screen_geometry.height() - header.height(),
        )

        self.car_options_side_menu = CarOptionsSideMenu(self)

        self.move(0, header.height())


class CarOptionsSideMenu(QtWidgets.QLabel):
    def __init__(self, rent_a_car_window):
        super(CarOptionsSideMenu, self).__init__(parent=rent_a_car_window)
        self.setStyleSheet(css.car_options_side_menu)

        windows_navbar_bottom_height = 25

        self.setFixedSize(
            rent_a_car_window.width() * 1 / 3,
            rent_a_car_window.height() - windows_navbar_bottom_height,
        )

        self.move(0, 0)

        self.lbl_available_cars = QtWidgets.QLabel("Veículos disponíveis", parent=self)
        self.lbl_available_cars.setStyleSheet(css.car_options_side_menu_title)
        self.lbl_available_cars.move(30, 30)

        self.scroll_area = QtWidgets.QScrollArea(parent=self)
        self.scroll_area.setFixedWidth(self.width() - 20)
        self.scroll_area.setMinimumHeight(self.height() - 100)
        self.scroll_area.move(10, 80)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.verticalScrollBar().setStyleSheet(css.scroll_bar)

        self.cars_grid_conteiner = QtWidgets.QWidget(parent=self.scroll_area)
        self.cars_grid_conteiner.setStyleSheet(css.cars_grid_conteiner)

        self.cars_grid = QtWidgets.QVBoxLayout()
        self.cars_grid.setSpacing(14)

        self.cars_grid_conteiner.setLayout(self.cars_grid)
        self.scroll_area.setWidget(self.cars_grid_conteiner)

        for vehicle in db_service.get_available_vehicles():
            print(vehicle)
            vehicle_info_box = QtWidgets.QLabel(
                f"{vehicle[4]} {vehicle[3]}, {vehicle[5]}, placa {vehicle[6]}"
            )
            vehicle_info_box.id = vehicle[0]
            vehicle_info_box.setStyleSheet(css.vehicle_info_box)
            vehicle_info_box.setFixedSize(self.cars_grid_conteiner.width() - 30, 80)
            vehicle_info_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            vehicle_info_box.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

            self.cars_grid.addWidget(vehicle_info_box)
