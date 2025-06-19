from PySide6 import QtWidgets, QtCore, QtGui
from CSS import rent_a_car_window_css as css
from CSS.rent_a_car_window_css import vehicle_info_box
from database import db_service
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
            user_screen_geometry.height() - header.height(),
        )

        self.move(0, header.height())

        self.car_options_side_menu = CarOptionsSideMenu(self)
        self.car_infomations_view = CarInformationsView(self)




class CarOptionsSideMenu(QtWidgets.QLabel):
    def __init__(self, rent_a_car_window):
        super(CarOptionsSideMenu, self).__init__(parent=rent_a_car_window)
        self.setStyleSheet(css.car_options_side_menu)

        windows_navbar_bottom_height = 25

        self.setFixedSize(
            rent_a_car_window.width() * 1 / 3,
            rent_a_car_window.height() - 125
        )

        self.move(
            rent_a_car_window.width() // 4 - self.width() // 2,
            (rent_a_car_window.height() - windows_navbar_bottom_height) // 2 - self.height() // 2
        )

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
        self.cars_grid_conteiner.setFixedWidth(self.scroll_area.width() - 40)
        self.scroll_area.setWidget(self.cars_grid_conteiner)

        for vehicle in db_service.get_available_vehicles():
            print(vehicle)
            vehicle_info_box = QtWidgets.QPushButton(
                f"{vehicle[4]} {vehicle[3]}, {vehicle[5]}"
            )
            vehicle_info_box.info = {
                'id': vehicle[0],
                'id_owner': vehicle[1],
                'chassi_number': vehicle[2],
                'year_of_manufacture': vehicle[3],
                'model': vehicle[4],
                'color': vehicle[5],
                'plate': vehicle[6],
                'car_return_location': vehicle[7],
                'rented': vehicle[8]
            }

            vehicle_info_box.setStyleSheet(css.vehicle_info_box)
            vehicle_info_box.setFixedSize(self.cars_grid_conteiner.width() - 20, 80)
            vehicle_info_box.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

            vehicle_info_box.enterEvent = (
                lambda mouse_event, box=vehicle_info_box: self.vehicle_info_box_enter(box)
            )
            vehicle_info_box.leaveEvent = (
                lambda mouse_event, box=vehicle_info_box: self.vehicle_info_box_leave(box)
            )
            vehicle_info_box.clicked.connect(
                lambda mouse_event, box=vehicle_info_box: self.vehicle_info_box_clicked(box)
            )

            self.cars_grid.addWidget(vehicle_info_box)
            self.resize_object_based_on_window_size()


    def vehicle_info_box_enter(self, vehicle_info_box_target):
        vehicle_info_box_target.setStyleSheet(css.vehicle_info_box_enter)

    def vehicle_info_box_leave(self, vehicle_info_box_target):
        vehicle_info_box_target.setStyleSheet(css.vehicle_info_box)

    def vehicle_info_box_clicked(self, vehicle_info_box_target):
        print(vehicle_info_box_target.info)

    def resize_object_based_on_window_size(self):
        rent_a_car_window_ = self.parent()
        windows_navbar_bottom_height_ = 25

        if rent_a_car_window_.width() <= 1280:
            self.setFixedWidth(
                rent_a_car_window_.width() // 2 - 150,
            )

            self.move(
                rent_a_car_window_.width() // 4 - self.width() // 2,
                (rent_a_car_window_.height() - windows_navbar_bottom_height_) // 2 - self.height() // 2
            )

            self.scroll_area.setFixedWidth(self.width() - 20)
            self.cars_grid_conteiner.setFixedWidth(self.scroll_area.width() - 40)

            for i in range(self.cars_grid.count()):
                item = self.cars_grid.itemAt(i)
                if item.widget() is not None:
                    vehicle_info_box = item.widget()
                    vehicle_info_box.setFixedSize(self.cars_grid_conteiner.width() - 20, 80)


