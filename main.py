from PySide6 import QtWidgets, QtCore, QtGui
from CSS import css
from pathlib import Path
import sqlite3
import database.prepared_sql_queries as psq
from database.prepared_sql_queries import register_new_driver

DATABASE_PATH = Path(__file__).parent / "database/database.sqlite3"
connection = sqlite3.connect(DATABASE_PATH)

psq.create_table_drivers(connection=connection)
psq.create_table_vehicles(connection=connection)


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setStyleSheet(css.main_window)

        user_screen = QtGui.QGuiApplication.primaryScreen()
        user_screen_geometry = user_screen.availableGeometry()
        self.setMinimumSize(user_screen_geometry.width(), user_screen_geometry.height())

        registration_forms = RegistrationForms(parent=self)


class RegistrationForms(QtWidgets.QLabel):
    def __init__(self, parent: MainWindow):
        super(RegistrationForms, self).__init__(parent=parent)
        self.setStyleSheet(css.registration_forms)

        user_screen = QtGui.QGuiApplication.primaryScreen()
        user_screen_geometry = user_screen.availableGeometry()
        self.setMinimumSize(645, user_screen_geometry.height())

        self.move(0, 0)

        margin_left = 30
        space_between_elements = 5
        inputs_width = self.width() - margin_left * 2
        inputs_height = 30

        driver_informations_section = QtWidgets.QLabel(parent=self)
        driver_informations_section.setStyleSheet(css.driver_informations_section)
        driver_informations_section.setFixedSize(self.width(), self.height())
        driver_informations_section.move(0, 0)

        driver_section_title = QtWidgets.QLabel(
            "Cadastro de motorista", parent=driver_informations_section
        )
        driver_section_title.setFixedWidth(355)
        driver_section_title.setStyleSheet(css.registration_title)
        driver_section_title.move(
            self.width() // 2 - driver_section_title.width() // 2, 50
        )

        lbl_fullname = QtWidgets.QLabel(
            "Nome completo:", parent=driver_informations_section
        )
        lbl_fullname.setStyleSheet(css.registration_label_guide)
        lbl_fullname.move(
            margin_left, driver_section_title.y() + driver_section_title.height() + 50
        )

        input_fullname = QtWidgets.QLineEdit(parent=driver_informations_section)
        input_fullname.setStyleSheet(css.registration_input)
        input_fullname.setFixedSize(inputs_width, inputs_height)
        input_fullname.setMaxLength(100)
        input_fullname.move(
            margin_left,
            lbl_fullname.y() + lbl_fullname.height() + space_between_elements,
        )

        lbl_cpf = QtWidgets.QLabel("CPF:", parent=driver_informations_section)
        lbl_cpf.setStyleSheet(css.registration_label_guide)
        lbl_cpf.move(
            margin_left,
            input_fullname.y() + inputs_height + (space_between_elements * 5),
        )

        # title = QtWidgets.QLabel("Cadastro de veículo", parent=self)
        # title.setFixedWidth(315)
        # title.setStyleSheet(css.registration_title)
        # title.move(self.width() // 2 - title.width() // 2, 40)

        # title = QtWidgets.QLabel("Cadastro de veículo", parent=self)
        # title.setFixedWidth(315)
        # title.setStyleSheet(css.registration_title)
        # title.move(self.width() // 2 - title.width() // 2, 40)


connection.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    main_window = MainWindow()
    main_window.showMaximized()
    app.exec()
