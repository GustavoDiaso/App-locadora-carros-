from PySide6 import QtWidgets, QtCore, QtGui
from CSS import css
import sqlite3
from pathlib import Path

# importing our modules
import database.db_service as db_service
import login_and_registration_page_widgets as lrwidgets
import informative_popup as infpopup
import driver_and_vehicle_objects
import header
import rent_a_car_page


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setStyleSheet(css.main_window)

        user_screen = QtGui.QGuiApplication.primaryScreen()
        user_screen_geometry = user_screen.availableGeometry()
        self.setMinimumSize(user_screen_geometry.width(), user_screen_geometry.height())

        self.logged_in_user = driver_and_vehicle_objects.Driver(
            full_name="Nomefalso Johnson",
            cpf="98765432109",
            birth_date="19/06/2004",
            address="Rua Guarian da Silva - SP - 3232",
            phone="11_983475637",
            email="nomefalso@gmail.com",
            password="1",
            cnh="4875162200",
        )

        self.login_and_registration_window = lrwidgets.LoginAndRegistrationWindow(
            parent=self
        )
        self.login_and_registration_window.hide()

        self.informative_popup = infpopup.InformativePopUp(parent=self)

        self.header = header.Header(main_window=self)
        self.rent_a_car_window = rent_a_car_page.RentACarWindow(main_window=self)


if __name__ == "__main__":
    # Even if the database already exists, It will be recreated. this helps a lot
    # because I am constantly changing the database.
    # db_service.recreate_sqlite_database(Path(__file__).parent / "database", "database")


    connection = sqlite3.connect(db_service.env_variables["DB_PATH"])
    db_service.set_connection(connection)
    db_service.create_table_drivers()
    db_service.create_table_vehicles()

    # Lets add in the database some random cars I created in the driver_and_vehicle_objects module.
    # for vehicle in driver_and_vehicle_objects.my_vehicle_collection:
    #     db_service.register_new_vehicle(vehicle)

    app = QtWidgets.QApplication()
    main_window = MainWindow()
    main_window.showMaximized()
    app.exec()

    # Since I am testing, I am always cleaning the table drivers.
    db_service.clear_table(table_name="drivers")
    connection.close()
