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
        self.setFixedSize(
            user_screen_geometry.width() * 2 / 5, user_screen_geometry.height()
        )

        self.move(0, 0)

        margin_left = 30
        space_between_elements = 5
        inputs_width = self.width() - margin_left * 2
        inputs_height = 30
        labels_height = 30

        self.driver_registration_title = QtWidgets.QLabel(
            "Cadastro de motorista", parent=self
        )
        self.driver_registration_title.setFixedWidth(355)
        self.driver_registration_title.setStyleSheet(css.registration_title)
        self.driver_registration_title.move(
            self.width() // 2 - self.driver_registration_title.width() // 2,
            self.height()//2
            - 5*(space_between_elements*6 + inputs_height + labels_height)//2
            - self.driver_registration_title.height()//2
            - 80
        )

        self.driver_informations_section1 = QtWidgets.QLabel(parent=self)
        self.driver_informations_section1.setStyleSheet(css.driver_informations_section)
        self.driver_informations_section1.setFixedSize(
            self.width(),
            5*(space_between_elements*6 + inputs_height + labels_height)
        )
        self.driver_informations_section1.move(
            0,
            self.height()//2 - self.driver_informations_section1.height()//2
        )

        self.lbl_fullname = QtWidgets.QLabel(
            "Nome completo:", parent=self.driver_informations_section1
        )
        self.lbl_fullname.setStyleSheet(css.registration_label_guide)
        self.lbl_fullname.move(margin_left, 0)

        self.input_fullname = QtWidgets.QLineEdit(
            parent=self.driver_informations_section1
        )
        self.input_fullname.setStyleSheet(css.registration_input_focused)
        self.input_fullname.setFixedSize(inputs_width, inputs_height)
        self.input_fullname.setMaxLength(100)
        self.input_fullname.move(
            margin_left,
            self.lbl_fullname.y() + self.lbl_fullname.height() + space_between_elements,
        )

        self.lbl_cpf = QtWidgets.QLabel(
            "CPF: (Apenas números)", parent=self.driver_informations_section1
        )
        self.lbl_cpf.setStyleSheet(css.registration_label_guide)
        self.lbl_cpf.move(
            margin_left,
            self.input_fullname.y() + inputs_height + (space_between_elements * 6),
        )

        self.input_cpf = QtWidgets.QLineEdit(parent=self.driver_informations_section1)
        self.input_cpf.setValidator(QtGui.QIntValidator())
        self.input_cpf.setStyleSheet(css.registration_input_focused)
        self.input_cpf.setFixedSize(inputs_width, inputs_height)
        self.input_cpf.setMaxLength(14)
        self.input_cpf.move(
            margin_left,
            self.lbl_cpf.y() + self.lbl_cpf.height() + space_between_elements,
        )

        self.lbl_birth_date = QtWidgets.QLabel(
            "Data de nascimento:", parent=self.driver_informations_section1
        )
        self.lbl_birth_date.setStyleSheet(css.registration_label_guide)
        self.lbl_birth_date.move(
            margin_left,
            self.input_cpf.y() + inputs_height + (space_between_elements * 6),
        )

        self.input_birth_date = QtWidgets.QDateEdit(
            parent=self.driver_informations_section1
        )
        self.input_birth_date.setStyleSheet(css.registration_input_focused)
        self.input_birth_date.setFixedSize(inputs_width, inputs_height)
        self.input_birth_date.move(
            margin_left,
            self.lbl_birth_date.y()
            + self.lbl_birth_date.height()
            + space_between_elements,
        )

        # Yes, I know it would be better to separate the adress into street, number and neighborhood
        # This is just a simple project to show my abilities
        self.lbl_address = QtWidgets.QLabel(
            "Endereço:", parent=self.driver_informations_section1
        )
        self.lbl_address.setStyleSheet(css.registration_label_guide)
        self.lbl_address.move(
            margin_left,
            self.input_birth_date.y() + inputs_height + (space_between_elements * 6),
        )

        self.input_address = QtWidgets.QLineEdit(
            parent=self.driver_informations_section1
        )
        self.input_address.setStyleSheet(css.registration_input_focused)
        self.input_address.setFixedSize(inputs_width, inputs_height)
        self.input_address.setMaxLength(150)
        self.input_address.move(
            margin_left,
            self.lbl_address.y() + self.lbl_address.height() + space_between_elements,
        )

        self.lbl_phone = QtWidgets.QLabel(
            "Telefone:", parent=self.driver_informations_section1
        )
        self.lbl_phone.setStyleSheet(css.registration_label_guide)
        self.lbl_phone.move(
            margin_left,
            self.input_address.y() + inputs_height + (space_between_elements * 6),
        )

        self.input_ddd = QtWidgets.QLineEdit(
            "DDD", parent=self.driver_informations_section1
        )
        self.input_ddd.setStyleSheet(css.registration_input)
        self.input_ddd.setValidator(QtGui.QIntValidator())
        self.input_ddd.setFixedSize(70, inputs_height)
        self.input_ddd.setMaxLength(3)
        self.input_ddd.move(
            margin_left,
            self.lbl_phone.y() + self.lbl_phone.height() + space_between_elements,
        )
        self.input_ddd.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        # Quando pressionado, um widget chama automaticamente o metodo interno mousePressEvent(event), passando
        # o evento ocorrido como argumento. O que eu estou fazendo aqui é basicamente sobrescrever o metodo
        # mousePressEvent original, atribuindo a esse identificador uma nova função.
        self.input_ddd.mousePressEvent = lambda event: self.toggle_placeholder(
            event, self.input_ddd, "DDD"
        )
        self.input_ddd.focusOutEvent = lambda event: self.toggle_placeholder(
            event, self.input_ddd, "DDD"
        )

        self.input_number = QtWidgets.QLineEdit(
            "999999999", parent=self.driver_informations_section1
        )
        self.input_number.setValidator(QtGui.QIntValidator())
        self.input_number.setStyleSheet(css.registration_input)
        self.input_number.setFixedSize(
            inputs_width - margin_left - self.input_ddd.width(), inputs_height
        )
        self.input_number.setMaxLength(9)
        self.input_number.move(
            (margin_left * 2) + self.input_ddd.width(),
            self.lbl_phone.y() + self.lbl_phone.height() + space_between_elements,
        )
        self.input_number.mousePressEvent = lambda event: self.toggle_placeholder(event, self.input_number, "999999999")
        self.input_number.focusOutEvent = lambda event: self.toggle_placeholder(event, self.input_number, "999999999")

        self.next_page_driver_button = QtWidgets.QPushButton("Next page >", parent=self)
        self.next_page_driver_button.setFixedSize(100, 40)
        self.next_page_driver_button.move(
            self.width() - margin_left - self.next_page_driver_button.width(),
            self.height() - self.next_page_driver_button.height() * 3,
        )
        self.next_page_driver_button.state = "deactivated"
        self.next_page_driver_button.clicked.connect(self.next_drivers_page)

        self.driver_informations_section2 = QtWidgets.QLabel(parent=self)
        self.driver_informations_section2.setStyleSheet(css.driver_informations_section)
        self.driver_informations_section2.setFixedSize(
            self.width(),
            self.driver_informations_section1.height()
        )
        self.driver_informations_section2.move(
            0,
            self.driver_informations_section1.y()
        )
        self.driver_informations_section2.setVisible(False)

        self.lbl_email = QtWidgets.QLabel(
            "E-mail:", parent=self.driver_informations_section2
        )
        self.lbl_email.setStyleSheet(css.registration_label_guide)
        self.lbl_email.move(
            margin_left,
            0
        )


        self.input_email = QtWidgets.QLineEdit(
            parent=self.driver_informations_section2
        )
        self.input_email.setStyleSheet(css.registration_input_focused)
        self.input_email.setFixedSize(inputs_width, inputs_height)
        self.input_email.setMaxLength(256)
        self.input_email.move(
            margin_left,
            self.lbl_email.y() + self.lbl_email.height() + space_between_elements,
        )

        # criando uma expressão regular validadora que impede a utilização de caracteres não apropriados
        # para o endereço de email. (isso não impede que o usuário insira um endereço de email inválido)
        regex = QtCore.QRegularExpression(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
        validator = QtGui.QRegularExpressionValidator(regex)
        self.input_email.setValidator(validator)

        self.lbl_cnh = QtWidgets.QLabel(
            "Número de registro da CNH:", parent=self.driver_informations_section2
        )
        self.lbl_cnh.setStyleSheet(css.registration_label_guide)
        self.lbl_cnh.move(
            margin_left,
            self.input_email.y() + self.input_email.height() + space_between_elements*6
        )


        self.input_cnh = QtWidgets.QLineEdit(
            parent=self.driver_informations_section2
        )
        self.input_cnh.setStyleSheet(css.registration_input_focused)
        self.input_cnh.setFixedSize(inputs_width, inputs_height)
        self.input_cnh.setMaxLength(11)
        self.input_cnh.move(
            margin_left,
            self.lbl_cnh.y() + self.lbl_cnh.height() + space_between_elements,
        )
        self.input_cnh.setValidator(QtGui.QIntValidator())


        self.lbl_password = QtWidgets.QLabel(
            "Senha:", parent=self.driver_informations_section2
        )
        self.lbl_password.setStyleSheet(css.registration_label_guide)
        self.lbl_password.move(
            margin_left,
            self.input_cnh.y() + self.input_cnh.height() + space_between_elements*6
        )

        self.input_password_first = QtWidgets.QLineEdit(
            parent=self.driver_informations_section2
        )

        self.input_password_first.setStyleSheet(css.registration_input_focused)
        self.input_password_first.setFixedSize(inputs_width, inputs_height)
        self.input_password_first.move(
            margin_left,
            self.lbl_password.y() + self.lbl_password.height() + space_between_elements,
        )
        self.input_password_first.mousePressEvent = (
            lambda event: (
                self.toggle_placeholder(event, self.input_password_first),
                self.enter_password_mode(self.input_password_first)
            )

        )
        self.input_password_first.focusOutEvent = (
            lambda event: (
                self.toggle_placeholder(event, self.input_password_first),
                self.exit_password_mode(event, self.input_password_first)
            )
        )


        self.input_password_second = QtWidgets.QLineEdit(
            "Confirme sua senha", parent=self.driver_informations_section2
        )
        self.input_password_second.setStyleSheet(css.registration_input)
        self.input_password_second.setFixedSize(inputs_width, inputs_height)
        self.input_password_second.move(
            margin_left,
            self.input_password_first.y() + inputs_height + space_between_elements*6,
        )
        self.input_password_second.mousePressEvent = (
            lambda event: (
                self.toggle_placeholder(event, self.input_password_second, "Confirme sua senha"),
                self.enter_password_mode(self.input_password_second)
            )

        )
        self.input_password_second.focusOutEvent = (
            lambda event: (
                self.toggle_placeholder(event, self.input_password_second, "Confirme sua senha"),
                self.exit_password_mode(event, self.input_password_second, 'Confirme sua senha'),
                self.check_matching_passwords()
            )
        )

        self.lbl_pwrd_dont_match = QtWidgets.QLabel("As senhas não coincidem", parent=self.driver_informations_section2)
        self.lbl_pwrd_dont_match.move(
            self.driver_informations_section2.width() // 2 - self.lbl_pwrd_dont_match.width() // 2,
            self.input_password_second.y() + self.input_password_second.height() + 40
        )
        self.lbl_pwrd_dont_match.setVisible(False)



        self.driver_informations_section1.raise_()


    # Daqui para frente estão os métodos (slots) que serão executados na disparada de eventos pelos obj da UX/UI
    def toggle_placeholder(self, event, target_input, placeholder=''):
        if isinstance(event, QtGui.QMouseEvent):
            if event.button().LeftButton:
                target_input.setReadOnly(False)

                if target_input.text() == placeholder:
                    target_input.setStyleSheet(css.registration_input_focused)
                    target_input.setText("")

        if isinstance(event, QtGui.QFocusEvent):
            if event.lostFocus():
                if target_input.text() == "":
                    target_input.setStyleSheet(css.registration_input)
                    target_input.setText(placeholder)

                target_input.setReadOnly(True)

    def next_drivers_page(self):
        if self.next_page_driver_button.state == "deactivated":
            self.next_page_driver_button.state = "activated"
            self.driver_informations_section1.setVisible(False)
            self.driver_informations_section2.setVisible(True)
            self.next_page_driver_button.setText("< Last page")
            self.driver_informations_section2.raise_()
        else:
            self.next_page_driver_button.state = "deactivated"
            self.next_page_driver_button.setText("Next page >")
            self.driver_informations_section1.setVisible(True)
            self.driver_informations_section2.setVisible(False)
            self.driver_informations_section1.raise_()


    def enter_password_mode(self, target_input: QtWidgets.QLineEdit):
        if target_input.echoMode() == QtWidgets.QLineEdit.EchoMode.Normal:
            target_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def exit_password_mode(self, event, target_input: QtWidgets.QLineEdit, placeholder=''):
        if isinstance(event, QtGui.QFocusEvent):
            if event.lostFocus():
                if target_input.text() == '' or target_input.text() == placeholder:
                    target_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
                    target_input.setText(placeholder)

        elif isinstance(event, QtGui.QMouseEvent):
            if event.button().LeftButton:
                target_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)


    def check_matching_passwords(self):
        if self.input_password_first.text() != self.input_password_second.text():
            self.lbl_pwrd_dont_match.setVisible(True)
        else:
            self.lbl_pwrd_dont_match.setVisible(False)


connection.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    main_window = MainWindow()
    main_window.showMaximized()
    app.exec()
