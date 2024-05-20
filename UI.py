import sys
import psycopg2
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QPushButton, QDialog, QFormLayout, QLineEdit, QLabel, QDateEdit
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Настройка главного окна
        self.setWindowTitle("Пример приложения PostgreSQL")
        self.resize(600, 400)

        # Создание табличного представления для отображения данных
        self.table_view = QTableView(self)
        self.table_view.setGeometry(10, 10, 580, 300)

        # Создание кнопок для выполнения операций
        self.add_button = QPushButton("Добавить", self)
        self.add_button.setGeometry(10, 320, 100, 30)
        self.add_button.clicked.connect(self.open_add_dialog)

        self.edit_button = QPushButton("Изменить", self)
        self.edit_button.setGeometry(120, 320, 100, 30)
        self.edit_button.clicked.connect(self.open_edit_dialog)

        self.delete_button = QPushButton("Удалить", self)
        self.delete_button.setGeometry(230, 320, 100, 30)
        self.delete_button.clicked.connect(self.delete_row)

        # Загрузка данных из базы данных при запуске приложения
        self.refresh_data()

    def refresh_data(self):
        conn = psycopg2.connect(dbname="kursach", user="postgres", host="localhost", password="SAO123_")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM admin")
        data = cursor.fetchall()
        data.sort(key=lambda x : x[0])

        model = QStandardItemModel(len(data), len(data[0]))
        for row_num, row in enumerate(data):
            for col_num, value in enumerate(row):
                item = QStandardItem(str(value))
                model.setItem(row_num, col_num, item)
        self.table_view.setModel(model)

    def open_add_dialog(self):
        self.add_dialog = AddDialog(self)
        self.add_dialog.show()

    def open_edit_dialog(self):
        selected_row = self.table_view.selectionModel().currentIndex().row()
        if selected_row >= 0:
            data = self.table_view.model().data(self.table_view.model().index(selected_row, 0))
            self.edit_dialog = EditDialog(self, data)
            self.edit_dialog.show()

    def delete_row(self):
        selected_row = self.table_view.selectionModel().currentIndex().row()
        if selected_row >= 0:
            data = self.table_view.model().data(self.table_view.model().index(selected_row, 0))
            conn = psycopg2.connect(dbname="kursach", user="postgres", host="localhost", password="SAO123_")
            cursor = conn.cursor()

            delete_query = "DELETE FROM admin WHERE adminid = %s"
            cursor.execute(delete_query, (data))

            conn.commit()
            conn.close()

            self.refresh_data()

class AddDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Добавить запись")
        self.resize(300, 200)

        conn = psycopg2.connect(dbname="kursach", user="postgres", host="localhost", password="SAO123_")
        cursor = conn.cursor()
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'admin'")
        column_names = [row[0] for row in cursor.fetchall()]
        conn.close()

        layout = QFormLayout(self)
        for column_name in column_names:
            label = QLabel(column_name, self)
            input_field = QLineEdit(self)
            layout.addRow(label, input_field)

        save_button = QPushButton("Сохранить", self)
        save_button.clicked.connect(self.save_data)

        layout.addRow(save_button)
        
        layout = QFormLayout(self)

        

    def save_data(self):
        values = []
        for child in self.children():
            if isinstance(child, QLineEdit):
                values.append(child.text())

        conn = psycopg2.connect(dbname="kursach", user="postgres", host="localhost", password="SAO123_")
        cursor = conn.cursor()
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'admin'")
        column_names = [row[0] for row in cursor.fetchall()]
        
        insert_query = "INSERT INTO admin (" + ", ".join(column_names) + ") VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, values)

        conn.commit()
        conn.close()

        self.parent().refresh_data()

        self.close()



class EditDialog(QDialog):
    def __init__(self, parent, data):
        super().__init__(parent)

        # Настройка формы редактирования записи
        self.setWindowTitle("Изменить запись")
        self.resize(300, 200)

        # Заполнение полей ввода значениями из текущей записи
        self.data = data  # Сохраните исходные данные для сравнения
        conn = psycopg2.connect(dbname="kursach", user="postgres", host="localhost", password="SAO123_")
        cursor = conn.cursor()
        cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'admin'")
        column_info = cursor.fetchall()
        conn.close()

        layout = QFormLayout(self)
        for column_name, data_type in column_info:
            label = QLabel(column_name, self)
            input_field = QLineEdit(self)
            #input_field.setText(str(self.data[column_name]))  # Заполните значениями из 'data'
            layout.addRow(label, input_field)

        # Создание кнопки для сохранения изменений
        save_button = QPushButton("Сохранить", self)
        save_button.clicked.connect(self.save_data)

        # Размещение элементов на форме
     
        layout.addRow(save_button)
        layout = QFormLayout(self)

    def save_data(self):
        updated_values = []
        for child in self.children():
            if isinstance(child, QLineEdit):
                updated_values.append(child.text())  # Измените тип преобразования в соответствии с типом данных
        print(updated_values)

        # Подключение к базе данных
        conn = psycopg2.connect(dbname="kursach", user="postgres", host="localhost", password="SAO123_")
        cursor = conn.cursor()
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'admin'")
        column_names = [row[0] for row in cursor.fetchall()]



        # Формирование SQL-запроса для обновления записи
        delete_query = "DELETE FROM admin WHERE adminid = %s"
        cursor.execute(delete_query, updated_values[0])
        insert_query = "INSERT INTO admin (" + ", ".join(column_names) + ") VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, updated_values)

        # Подтверждение изменений в базе данных
        conn.commit()
        conn.close()

        # Обновление табличного представления в главном окне
        self.parent().refresh_data()

        # Закрытие формы
        self.close()
