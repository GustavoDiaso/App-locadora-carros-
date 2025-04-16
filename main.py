from PySide6 import QtWidgets, QtCore, QtGui
from CSS import css
from pathlib import Path
import sqlite3

# importing our modules
import database.prepared_sql_queries as psq
import login_and_registration_page_widgets as lrwidgets
import driver_and_vehicle_objects

DATABASE_PATH = Path(__file__).parent / "database/database.sqlite3"
# connecting to the sqlite3 database.
connection = sqlite3.connect(DATABASE_PATH)

psq.create_table_drivers(connection=connection)
psq.create_table_vehicles(connection=connection)


class MainWindow(QtWidgets.QWidget):
    """This class represents our main window, where all the widgets are gonna be displayed"""
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setStyleSheet(css.main_window)

        user_screen = QtGui.QGuiApplication.primaryScreen()
        user_screen_geometry = user_screen.availableGeometry()
        self.setMinimumSize(user_screen_geometry.width(), user_screen_geometry.height())

        # self.logged_in_user = None
        # Im gonna create this fake user just so I'll be able to configure the app without having to login every time.
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
        # self.login_and_registration_window.hide()

        self.informative_popup = InformativePopUp(parent=self)

class InformativePopUp(QtWidgets.QLabel):
    """This class represents the popup that appears in the screen every time we wanna show something"""
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




if __name__ == "__main__":
    app = QtWidgets.QApplication()
    main_window = MainWindow()
    main_window.showMaximized()
    app.exec()
    # psq.clear_table(connection=connection, table_name="drivers")
    connection.close()
