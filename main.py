from PySide6 import QtWidgets, QtCore, QtGui
from win32api import mouse_event

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
        input_fullname.setStyleSheet(css.registration_input_focused)
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
            input_fullname.y() + inputs_height + (space_between_elements * 6),
        )

        input_cpf = QtWidgets.QLineEdit(parent=driver_informations_section)
        input_cpf.setStyleSheet(css.registration_input_focused)
        input_cpf.setFixedSize(inputs_width, inputs_height)
        input_cpf.setMaxLength(14)
        input_cpf.move(
            margin_left,
            lbl_cpf.y() + lbl_cpf.height() + space_between_elements
        )

        lbl_birth_date = QtWidgets.QLabel("Data de nascimento:", parent=driver_informations_section)
        lbl_birth_date.setStyleSheet(css.registration_label_guide)
        lbl_birth_date.move(
            margin_left,
            input_cpf.y() + inputs_height + (space_between_elements * 6),
        )

        input_birth_date = QtWidgets.QDateEdit(parent=driver_informations_section)
        input_birth_date.setStyleSheet(css.registration_input_focused)
        input_birth_date.setFixedSize(inputs_width, inputs_height)
        input_birth_date.move(
            margin_left,
            lbl_birth_date.y() + lbl_birth_date.height() + space_between_elements
        )

        # Yes, I know it would be better to separate the adress into street, number and neighborhood
        # This is just a simple project to show my abilities
        lbl_address = QtWidgets.QLabel("Endereço:", parent=driver_informations_section)
        lbl_address.setStyleSheet(css.registration_label_guide)
        lbl_address.move(
            margin_left,
            input_birth_date.y() + inputs_height + (space_between_elements * 6),
        )

        input_address = QtWidgets.QLineEdit(parent=driver_informations_section)
        input_address.setStyleSheet(css.registration_input_focused)
        input_address.setFixedSize(inputs_width, inputs_height)
        input_address.setMaxLength(150)
        input_address.move(
            margin_left,
            lbl_address.y() + lbl_address.height() + space_between_elements
        )

        lbl_phone = QtWidgets.QLabel("Telefone:", parent=driver_informations_section)
        lbl_phone.setStyleSheet(css.registration_label_guide)
        lbl_phone.move(
            margin_left,
            input_address.y() + inputs_height + (space_between_elements * 6),
        )

        input_ddd = QtWidgets.QLineEdit("DDD",parent=driver_informations_section)
        input_ddd.setStyleSheet(css.registration_input)
        input_ddd.setFixedSize(70, inputs_height)
        input_ddd.setMaxLength(3)
        input_ddd.move(
            margin_left,
            lbl_phone.y() + lbl_phone.height() + space_between_elements
        )
        input_ddd.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        # Quando pressionado, um widget chama automaticamente o metodo interno mousePressEvent(event), passando
        # o evento ocorrido como argumento. O que eu estou fazendo aqui é basicamente sobrescrever o metodo
        # mousePressEvent original, atribuindo a esse identificador uma nova função.
        input_ddd.mousePressEvent = lambda event: self.input_toggle_placeholder(input_ddd, "DDD")
        input_ddd.focusOutEvent = lambda event: self.input_toggle_placeholder(input_ddd, "DDD")

        input_number = QtWidgets.QLineEdit(parent=driver_informations_section)
        input_number.setStyleSheet(css.registration_input_focused)
        input_number.setFixedSize(inputs_width - margin_left - input_ddd.width(), inputs_height)
        input_number.setMaxLength(9)
        input_number.move(
            (margin_left*2) + input_ddd.width(),
            lbl_phone.y() + lbl_phone.height() + space_between_elements
        )

    def input_toggle_placeholder(self, target_input, placeholder):
        if target_input.text() == placeholder:
            target_input.setText("")
            target_input.setReadOnly(False)
            target_input.setStyleSheet(css.registration_input_focused)
        else:
            target_input.setText(placeholder)
            target_input.setReadOnly(True)
            target_input.setStyleSheet(css.registration_input)


connection.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    main_window = MainWindow()
    main_window.showMaximized()
    app.exec()
