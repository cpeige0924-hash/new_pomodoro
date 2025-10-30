# ui/pet_setup.py
# 创建新宠物的对话框：输入名字、选择种类
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from core.pet import Pet
from core.pet_manager import save_growing

class PetSetupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create Your Pet")
        self.resize(300, 180)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter pet name")

        self.species = None

        btn_cat = QPushButton("Cat")
        btn_rab = QPushButton("Rabbit")
        btn_dog = QPushButton("Dog")
        btn_duck = QPushButton("Duck")
        for b in (btn_cat, btn_rab, btn_dog, btn_duck):
            b.setCheckable(True)
            b.clicked.connect(self._on_species_clicked)

        h = QHBoxLayout()
        h.addWidget(btn_cat)
        h.addWidget(btn_rab)
        h.addWidget(btn_dog)
        h.addWidget(btn_duck)

        create_btn = QPushButton("Confirm")
        create_btn.clicked.connect(self._confirm)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Pet Name:"))
        layout.addWidget(self.name_edit)
        layout.addWidget(QLabel("Choose Species:"))
        layout.addLayout(h)
        layout.addWidget(create_btn)

        self._species_buttons = (btn_cat, btn_rab, btn_dog, btn_duck)

    def _on_species_clicked(self):
        sender = self.sender()
        # 单选：取消其他按钮
        for b in self._species_buttons:
            if b is not sender:
                b.setChecked(False)
        # 记录种类
        text = sender.text().lower()
        self.species = "rabbit" if "rabbit" in text else text

    def _confirm(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Invalid", "Please enter a pet name.")
            return
        if not self.species:
            QMessageBox.warning(self, "Invalid", "Please choose a species.")
            return

        pet = Pet(name=name, species=self.species, growth_value=0.0, stage=1)
        save_growing(pet)
        self.accept()
