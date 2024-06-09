import sys
import psycopg2
from PyQt5.QtWidgets import QMainWindow, QTableView, QPushButton, QDialog, QFormLayout, QLineEdit, QLabel, QComboBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Пример приложения PostgreSQL")
        self.resize(1500, 600)

        self.table_view = QTableView(self)
        self.table_view.setGeometry(10, 10, 1000, 300)

        self.add_button = QPushButton("Добавить", self)
        self.add_button.setGeometry(1050, 60, 200, 30)

        self.edit_button = QPushButton("Изменить", self)
        self.edit_button.setGeometry(1050, 110, 200, 30)

        self.delete_button = QPushButton("Удалить", self)
        self.delete_button.setGeometry(1050, 160, 200, 30)

        self.combo_box = QComboBox(self)
        self.combo_box.setGeometry(1050, 10, 200, 30)

    def setting_dorp_down_list(self, names_columns):
        self.combo_box.addItems([', '.join(map(str, name)) for name in names_columns])

class Dialog(QDialog):
    def __init__(self, parent, name_window, name_button):
        super().__init__(parent)

        self.setWindowTitle(name_window)
        self.resize(300, 200)

        self.layout = QFormLayout(self)

        self.button = QPushButton(name_button, self)
        self.layout.addRow(self.button)

        self.dynamic_widgets = []
    
    def clear_layout(self):
        for widget in self.dynamic_widgets:
            widget.deleteLater()
        self.dynamic_widgets.clear()
    
    def settint_to_layaout(self, list_names):
        self.clear_layout()
        for name in list_names:
            label = QLabel((name), self)
            input_field = QLineEdit(self)
            self.layout.addRow(label, input_field)
            self.dynamic_widgets.extend([label, input_field])

class ErrorDilog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)