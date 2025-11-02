# ---------------------------------------------------------
# 花园窗口：展示所有成熟宠物（柔光金杏风格）
# ---------------------------------------------------------
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea
from PyQt5.QtCore import Qt
from core.pet_manager import load_garden
from core.ascii_art import get_ascii

class GardenPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌸 My Lovely Garden 🌸")
        self.resize(520, 640)
        self.setStyleSheet("background-color: #fdfaf6;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        header = QLabel("🌿 Your Garden Friends 🌿")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size:18px; font-weight:bold; color:#4a3f35; margin:10px 0;")
        layout.addWidget(header)

        pets = load_garden()
        if not pets:
            msg = QLabel("🌱 Your garden is still empty.")
            msg.setAlignment(Qt.AlignCenter)
            msg.setStyleSheet("font-size:16px; color:#6b6057; margin-top:20px;")
            layout.addWidget(msg)
        else:
            for pet in pets:
                name = pet.get("name", "Unknown")
                species = pet.get("species", "Unknown")
                stage = pet.get("stage", 3)

                card = QWidget()
                card.setStyleSheet("""
                    background-color: rgba(255, 255, 255, 0.85);
                    border: 1px solid #e4d3b4;
                    border-radius: 12px;
                    padding: 10px;
                    margin: 8px 16px;
                """)
                vbox = QVBoxLayout(card)

                title = QLabel(f"🌾 {name} the {species.capitalize()}")
                title.setAlignment(Qt.AlignCenter)
                title.setStyleSheet("font-size:14px; font-weight:bold; color:#4a3f35;")

                ascii_art = QLabel(get_ascii(species, stage))
                ascii_art.setAlignment(Qt.AlignCenter)
                ascii_art.setStyleSheet("font-family:'Courier New'; font-size:12px; color:#3a2f2f;")

                vbox.addWidget(title)
                vbox.addWidget(ascii_art)
                layout.addWidget(card)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        container.setLayout(layout)
        scroll.setWidget(container)
        scroll.setFrameShape(QScrollArea.NoFrame)

        root = QVBoxLayout()
        root.addWidget(scroll)
        self.setLayout(root)



