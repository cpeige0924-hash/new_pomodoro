# ui/garden_page.py
# ---------------------------------------------------------
# Garden window: show all fully grown pets
# ---------------------------------------------------------
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea
from PyQt5.QtCore import Qt
from core.pet_manager import load_garden
from core.ascii_art import get_ascii

class GardenPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Your Garden 🌸")
        self.setStyleSheet("background-color: #faf7f2;")
        self.resize(500, 600)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        pets = load_garden()
        if not pets:
            msg = QLabel("🌱 Your garden is still empty.")
            msg.setAlignment(Qt.AlignCenter)
            msg.setStyleSheet("font-size: 16px; color: #6b6057;")
            layout.addWidget(msg)
        else:
            for pet in pets:
                name = pet.get("name", "Unknown")
                species = pet.get("species", "Unknown")
                stage = pet.get("stage", 3)

                name_label = QLabel(f"🌾 {name} the {species.capitalize()}")
                name_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #4a3f35;")
                name_label.setAlignment(Qt.AlignCenter)

                ascii_label = QLabel(get_ascii(species, stage))
                ascii_label.setAlignment(Qt.AlignCenter)
                ascii_label.setStyleSheet("font-family: 'Courier New'; font-size: 12px; color: #3a2f2f;")

                layout.addWidget(name_label)
                layout.addWidget(ascii_label)
                layout.addSpacing(10)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        container.setLayout(layout)
        scroll.setWidget(container)

        root = QVBoxLayout()
        root.addWidget(scroll)
        self.setLayout(root)



