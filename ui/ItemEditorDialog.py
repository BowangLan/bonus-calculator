from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class ItemEditorDialog(QDialog):
    def __init__(self, parent=None, item_type: str = None, amount: float = None):
        super(QDialog, self).__init__(parent=parent)
        loadUi('./ui/ItemEditorDialog.ui', self)
        self.invalid_message.setVisible(False)
        self.okButton.clicked.connect(self.onOK)
        self.cancelButton.clicked.connect(self.onCancel)
        self.amount_value.textChanged.connect(self.onChange)
        self.amount_valid = False

        if item_type:
            self.type_value.setCurrentText(item_type)
        if amount:
            self.amount_value.setText("{:.2f}".format(amount))

    def onChange(self):
        try:
            current_text = self.amount_value.text()
            if current_text == '':
                raise Exception
            float(current_text)
            self.amount_valid = True
            self.invalid_message.setVisible(False)
        except Exception:
            self.amount_valid = False
            self.invalid_message.setVisible(True)

    def onOK(self):
        if self.amount_valid:
            self.accept()

    def onCancel(self):
        self.close()

    def get_item_value(self):
        return {
            'type': self.type_value.currentText(),
            'amount': float(self.amount_value.text())
        }