class CarInformationsView(QtWidgets.QLabel):
    def __init__(self, rent_a_car_window):
        super(CarInformationsView, self).__init__(parent=rent_a_car_window)

        default_font = QtGui.QFont()
        default_font.setFamily("Segoe UI")
        default_font.setPixelSize(24)
        windows_navbar_bottom_height = 25

        self.setStyleSheet(css.car_informations_view)

        self.setFixedSize(rent_a_car_window.width() // 2, rent_a_car_window.height())

        self.move(
            rent_a_car_window.width() // 2,
            0
        )

        self.informations_section = QtWidgets.QLabel(parent=self)
        self.informations_section.setFixedWidth(
            self.width()
        )
        self.informations_section.setStyleSheet(css.informations_section)

        self.car_image = QtWidgets.QLabel(parent=self.informations_section)
        self.car_image.setPixmap(
            QtGui.QPixmap(Path(__file__).parent / 'images/3d-car.png').scaled(250, 225)
        )
        self.car_image.move(
            self.width()//2 - self.car_image.pixmap().width()//2,
            0
        )

        self.lbl_car_name = QtWidgets.QLabel("O nome do carro vai aqui", parent=self.informations_section)
        self.lbl_car_name.setStyleSheet(css.lbl_car_info)
        self.lbl_car_name.setFont(default_font)
        self.lbl_car_name.setFixedWidth(
            QtGui.QFontMetrics(default_font).horizontalAdvance(self.lbl_car_name.text())
        )
        self.lbl_car_name.move(
            self.width()//2 - self.lbl_car_name.width()//2,
            self.car_image.y() + self.car_image.pixmap().height() + 20
        )

        self.lbl_car_color = QtWidgets.QLabel("Cor da pintura: Default", parent=self.informations_section)
        self.lbl_car_color.setStyleSheet(css.lbl_car_info)
        self.lbl_car_color.setFont(default_font)
        self.lbl_car_color.setFixedWidth(
            QtGui.QFontMetrics(default_font).horizontalAdvance(self.lbl_car_color.text())
        )
        self.lbl_car_color.move(
            self.width()//2 - self.lbl_car_color.width()//2,
            self.lbl_car_name.y() + self.lbl_car_name.height() + 20
        )

        self.lbl_car_year = QtWidgets.QLabel("2025", parent=self.informations_section)
        self.lbl_car_year.setStyleSheet(css.lbl_car_info)
        self.lbl_car_year.setFont(default_font)
        self.lbl_car_year.setFixedWidth(
            QtGui.QFontMetrics(default_font).horizontalAdvance(self.lbl_car_year.text())
        )
        self.lbl_car_year.move(
            self.width()//2 - self.lbl_car_year.width()//2,
            self.lbl_car_color.y() + self.lbl_car_color.height() + 20
        )

        self.lbl_car_plate = QtWidgets.QLabel("Placa:", parent=self.informations_section)
        self.lbl_car_plate.setStyleSheet(css.lbl_car_info)
        self.lbl_car_plate.setFont(default_font)
        self.lbl_car_plate.setFixedWidth(
            QtGui.QFontMetrics(default_font).horizontalAdvance(self.lbl_car_plate.text())
        )
        self.lbl_car_plate.move(
            self.width()//2 - self.lbl_car_plate.width()//2,
            self.lbl_car_year.y() + self.lbl_car_year.height() + 20
        )

        self.lbl_car_return_location = QtWidgets.QLabel("Localização:", parent=self.informations_section)
        self.lbl_car_return_location.setStyleSheet(css.lbl_car_info)
        self.lbl_car_return_location.setFont(default_font)
        self.lbl_car_return_location.setFixedWidth(
            QtGui.QFontMetrics(default_font).horizontalAdvance(self.lbl_car_return_location.text())
        )
        self.lbl_car_return_location.move(
            self.width()//2 - self.lbl_car_return_location.width()//2,
            self.lbl_car_plate.y() + self.lbl_car_plate.height() + 20
        )

        self.informations_section.setFixedHeight(
            self.car_image.pixmap().height() +
            self.lbl_car_color.height() * 5 +
            20 * 5
        )
        self.informations_section.move(
            self.width()//2 - self.informations_section.width() // 2,
            self.height()//2 - self.informations_section.height() // 2 - windows_navbar_bottom_height
        )
