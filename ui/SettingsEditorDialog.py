from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class SettingsEditorDialog(QDialog):
    def __init__(self, parent=None, settings_manager=None):
        self.settings_manager = settings_manager
        super().__init__(parent=None)
        loadUi('./ui/SettingsEditorDialog.ui', self)

        self.message_label.setVisible(False)

        self.autosave_value.setChecked(
            self.settings_manager.settings['basic']['autosave'])
        self.cache_path_value.setText(
            self.settings_manager.settings['basic']['cache_path'])
        self.autoopen_data_path_value.setText(
            self.settings_manager.settings['basic']['autoopen_data_path'])

        self.order_color.setText(
            self.settings_manager.settings['style']['order_color'])
        self.income_color.setText(
            self.settings_manager.settings['style']['income_color'])

        self.save_button.clicked.connect(self.save)
        self.cancel_button.clicked.connect(self.on_close)

    def save(self):
        self.settings_manager.settings.update({
            'basic': {
                'cache_path': self.cache_path_value.text(),
                'autoopen_data_path': self.autoopen_data_path_value.text(),
                'autosave': self.autosave_value.isChecked(),
            },
            'style': {
                'order_color': self.order_color.text(),
                'income_color': self.income_color.text()
            }
        })
        self.settings_manager.save_data()
        self.message_label.setStyleSheet('color: green;')
        self.message_label.setText("Settings saved succussfully")
        self.message_label.setVisible(True)

    def on_close(self):
        self.close()
