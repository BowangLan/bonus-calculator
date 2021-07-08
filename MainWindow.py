from PyQt5.QtWidgets import QMainWindow, QMenu, QTableWidgetItem, QInputDialog, QHeaderView, QFileDialog
from PyQt5.QtCore import QFile, Qt
from PyQt5.QtGui import QColor
from PyQt5.uic import loadUi
from ui.ItemEditorDialog import ItemEditorDialog
from ui.SettingsEditorDialog import SettingsEditorDialog
from DataManager import JSONDataManager, SettingsManager
from BonusCalculator import BonusCalculator
from time import perf_counter


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        loadUi('ui/MainUI.ui', self)
        self.setWindowTitle("Bonus Calculator")

        self.settings_manager = SettingsManager()  # auto load
        self.cache_manager = JSONDataManager(
            data_path=self.settings['basic']['cache_path'], default_value={'recent_opens': []})
        self.calculator = BonusCalculator(
            bonus_rules=self.settings['data']['bonus_rules'])

        # menu
        self.action_open_settings.triggered.connect(self.open_settings_editor)
        self.actionNew.triggered.connect(self.create_new)
        self.actionOpen.triggered.connect(self.open)
        self.actionSave.triggered.connect(self.save)

        # target income label & button
        self.target_income_edit_button.clicked.connect(self.edit_target_income)

        # table
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openRightClickMenu)
        # self.tableWidget.itemChanged.connect(self.handleItemChange)
        self.tableWidget.itemDoubleClicked.connect(
            self.handleItemDoubleClicked)
        self.renderingData = False

        # button clicked
        self.add_button.clicked.connect(self.add_item)
        self.save_button.clicked.connect(self.save)
        self.refresh_button.clicked.connect(self.load_data)

        if self.settings['basic']['autoopen_data_path']:
            self.open_data_file(self.settings['basic']['autoopen_data_path'])

        self.target_income_value.setText("{:.2f}".format(self.target_income))

    @property
    def autosave(self):
        return self.settings_manager.settings['basic']['autosave']

    @property
    def target_income(self):
        return self.settings_manager.settings['data']['target_income']

    @target_income.setter
    def target_income(self, value: float):
        """When settting a target income, the new value is automatically saved."""
        self.settings_manager.settings['data']['target_income'] = value
        self.target_income_value.setText("{:.2f}".format(value))
        self.setCalculationResult()
        self.settings_manager.save_data()

    @property
    def settings(self):
        return self.settings_manager.settings

    @property
    def cache(self):
        return self.cache_manager.data

    def edit_target_income(self):
        """Edit the target income by popping user input dialog.
        """
        result, done = QInputDialog.getDouble(
            self, "New Target Income", "Enter a new target income: ", value=self.target_income)
        if not done:
            return
        try:
            print("New target income: " + str(result))
            self.target_income = result
        except:
            self.show_warning("Invalid target income!")

    def open_settings_editor(self):
        """Open settings editor window."""
        editor = SettingsEditorDialog(settings_manager=self.settings_manager)
        editor.exec_()

    def open_data_file(self, filepath):
        self.data_manager = JSONDataManager(data_path=filepath)
        if filepath in self.cache['recent_opens']:
            self.cache['recent_opens'].remove(filepath)
        self.cache['recent_opens'].insert(0, filepath)
        self.load_data()

    def open(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileNames()", "", "JSON Files (*.json)", options=options)
        if file:
            self.open_data_file(file)

    def create_new(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getSaveFileName(
            self, "QFileDialog.getSaveFileName()", "", "JSON Files (*.json)", options=options)
        if files:
            self.open_data_file(files)

    def save(self, show_message=True):
        self.data_manager.save_data()
        if show_message:
            self.show_message("{} items saved".format(
                len(self.data_manager.data)))

    def show_message(self, msg):
        self.statusBar().setStyleSheet("")
        self.statusBar().showMessage(msg)

    def show_warning(self, msg):
        self.statusBar().setStyleSheet("color: red;")
        self.statusBar().showMessage(msg)

    def handleItemChange(self, item):
        """
        Handle an item's value after it's been changed.
        Not being used. Replaced by `handleItemDoubleClicked`
        """
        if self.renderingData:
            return
        if item.column() == 0:
            item.setText(self.data_manager.data[item.row()]['type'])
            self.show_warning("You can't change item type!")
        else:
            try:
                amount = float(item.text())
                self.data_manager.data[item.row()]['amount'] = amount
                self.setCalculationResult()
                if self.autosave:
                    self.data_manager.data_save()
                self.show_message("Item {} modified".format(item.row() + 1))

            except Exception:
                item.setText("{:.2f}".format(
                    self.data_manager.data[item.row()]['amount']))
                self.show_warning("Invalid amount value!")
        print('Cell changed: {} {}'.format(item.row(), item.column()))

    def handleItemDoubleClicked(self, item):
        """Modify an item row's value by opening a new window.
        """
        row = item.row()
        item_type = self.data_manager.data[row]['type']
        amount = self.data_manager.data[row]['amount']
        edit_dialog = ItemEditorDialog(item_type=item_type, amount=amount)
        if edit_dialog.exec_():
            self.data_manager.data[row] = edit_dialog.get_item_value()
            self.set_table()
            self.setCalculationResult()
            self.show_message("1 Item modified")
            if self.autosave:
                self.save()

    def load_data(self):
        """Load the data from local data file into the data manager, and
        into then into the table."""
        self.data_manager.load_data()
        self.set_table()
        self.setCalculationResult()

    def set_table(self):
        """Set table data from the data manager."""
        self.renderingData = True
        self.show_message("Setting table...")
        tic = perf_counter()
        data = self.data_manager.data
        self.tableWidget.setRowCount(len(data))
        for r, line in enumerate(data):
            color = self.settings_manager.settings['style']['{}_color'.format(
                line['type'])]
            color = QColor(color)
            item1 = QTableWidgetItem(line['type'])
            item1.item_type = line['type']
            item1.setBackground(color)
            self.tableWidget.setItem(r, 0, item1)
            item2 = QTableWidgetItem('{:.2f}'.format(line['amount']))
            item2.setBackground(color)
            self.tableWidget.setItem(r, 1, item2)
        toc = perf_counter() - tic
        self.show_message("{} item(s) loaded in {:.4f} seconds".format(
            len(self.data_manager.data), toc))
        self.renderingData = False

    def add_item(self):
        add_dialog = ItemEditorDialog()
        if not add_dialog.exec_():
            return
        new_item = add_dialog.get_item_value()
        # item_type, status = QInputDialog.getItem(
        #     self, 'New Item', 'Enter an item type', ['order', 'income'], editable=False)
        # if not status:
        #     return
        # amount, status = QInputDialog.getDouble(
        #     self, 'New Item', 'Enter the amount')
        # if not status:
        #     return
        # new_item = {"type": item_type, "amount": amount}
        print("New item: ", str(new_item))
        self.data_manager.data.append(new_item)
        self.set_table()
        self.setCalculationResult()
        if self.autosave:
            self.save()

    def delete_rows(self):
        indeces = self.tableWidget.selectionModel().selectedRows()
        for i in indeces:
            self.data_manager.data.pop(i.row())
            self.tableWidget.removeRow(i.row())
        self.setCalculationResult()
        if self.autosave:
            self.save()
        self.show_message("{} items deleted".format(len(indeces)))

    def openRightClickMenu(self, pos):
        menu = QMenu()
        delete_action = menu.addAction('Delete Selected Row(s)')
        delete_action.triggered.connect(lambda _: self.delete_rows())
        menu.exec_(self.mapToGlobal(pos))

    def setCalculationResult(self):
        total_income,  \
            actual_income, \
            total_bonus,   \
            actual_bonus = self.calculator.calculate(
                self.data_manager.data,
                self.target_income)
        self.current_bonus_value.setText('{:.2f}'.format(actual_bonus))
        self.total_income_value.setText('{:.2f}'.format(total_income))
        self.actual_income_value.setText('{:.2f}'.format(actual_income))
