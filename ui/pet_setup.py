# ----------------------------
# Create-a-Pet dialog with soft UI styling.
# ----------------------------

from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout
)
from core.ui_utils import show_pretty_message  # 用于柔光弹窗

class PetSetupDialog(QDialog):
    """宠物创建界面：输入名字 + 选择种类"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create Your Pet")
        self.setFixedSize(450, 260)
        self.species = None

        # --- Widgets ---
        self.name_label = QLabel("Pet Name:")
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter pet name")

        self.species_label = QLabel("Choose Species:")

        # 四种动物按钮
        self.btn_cat = QPushButton("Cat")
        self.btn_rabbit = QPushButton("Rabbit")
        self.btn_dog = QPushButton("Dog")
        self.btn_duck = QPushButton("Duck")

        self.btn_confirm = QPushButton("Confirm")

        # --- Layout ---
        species_layout = QHBoxLayout()
        for btn in [self.btn_cat, self.btn_rabbit, self.btn_dog, self.btn_duck]:
            species_layout.addWidget(btn)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(self.species_label)
        layout.addLayout(species_layout)
        layout.addWidget(self.btn_confirm)
        self.setLayout(layout)

        # --- Button logic ---
        self.btn_cat.clicked.connect(lambda: self._select_species("Cat"))
        self.btn_rabbit.clicked.connect(lambda: self._select_species("Rabbit"))
        self.btn_dog.clicked.connect(lambda: self._select_species("Dog"))
        self.btn_duck.clicked.connect(lambda: self._select_species("Duck"))
        self.btn_confirm.clicked.connect(self._confirm)

        # --- Styling ---
        self.setStyleSheet("""
            QDialog {
                background-color: #fffaf3;
                border: 1px solid #e4d3b4;
                border-radius: 12px;
            }
            QLabel {
                color: #3a2f2f;
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #fffdf8;
                border: 1px solid #d9c7a5;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #f7e7c2;
                border: 1px solid #e2cfa3;
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 14px;
                font-weight: bold;
                color: #3a2f2f;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #f3d9a8;
            }
            QPushButton:pressed {
                background-color: #eacb8d;
            }
            QPushButton:focus {
                outline: none;
                border: 2px solid #d1b06b;
            }
        """)

    # --- Internal methods ---
    def _select_species(self, name):
        """选中某种动物时高亮按钮"""
        self.species = name
        for btn in [self.btn_cat, self.btn_rabbit, self.btn_dog, self.btn_duck]:
            btn.setStyleSheet("background-color: #f7e7c2; border: 1px solid #e2cfa3; border-radius: 8px;")
        self.sender().setStyleSheet("background-color: #f3d9a8; border: 2px solid #d1b06b; border-radius: 8px;")

    def _confirm(self):
        """确认宠物信息"""
        name = self.name_edit.text().strip()
        if not name:
            show_pretty_message("Invalid", "Please enter a pet name.")
            return
        if not self.species:
            show_pretty_message("Invalid", "Please choose a species.")
            return
        self.accept()

    def get_data(self):
        """返回宠物信息"""
        return self.name_edit.text().strip(), self.species

