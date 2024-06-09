import sys
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from BaseData import BaseData
from UI import MainWindow, Dialog

class Controller(QObject):
    def __init__(self) -> None:
        super().__init__()
        self.base = BaseData()
        self.list_name_table = self.base.getListNamesTables()
        self.list_base = self.base.getListTable()
        #self.list_names_columns = self.base.getListColumns(self.list_name_table[self.num_table])
        self.num_table = 0

        self.main_window = MainWindow()
        self.add_dialog = Dialog(self.main_window, "Изменение Данных", "Сохранить")
        self.edit_dialog = Dialog(self.main_window, "Редактировать данные", "Редактировать")
 
        self.main_window.add_button.clicked.connect(self.open_add_dialog)
        self.main_window.edit_button.clicked.connect(self.open_edit_dialog)
        self.main_window.delete_button.clicked.connect(self.delete_row)
        self.main_window.combo_box.currentIndexChanged.connect(self.on_combobox_changed)

        self.add_dialog.button.clicked.connect(self.save_data)
        self.edit_dialog.button.clicked.connect(self.edit_data)
        
        self.main_window.setting_dorp_down_list(self.list_name_table)
        self.refresh_data()
        self.main_window.show()

    def refresh_data(self):

        data = self.base.getData(self.list_name_table[self.num_table])
        data.sort(key=lambda x : x[0])
        count_col, count_row = 0, 0
        if not len(data) == 0:
            count_col, count_row = len(data), len(data[0])

        model = QStandardItemModel(count_col, count_row)
        for row_num, row in enumerate(data):
            for col_num, value in enumerate(row):
                item = QStandardItem(str(value))
                model.setItem(row_num, col_num, item)
                model.setHorizontalHeaderLabels(self.base.getListColumns(self.list_name_table[self.num_table]))
        self.main_window.table_view.setModel(model)

    def open_add_dialog(self):
        list_names_columns = self.base.getListColumns(self.list_name_table[self.num_table])
        self.add_dialog.settint_to_layaout(list_names_columns)
        self.add_dialog.show()
    
    def open_edit_dialog(self):
        list_names_columns = self.base.getListColumns(self.list_name_table[self.num_table])
        self.edit_dialog.settint_to_layaout(list_names_columns)
        self.edit_dialog.show()
    
    def delete_row(self):
        selected_row = self.main_window.table_view.selectionModel().currentIndex().row()
        if selected_row >= 0:
            data = self.main_window.table_view.model().data(self.main_window.table_view.model().index(selected_row, 0))
            self.base.deleteData(data)
            self.refresh_data()
    
    def on_combobox_changed(self):
        self.num_table = self.main_window.combo_box.currentIndex()
        self.refresh_data()
    
    def save_data(self):
        values = []
        for child in self.add_dialog.children():
            if isinstance(child, QLineEdit):
                values.append(child.text())

        name_table = self.list_name_table[self.num_table]
        list_names_columns = self.base.getListColumns(name_table)
        self.base.dowonloadData(name_table, list_names_columns, values)

        self.refresh_data()
        self.add_dialog.close()
    
    def edit_data(self):
        values = []
        for child in self.edit_dialog.children():
            if isinstance(child, QLineEdit):
                values.append(child.text())

        name_table = self.list_name_table[self.num_table]
        list_names_columns = self.base.getListColumns(name_table)
        self.delete_row()
        self.base.dowonloadData(name_table, list_names_columns, values)
        self.refresh_data()
        self.edit_dialog.close()


    
