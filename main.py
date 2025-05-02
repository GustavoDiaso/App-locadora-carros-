from PySide6 import QtWidgets, QtCore, QtGui
from CSS import css
from dotenv import dotenv_values
import sqlite3

# importing our modules
import database.db_service as db_service
import login_and_registration_page_widgets as lrwidgets
import informative_popup as infpopup
import driver_and_vehicle_objects
import header



class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setStyleSheet(css.main_window)

        user_screen = QtGui.QGuiApplication.primaryScreen()
        user_screen_geometry = user_screen.availableGeometry()
        self.setMinimumSize(user_screen_geometry.width(), user_screen_geometry.height())

        self.logged_in_user = driver_and_vehicle_objects.Driver(
             full_name='Nomefalso Johnson',
             cpf='98765432109',
             birth_date='19/06/2004',
             address='Rua Guarian da Silva - SP - 3232',
             phone='11_983475637',
             email='nomefalso@gmail.com',
             password='1',
             cnh='4875162200',
        )

        self.login_and_registration_window = lrwidgets.LoginAndRegistrationWindow(parent=self)
        self.login_and_registration_window.hide()

        self.informative_popup = infpopup.InformativePopUp(parent=self)

        self.header = header.Header(parent=self)


if __name__ == "__main__":
    connection = sqlite3.connect(db_service.env_variables['DB_PATH'])
    db_service.set_connection(connection)
    db_service.create_table_drivers()
    db_service.create_table_vehicles()

    app = QtWidgets.QApplication()
    main_window = MainWindow()
    main_window.showMaximized()
    app.exec()

    db_service.clear_table(table_name="drivers")
    connection.close()
