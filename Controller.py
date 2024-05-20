import sys
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QPushButton, QDialog, QFormLayout, QLineEdit, QLabel, QDateEdit
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from BaseData import BaseData
from UI import MainWindow, AddDialog, EditDialog
class Controller(QObject):
    def __init__(self) -> None:
        super().__init__()
        self.base = BaseData()
        list_base = self.base.getListTable()
        self.num_table = 0
        self.list_names_columns = self.base.getListColumns(list_base[self.num_table])

        self.main_window = MainWindow()
        self.add_dialog = AddDialog()
        self.edit_dialog = EditDialog(self.main_window)

        self.main_window.setting_dorp_down_list(self.list_names_columns)
        self.add_dialog.settint_to_layaout(self.list_names_columns)
 
        self.main_window.add_button.clicked.connect(self.open_add_dialog)
        self.main_window.edit_button.clicked.connect(self.open_edit_dialog)
        self.main_window.delete_button.clicked.connect(self.delete_row)
        self.main_window.combo_box.currentIndexChanged.connect(self.on_combobox_changed)

        self.add_dialog.save_button.clicked.connect(self.save_data)

        self.refresh_data(list_base[0])
        self.main_window.show()

    def refresh_data(self, base_data):
        data = base_data
        data.sort(key=lambda x : x[0])

        model = QStandardItemModel(len(data), len(data[0]))
        for row_num, row in enumerate(data):
            for col_num, value in enumerate(row):
                item = QStandardItem(str(value))
                model.setItem(row_num, col_num, item)
        self.main_window.table_view.setModel(model)

    def open_add_dialog(self):
        self.add_dialog.show()
    
    def open_edit_dialog(self):
        selected_row = self.main_window.table_view.selectionModel().currentIndex().row()
        if selected_row >= 0:
            data = self.main_window.table_view.model().data(self.main_window.table_view.model().index(selected_row, 0))
            self.edit_dialog.show()
    
    def delete_row(self):
        selected_row = self.main_window.table_view.selectionModel().currentIndex().row()
        if selected_row >= 0:
            data = self.main_window.table_view.model().data(self.main_window.table_view.model().index(selected_row, 0))
            self.base.deleteData(data)
            self.edit_dialog.show()
            self.refresh_data()
    
    def on_combobox_changed(self):
        self.num_table = self.main_window.combo_box.currentIndex()
    
    def save_data(self):
        values = []
        for child in self.children():
            if isinstance(child, QLineEdit):
                values.append(child.text())
        
        self.base.dowonloadData(self.list_names_columns, values)

        self.refresh_data()
        self.add_dialog.close()


    
