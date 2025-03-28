from PySide6 import  QtWidgets, QtCore, QtGui
from CSS import css
from pathlib import  Path
import sqlite3
import  database.prepared_sql_queries as psq
from database.prepared_sql_queries import register_new_driver

DATABASE_PATH = Path(__file__).parent / 'database/database.sqlite3'
connection = sqlite3.connect(DATABASE_PATH)

psq.create_table_drivers(connection=connection)
psq.create_table_vehicles(connection=connection)

class Main_Window(QtWidgets.QWidget):
    def __init__(self):
        super(Main_Window, self).__init__()
        self.setStyleSheet(css.main_window)

        user_screen = QtGui.QGuiApplication.primaryScreen()
        user_screen_geometry = user_screen.availableGeometry()
        self.setMinimumSize(user_screen_geometry.width(), user_screen_geometry.height())


register_new_driver(connection=connection, psq.Driver())

connection.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication()
    main_window = Main_Window()
    main_window.showMaximized()
    app.exec()


