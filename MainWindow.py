from PyQt5.QtWidgets import QMainWindow, QMenu, QTableWidgetItem, QInputDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.uic import loadUi
from ItemEditorDialog import ItemEditorDialog
from SettingsEditorDialog import SettingsEditorDialog
from SettingsManager import SettingsManager
from DataManager import JSONDataManager
from BonusCalculator import BonusCalculator
from time import perf_counter


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        loadUi('MainUI.ui', self)
        self.setWindowTitle("Bonus Calculator")

        self.settings_manager = SettingsManager()
        self.settings_manager.load()
        self.settings = self.settings_manager.settings
        self.data_manager = JSONDataManager(
            data_path=self.settings_manager.settings['basic']['data_path'])
        self.data_manager.load_data()
        self.calculator = BonusCalculator(
            bonus_rules=None,
            target_income=self.settings_manager.settings['data']['target_income'])

        self.action_open_settings.triggered.connect(self.open_settings_editor)

        # target income
        self.target_income_value.setText("{:.2f}".format(self.target_income))
        self.target_income_edit_button.clicked.connect(self.edit_target_income)

        # table
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openRightClickMenu)
        # self.tableWidget.itemChanged.connect(self.handleItemChange)
        self.tableWidget.itemDoubleClicked.connect(
            self.handleItemDoubleClicked)
        self.renderingData = False

        # button clicked
        self.add_button.clicked.connect(self.add_item)
        self.save_button.clicked.connect(self.save)
        self.refresh_button.clicked.connect(self.set_table)

        # load data and calculation
        self.set_table()
        self.setCalculationResult()

    @property
    def autosave(self):
        return self.settings_manager.settings['basic']['autosave']

    @property
    def target_income(self):
        return self.settings_manager.settings['data']['target_income']

    @target_income.setter
    def target_income(self, value: float):
        self.settings_manager.settings['data']['target_income'] = value
        self.target_income_value.setText("{:.2f}".format(value))
        self.calculator.target_income = value
        self.setCalculationResult()
        self.settings_manager.save()

    def edit_target_income(self):
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
        editor = SettingsEditorDialog(settings_manager=self.settings_manager)
        editor.exec_()

    def save(self):
        self.data_manager.save_data()
        self.show_message("{} items saved".format(len(self.data_manager.data)))

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
        row = item.row()
        item_type = self.data_manager.data[row]['type']
        amount = self.data_manager.data[row]['amount']
        edit_dialog = ItemEditorDialog(item_type=item_type, amount=amount)
        if edit_dialog.exec_():
            self.data_manager.data[row] = edit_dialog.get_item_value()
            self.set_table()
            self.setCalculationResult()
            self.show_message("1 Item modified")

    def set_autosave(self, _):
        self.autosave = self.autosave_button.isChecked()
        print(self.autosave)
        self.save()

    def set_table(self):
        self.renderingData = True
        self.show_message("Loading data...")
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
        # add_dialog = ItemEditorDialog()
        # if add_dialog.exec_():
        #     new_item = add_dialog.get_item_value()
        item_type, status = QInputDialog.getItem(
            self, 'New Item', 'Enter an item type', ['order', 'income'])
        if not status:
            return
        amount, status = QInputDialog.getDouble(
            self, 'New Item', 'Enter the amount')
        if not status:
            return
        new_item = {"type": item_type, "amount": amount}
        print("New item: ", str(new_item))
        self.data_manager.data.append(new_item)
        self.set_table()
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
        self.calculator.parse_data(data=self.data_manager.data)
        total_income, actual_income, total_bonus, actual_bonus = self.calculator.calculate()
        self.current_bonus_value.setText('{:.2f}'.format(actual_bonus))
        self.total_income_value.setText('{:.2f}'.format(total_income))
        self.actual_income_value.setText('{:.2f}'.format(actual_income))
