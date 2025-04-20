from PySide6 import QtWidgets, QtCore, QtGui
from datetime import datetime, timedelta
from CSS import css
from pathlib import Path
import sqlite3
import database.prepared_sql_queries as psq
import re


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

        self.logged_in_user = None

        self.login_or_register_window = LoginOrRegisterSideMenu(parent=self)
        self.login_or_register_window.hide()

        self.driver_registration_form = DriverRegistrationForm(parent=self)

        self.driver_login_form = DriverLoginForm(parent=self)

        self.informative_popup = InformativePopUp(parent=self)


class DriverRegistrationForm(QtWidgets.QLabel):
    def __init__(self, parent: MainWindow):
        super(DriverRegistrationForm, self).__init__(parent=parent)
        self.setVisible(False)
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
            self.height() // 2
            - 5 * (space_between_elements * 6 + inputs_height + labels_height) // 2
            - self.driver_registration_title.height() // 2
            - 80,
        )

        self.btn_go_back = QtWidgets.QPushButton("<", parent=self)
        self.btn_go_back.setFixedSize(30, 30)
        self.btn_go_back.move(margin_left, self.driver_registration_title.y() + 10)
        self.btn_go_back.setCursor(QtGui.Qt.CursorShape.PointingHandCursor)
        self.btn_go_back.setStyleSheet(css.btn_go_back)
        self.btn_go_back.clicked.connect(self.back_to_main_window)

        self.driver_informations_section1 = QtWidgets.QLabel(parent=self)
        self.driver_informations_section1.setStyleSheet(css.driver_informations_section)
        self.driver_informations_section1.setFixedSize(
            self.width(),
            5 * (space_between_elements * 6 + inputs_height + labels_height),
        )
        self.driver_informations_section1.move(
            0, self.height() // 2 - self.driver_informations_section1.height() // 2
        )

        self.lbl_fullname = QtWidgets.QLabel(
            "Nome completo:", parent=self.driver_informations_section1
        )
        self.lbl_fullname.setStyleSheet(css.registration_label_guide)
        self.lbl_fullname.move(margin_left, 0)

        self.input_fullname = QtWidgets.QLineEdit(
            parent=self.driver_informations_section1
        )
        self.input_fullname.setValidator(
            QtGui.QRegularExpressionValidator("[a-zA-Z\\s]+")
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

        self.input_cpf.setValidator(QtGui.QRegularExpressionValidator("[0-9]{11}"))
        self.input_cpf.setStyleSheet(css.registration_input_focused)
        self.input_cpf.setFixedSize(inputs_width, inputs_height)
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
        self.input_address.setValidator(
            QtGui.QRegularExpressionValidator(
                "[a-zA-Z0-9,áéíóúãõôâçÁÉÍÓÚÃÕÔÂÇ\\.\\-\\s]+"
            )
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
        self.input_number.mousePressEvent = lambda event: self.toggle_placeholder(
            event, self.input_number, "999999999"
        )
        self.input_number.focusOutEvent = lambda event: self.toggle_placeholder(
            event, self.input_number, "999999999"
        )

        self.driver_informations_section2 = QtWidgets.QLabel(parent=self)
        self.driver_informations_section2.setStyleSheet(css.driver_informations_section)
        self.driver_informations_section2.setFixedSize(
            self.width(), self.driver_informations_section1.height()
        )
        self.driver_informations_section2.move(0, self.driver_informations_section1.y())
        self.driver_informations_section2.setVisible(False)

        self.lbl_email = QtWidgets.QLabel(
            "E-mail:", parent=self.driver_informations_section2
        )
        self.lbl_email.setStyleSheet(css.registration_label_guide)
        self.lbl_email.move(margin_left, 0)

        self.input_email = QtWidgets.QLineEdit(parent=self.driver_informations_section2)
        self.input_email.setStyleSheet(css.registration_input_focused)
        self.input_email.setFixedSize(inputs_width, inputs_height)
        self.input_email.setMaxLength(256)
        self.input_email.move(
            margin_left,
            self.lbl_email.y() + self.lbl_email.height() + space_between_elements,
        )

        # criando uma expressão regular validadora que impede a utilização de caracteres não apropriados
        # para o endereço de email. (isso não impede que o usuário insira um endereço de email inválido)
        regex = QtCore.QRegularExpression(
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        )
        validator = QtGui.QRegularExpressionValidator(regex)
        self.input_email.setValidator(validator)

        self.lbl_cnh = QtWidgets.QLabel(
            "Número de registro da CNH:", parent=self.driver_informations_section2
        )
        self.lbl_cnh.setStyleSheet(css.registration_label_guide)
        self.lbl_cnh.move(
            margin_left,
            self.input_email.y()
            + self.input_email.height()
            + space_between_elements * 6,
        )

        self.input_cnh = QtWidgets.QLineEdit(parent=self.driver_informations_section2)
        self.input_cnh.setStyleSheet(css.registration_input_focused)
        self.input_cnh.setFixedSize(inputs_width, inputs_height)
        self.input_cnh.move(
            margin_left,
            self.lbl_cnh.y() + self.lbl_cnh.height() + space_between_elements,
        )
        self.input_cnh.setValidator(QtGui.QRegularExpressionValidator("[0-9]{11}"))

        self.lbl_password = QtWidgets.QLabel(
            "Senha:", parent=self.driver_informations_section2
        )
        self.lbl_password.setStyleSheet(css.registration_label_guide)
        self.lbl_password.move(
            margin_left,
            self.input_cnh.y() + self.input_cnh.height() + space_between_elements * 6,
        )

        self.input_password_first = QtWidgets.QLineEdit(
            parent=self.driver_informations_section2
        )
        self.input_password_first.setMaxLength(25)
        self.input_password_first.setStyleSheet(css.registration_input_focused)
        self.input_password_first.setFixedSize(inputs_width, inputs_height)
        self.input_password_first.move(
            margin_left,
            self.lbl_password.y() + self.lbl_password.height() + space_between_elements,
        )
        self.input_password_first.mousePressEvent = lambda event: (
            self.toggle_placeholder(event, self.input_password_first),
            self.enter_password_mode(self.input_password_first),
        )
        self.input_password_first.focusOutEvent = lambda event: (
            self.toggle_placeholder(event, self.input_password_first),
            self.exit_password_mode(event, self.input_password_first),
        )

        self.input_password_second = QtWidgets.QLineEdit(
            "Confirme sua senha", parent=self.driver_informations_section2
        )
        self.input_password_second.setMaxLength(25)
        self.input_password_second.setStyleSheet(css.registration_input)
        self.input_password_second.setFixedSize(inputs_width, inputs_height)
        self.input_password_second.move(
            margin_left,
            self.input_password_first.y() + inputs_height + space_between_elements * 6,
        )
        self.input_password_second.mousePressEvent = lambda event: (
            self.toggle_placeholder(
                event, self.input_password_second, "Confirme sua senha"
            ),
            self.enter_password_mode(self.input_password_second),
        )
        self.input_password_second.focusOutEvent = lambda event: (
            self.toggle_placeholder(
                event, self.input_password_second, "Confirme sua senha"
            ),
            self.exit_password_mode(
                event, self.input_password_second, "Confirme sua senha"
            ),
        )

        self.lbl_pwrd_dont_match = QtWidgets.QLabel(
            "As senhas não coincidem!", parent=self.driver_informations_section2
        )
        self.lbl_pwrd_dont_match.move(
            margin_left,
            self.input_password_second.y() + self.input_password_second.height() + 40,
        )
        self.lbl_pwrd_dont_match.setVisible(False)
        self.lbl_pwrd_dont_match.setStyleSheet(
            """
                font-family: Segoe UI;
                color: white;
                font-size: 14px;
            """
        )

        self.input_email.focusOutEvent = lambda event: self.check_valid_email()
        self.input_email.mousePressEvent = lambda event: self.input_email.setReadOnly(
            False
        )

        self.btn_register_driver = QtWidgets.QPushButton(
            "Cadastrar", parent=self.driver_informations_section2
        )
        self.btn_register_driver.setFixedSize(120, 60)
        self.btn_register_driver.setStyleSheet(css.login_and_register_buttons)
        self.btn_register_driver.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_register_driver.move(
            self.driver_informations_section2.width() // 2
            - self.btn_register_driver.width() // 2,
            self.input_password_second.y() + inputs_height + space_between_elements * 6,
        )
        self.btn_register_driver.clicked.connect(
            lambda: self.save_driver_informations()
        )

        # Esse comando faz com que a seção 1 da tela de cadastro de motoristas apareça antes
        # da seção 2.
        self.driver_informations_section1.raise_()

        # Criando um botão para navegar entre as páginas do formulário de cadastro de motoristas
        self.btn_next_stage_driver_info = QtWidgets.QPushButton(
            "Next page >", parent=self
        )
        self.btn_next_stage_driver_info.setFixedSize(100, 40)
        self.btn_next_stage_driver_info.move(
            self.width() - margin_left - self.btn_next_stage_driver_info.width(),
            self.driver_informations_section1.y()
            + self.driver_informations_section1.height()
            + 35,
        )
        self.btn_next_stage_driver_info.state = "deactivated"
        self.btn_next_stage_driver_info.clicked.connect(self.next_drivers_page)

    # Daqui para frente estão os métodos (slots) que serão executados na disparada de eventos pelos obj da UX/UI
    def toggle_placeholder(self, event, target_input, placeholder=""):
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

    def back_to_main_window(self):
        main_window: MainWindow = self.parent()
        main_window.login_or_register_window.show()
        self.hide()

    def next_drivers_page(self):
        print(self.check_valid_birthdate())

        if self.btn_next_stage_driver_info.state == "deactivated":
            self.btn_next_stage_driver_info.state = "activated"
            self.driver_informations_section1.setVisible(False)
            self.driver_informations_section2.setVisible(True)
            self.btn_next_stage_driver_info.setText("< Last page")
            self.driver_informations_section2.raise_()
            self.btn_next_stage_driver_info.raise_()
        else:
            self.btn_next_stage_driver_info.state = "deactivated"
            self.btn_next_stage_driver_info.setText("Next page >")
            self.driver_informations_section1.setVisible(True)
            self.driver_informations_section2.setVisible(False)
            self.driver_informations_section1.raise_()
            self.btn_next_stage_driver_info.raise_()

    def enter_password_mode(self, target_input: QtWidgets.QLineEdit):
        if target_input.echoMode() == QtWidgets.QLineEdit.EchoMode.Normal:
            target_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        target_input.setReadOnly(False)
        target_input.setFocus()

    def exit_password_mode(
        self, event, target_input: QtWidgets.QLineEdit, placeholder=""
    ):
        if isinstance(event, QtGui.QFocusEvent):
            if event.lostFocus():
                if target_input.text() == "" or target_input.text() == placeholder:
                    target_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
                    target_input.setText(placeholder)

                target_input.clearFocus()

        elif isinstance(event, QtGui.QMouseEvent):
            if event.button().LeftButton:
                target_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)

    def check_matching_passwords(self):
        if self.input_password_first.text() == self.input_password_second.text():
            return True

        return False

    def check_valid_email(self):
        email = self.input_email.text()
        self.input_email.setReadOnly(True)

        if (
            re.fullmatch(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", email)
            is not None
        ):
            return True

        return False

    def check_valid_phone_number(self):
        ddd = self.input_ddd.text()
        number = self.input_number.text()

        if ddd != "DDD" and ddd != "" and number != "999999999" and number != "":
            return True

        return False

    def check_valid_cpf(self):
        cpf = self.input_cpf.text()
        sum = 0
        for num in cpf:
            sum += int(num)

        if len(cpf) != 11 or str(sum)[0] != str(sum)[1]:
            return False

        return True

    def check_valid_birthdate(self):
        birth_date = datetime.strptime(self.input_birth_date.text(), r"%d/%m/%Y")
        today = datetime.now()
        years_of_difference = today.year - birth_date.year

        return True if years_of_difference >= 18 else False

    def all_data_provided(self):
        conditions = [
            self.input_address.text() != "",
            self.input_cpf.text() != "",
            self.input_birth_date.text() != "",
            self.input_cnh.text() != "",
            self.input_fullname.text() != "",
            self.input_ddd.text() != "DDD",
            self.input_ddd.text() != "",
            self.input_number.text() != "999999999",
            self.input_number.text() != "",
            self.input_email.text() != "",
            self.input_password_first.text() != "",
            self.input_password_second.text() != "",
            self.input_password_second.text() != "Confirme sua senha",
        ]

        return True if all(conditions) else False

    def clear_driver_forms_inputs(self):
        self.input_address.setText("")
        self.input_birth_date.setDate(QtCore.QDate.currentDate())
        self.input_email.setText("")
        self.input_cnh.setText("")
        self.input_fullname.setText("")
        self.input_ddd.setText("DDD")
        self.input_number.setText("999999999")
        self.input_password_first.setText("")
        self.input_password_second.setText("")

    def save_driver_informations(self):
        special_conditions = [
            self.check_matching_passwords(),
            self.check_valid_email(),
            self.check_valid_phone_number(),
            self.check_valid_cpf(),
            self.check_valid_birthdate(),
        ]
        nothing_empty = self.all_data_provided()

        main_window: MainWindow = self.parent()
        informative_popup: InformativePopUp = main_window.informative_popup

        # Se todas as condições especiais forem satisfeitas e todos os dados tiverem
        # sido fornecidos...
        if all(special_conditions) and nothing_empty:
            full_name = self.input_fullname.text()
            cpf = self.input_cpf.text()
            birth_date = self.input_birth_date.text()
            address = self.input_address.text()
            phone = self.input_ddd.text() + "_" + self.input_number.text()
            email = self.input_email.text()
            password = self.input_password_first.text()
            cnh = self.input_cnh.text()

            driver = psq.Driver(
                full_name=full_name,
                cpf=cpf,
                birth_date=birth_date,
                address=address,
                phone=phone,
                email=email,
                password=password,
                cnh=cnh,
            )
            self.lbl_pwrd_dont_match.setVisible(False)

            # Vamos tentar fazer o cadastro do motorista no banco de dados:
            driver_registration_status = psq.register_new_driver(
                connection=connection, driver=driver
            )

            informative_popup.popup_header.setText("Operação malsucedida")
            informative_popup.lbl_information.setText(driver_registration_status[1])

            # Caso o motorista tenha sido cadastrado com sucesso...
            if driver_registration_status[0] is True:
                self.clear_driver_forms_inputs()
                informative_popup.popup_header.setText("Operação bem-sucedida")

            informative_popup.setVisible(True)

        else:
            if nothing_empty:

                error_message = ""

                for condition, evaluation in enumerate(special_conditions):
                    if evaluation is False:
                        match condition:
                            case 0:
                                error_message = "Senhas não combinam"
                                self.lbl_pwrd_dont_match.setVisible(True)
                            case 1:
                                error_message = "Email inválido"
                            case 2:
                                error_message = "Telefone inválido"
                            case 3:
                                error_message = "CPF inválido"

                informative_popup.popup_header.setText("Operação malsucedida")
                informative_popup.lbl_information.setText(error_message)
                informative_popup.setVisible(True)

            else:
                informative_popup.popup_header.setText("Operação malsucedida")
                informative_popup.lbl_information.setText(
                    "Todos os campos devem ser preenchidos!"
                )
                informative_popup.setVisible(True)


class DriverLoginForm(QtWidgets.QLabel):
    def __init__(self, parent: MainWindow):
        super(DriverLoginForm, self).__init__(parent=parent)
        self.setVisible(False)
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

        self.driver_login_title = QtWidgets.QLabel("Login", parent=self)
        self.driver_login_title.setFixedWidth(len(self.driver_login_title.text()) * 18)
        self.driver_login_title.setStyleSheet(css.registration_title)
        self.driver_login_title.move(
            self.width() // 2 - self.driver_login_title.width() // 2,
            self.height() // 2
            - (labels_height + space_between_elements * 7 + inputs_height) * 3 / 2
            - 90,
        )

        self.btn_go_back = QtWidgets.QPushButton("<", parent=self)
        self.btn_go_back.setFixedSize(30, 30)
        self.btn_go_back.move(margin_left, self.driver_login_title.y() + 10)
        self.btn_go_back.setCursor(QtGui.Qt.CursorShape.PointingHandCursor)
        self.btn_go_back.setStyleSheet(css.btn_go_back)
        self.btn_go_back.clicked.connect(self.back_to_main_window)

        self.login_section = QtWidgets.QLabel(parent=self)
        self.login_section.setFixedSize(
            self.width(),
            (labels_height + space_between_elements * 7 + inputs_height) * 3,
        )
        self.login_section.setStyleSheet(css.login_section)
        self.login_section.move(
            0, self.height() // 2 - self.login_section.height() // 2
        )

        self.lbl_cpf = QtWidgets.QLabel(
            "CPF: (Apenas números)", parent=self.login_section
        )
        self.lbl_cpf.setFixedHeight(labels_height)
        self.lbl_cpf.setStyleSheet(css.registration_label_guide)
        self.lbl_cpf.move(margin_left, 0)

        self.input_cpf = QtWidgets.QLineEdit(parent=self.login_section)

        self.input_cpf.setValidator(QtGui.QRegularExpressionValidator("[0-9]{11}"))
        self.input_cpf.setStyleSheet(css.registration_input_focused)
        self.input_cpf.setFixedSize(inputs_width, inputs_height)
        self.input_cpf.move(
            margin_left,
            self.lbl_cpf.y() + self.lbl_cpf.height() + space_between_elements,
        )

        self.lbl_password = QtWidgets.QLabel("Senha:", parent=self.login_section)
        self.lbl_password.setFixedHeight(labels_height)
        self.lbl_password.setStyleSheet(css.registration_label_guide)
        self.lbl_password.move(
            margin_left, self.input_cpf.y() + inputs_height + space_between_elements * 6
        )

        self.input_password = QtWidgets.QLineEdit(parent=self.login_section)
        self.input_password.setMaxLength(25)
        self.input_password.setStyleSheet(css.registration_input)
        self.input_password.setFixedSize(inputs_width, inputs_height)
        self.input_password.move(
            margin_left,
            self.lbl_password.y() + labels_height + space_between_elements,
        )
        self.input_password.mousePressEvent = lambda event: (
            self.enter_password_mode(self.input_password),
        )
        self.input_password.focusOutEvent = lambda event: (
            self.exit_password_mode(event, self.input_password),
        )

        self.btn_login = QtWidgets.QPushButton("Login", parent=self.login_section)
        self.btn_login.setFixedSize(150, 60)
        self.btn_login.move(
            self.width() // 2 - self.btn_login.width() // 2,
            self.input_password.y() + inputs_height + space_between_elements * 10,
        )
        self.btn_login.setStyleSheet(css.login_and_register_buttons)
        self.btn_login.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_login.highlighted = False
        self.btn_login.enterEvent = lambda event: self.emphasize_button(self.btn_login)
        self.btn_login.leaveEvent = lambda event: self.deemphasize_button(
            self.btn_login
        )

        self.btn_eye = QtWidgets.QPushButton(parent=self.login_section)
        self.btn_eye.setIcon(QtGui.QIcon(str(Path(__file__).parent / "icons/eye.png")))
        self.btn_eye.setIconSize(QtCore.QSize(40, 40))
        self.btn_eye.setFixedSize(40, 40)
        self.btn_eye.move(inputs_width, self.input_password.y() - 6)
        self.btn_eye.setCursor(QtGui.Qt.CursorShape.PointingHandCursor)
        self.btn_eye.setStyleSheet(css.eye_icon)
        self.btn_eye.pressed.connect(self.toggle_password_mode)
        self.btn_eye.released.connect(self.toggle_password_mode)

    def enter_password_mode(self, target_input: QtWidgets.QLineEdit):
        if target_input.echoMode() == QtWidgets.QLineEdit.EchoMode.Normal:
            target_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        target_input.setReadOnly(False)
        target_input.setFocus()

    def exit_password_mode(
        self, event, target_input: QtWidgets.QLineEdit, placeholder=""
    ):
        print("chamei")
        if isinstance(event, QtGui.QFocusEvent):
            if event.lostFocus():
                if target_input.text() == "" or target_input.text() == placeholder:
                    target_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
                    target_input.setText(placeholder)

                target_input.setReadOnly(True)

        elif isinstance(event, QtGui.QMouseEvent):
            if event.button().LeftButton:
                target_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
                target_input.setReadOnly(False)

    def toggle_password_mode(self):
        if self.input_password.echoMode() == QtWidgets.QLineEdit.EchoMode.Normal:
            self.input_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            self.input_password.setReadOnly(False)
            self.input_password.setFocus()
        else:
            self.input_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            self.input_password.setReadOnly(True)

    def emphasize_button(self, button: QtWidgets.QPushButton):
        if not button.highlighted:
            button.highlighted = True
            button.setStyleSheet(css.login_and_register_buttons_highlighted)

    def deemphasize_button(self, button: QtWidgets.QPushButton):
        if button.highlighted:
            button.highlighted = False
            button.setStyleSheet(css.login_and_register_buttons)

    def back_to_main_window(self):
        main_window: MainWindow = self.parent()
        main_window.login_or_register_window.show()
        self.hide()


class InformativePopUp(QtWidgets.QLabel):
    def __init__(
        self,
        parent: MainWindow,
        title: str = "No titles here",
        information: str = "No infomations here",
    ):
        super(InformativePopUp, self).__init__(parent=parent)
        self.setFixedSize(400, 200)
        self.move(
            parent.width() // 2 - self.width() // 2,
            parent.height() // 2 - self.height() // 2,
        )
        self.setStyleSheet(css.informative_popup)

        margin_right = 30
        margin_left = 30

        self.popup_header = QtWidgets.QLabel(title, parent=self)
        self.popup_header.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.popup_header.setFixedSize(self.width(), 40)
        self.popup_header.setStyleSheet(css.popup_header)
        self.popup_header.move(0, 0)

        self.btn_close_popup = QtWidgets.QPushButton("X", parent=self)
        self.btn_close_popup.setFixedSize(20, 20)
        self.btn_close_popup.move(
            self.width() - self.btn_close_popup.width() - 10,
            self.popup_header.height() // 2 - self.btn_close_popup.height() // 2 + 1,
        )
        self.btn_close_popup.clicked.connect(self.toggle_popup)
        self.btn_close_popup.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_close_popup.setStyleSheet(css.btn_close_popup)

        self.lbl_information = QtWidgets.QLabel(information, parent=self)
        self.lbl_information.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_information.setFixedWidth(380)
        self.lbl_information.move(
            self.width() // 2 - self.lbl_information.width() // 2,
            self.height() // 2 - self.lbl_information.height() // 2 + 15,
        )
        self.lbl_information.setStyleSheet(css.informative_popup_lbl)

        self.setVisible(False)

    def toggle_popup(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()


class LoginOrRegisterSideMenu(QtWidgets.QLabel):
    def __init__(self, parent: MainWindow):
        super(LoginOrRegisterSideMenu, self).__init__(parent=parent)
        self.setStyleSheet(css.registration_forms)

        user_screen = QtGui.QGuiApplication.primaryScreen()
        user_screen_geometry = user_screen.availableGeometry()
        self.setFixedSize(
            user_screen_geometry.width() * 2 / 5, user_screen_geometry.height()
        )

        self.move(0, 0)

        space_between_the_buttons = 10
        buttons_height = 60
        buttons_width = 120

        self.welcome_title = QtWidgets.QLabel("Seja bem-vindo", parent=self)
        self.welcome_title.setFixedWidth(len(self.welcome_title.text()) * 18)
        self.welcome_title.setStyleSheet(css.registration_title)
        self.welcome_title.move(
            self.width() // 2 - self.welcome_title.width() // 2,
            self.height() // 2 - buttons_height // 2 - self.welcome_title.height() - 60,
        )

        self.login_or_register_div = QtWidgets.QLabel(parent=self)
        self.login_or_register_div.setFixedSize(self.width(), buttons_height)
        self.login_or_register_div.move(
            0, self.height() // 2 - self.login_or_register_div.height() // 2
        )

        self.btn_login = QtWidgets.QPushButton(
            "Fazer login", parent=self.login_or_register_div
        )
        self.btn_login.setStyleSheet(css.login_and_register_buttons)
        self.btn_login.setFixedSize(buttons_width, buttons_height)
        self.btn_login.move(
            self.width() // 2 - buttons_width - space_between_the_buttons, 0
        )
        self.btn_login.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_login.highlighted = False
        self.btn_login.enterEvent = lambda event: self.emphasize_button(self.btn_login)
        self.btn_login.leaveEvent = lambda event: self.deemphasize_button(
            self.btn_login
        )
        self.btn_login.clicked.connect(self.open_driver_login_form)

        self.btn_register = QtWidgets.QPushButton(
            "Cadastrar-se", parent=self.login_or_register_div
        )
        self.btn_register.setStyleSheet(css.login_and_register_buttons)
        self.btn_register.setFixedSize(buttons_width, buttons_height)
        self.btn_register.move(self.width() // 2 + space_between_the_buttons, 0)
        self.btn_register.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_register.highlighted = False
        self.btn_register.enterEvent = lambda event: self.emphasize_button(
            self.btn_register
        )
        self.btn_register.leaveEvent = lambda event: self.deemphasize_button(
            self.btn_register
        )
        self.btn_register.clicked.connect(self.open_driver_registration_form)

    def emphasize_button(self, button: QtWidgets.QPushButton):
        if not button.highlighted:
            button.highlighted = True
            button.setStyleSheet(css.login_and_register_buttons_highlighted)

    def deemphasize_button(self, button: QtWidgets.QPushButton):
        if button.highlighted:
            button.highlighted = False
            button.setStyleSheet(css.login_and_register_buttons)

    def open_driver_registration_form(self):
        main_window = self.parent()
        main_window.driver_registration_form.show()
        self.hide()

    def open_driver_login_form(self):
        main_window = self.parent()
        main_window.driver_login_form.show()
        self.hide()


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    main_window = MainWindow()
    main_window.showMaximized()
    app.exec()
    psq.clear_table(connection=connection, table_name="drivers")
    connection.close()
