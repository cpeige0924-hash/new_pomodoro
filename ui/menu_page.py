# ui/menu_page.py
# ----------------------------
# 主菜单界面（柔光金杏风格）
# ----------------------------
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from core.state_manager import get_history
from core.pet_manager import load_growing
from datetime import date
from ui.garden_page import GardenPage

class MenuPage(QWidget):
    def __init__(self, start_callback):
        super().__init__()
        self.start_callback = start_callback
        self.selected_minutes = 25

        # --- 样式主题 ---
        self.setStyleSheet("""
            QWidget {
                background-color: #fffaf3;
            }
            QLabel {
                color: #3a2f2f;
            }
            QPushButton {
                background-color: #f7e7c2;
                color: #3a2f2f;
                border-radius: 10px;
                font-weight: bold;
                font-size: 14px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #f3d9a8;
            }
        """)

        # --- 标题 ---
        title = QLabel("🍅 Pomodoro Garden")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #2d2a26;")

        # --- 今日专注时长 ---
        self.stats = QLabel("")
        self.stats.setStyleSheet("font-size: 13px; color: #5c4b3b;")

        # --- 宠物状态（右下角） ---
        self.pet_label = QLabel("")
        self.pet_label.setStyleSheet("font-size: 12px; color: #6b6057; text-align: right;")

        # --- 模式选择 ---
        label = QLabel("Select your session length:")
        label.setStyleSheet("font-size: 14px;")

        self.btn_25 = QPushButton("25 min")
        self.btn_50 = QPushButton("50 min")
        self.btn_start = QPushButton("Start")
        self.btn_garden = QPushButton("🌸 Garden")
        self.btn_history = QPushButton("📅 View History")

        for b in [self.btn_25, self.btn_50, self.btn_start, self.btn_garden, self.btn_history]:
            b.setFixedHeight(36)

        # 模式按钮布局
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(self.btn_25)
        mode_layout.addWidget(self.btn_50)

        # 主布局
        layout = QVBoxLayout()
        layout.addWidget(title, alignment=Qt.AlignCenter)
        layout.addWidget(self.stats, alignment=Qt.AlignCenter)
        layout.addSpacing(6)
        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addLayout(mode_layout)
        layout.addSpacing(8)
        layout.addWidget(self.btn_start)
        layout.addWidget(self.btn_garden)
        layout.addWidget(self.btn_history)
        layout.addSpacing(10)
        layout.addWidget(self.pet_label, alignment=Qt.AlignRight)
        self.setLayout(layout)

        # 事件绑定
        self.btn_25.clicked.connect(lambda: self.select_mode(25))
        self.btn_50.clicked.connect(lambda: self.select_mode(50))
        self.btn_start.clicked.connect(self.start_clicked)
        self.btn_garden.clicked.connect(self.show_garden)
        self.btn_history.clicked.connect(self.show_history)

        self.refresh_stats()

    def select_mode(self, minutes):
        """切换模式按钮高亮"""
        self.selected_minutes = minutes
        if minutes == 25:
            self.btn_25.setStyleSheet("background:#f87171; color:white; border-radius:10px; font-size:14px;")
            self.btn_50.setStyleSheet("background:#f7e7c2; color:#3a2f2f; border-radius:10px; font-size:14px;")
        else:
            self.btn_50.setStyleSheet("background:#f87171; color:white; border-radius:10px; font-size:14px;")
            self.btn_25.setStyleSheet("background:#f7e7c2; color:#3a2f2f; border-radius:10px; font-size:14px;")

    def refresh_stats(self):
        """刷新今日专注时长与宠物状态"""
        history = get_history()
        today = date.today().isoformat()
        total = history.get(today, 0)
        self.stats.setText(f"Today's Focus: {total} min")

        pet = load_growing()
        if pet:
            stage_name = {1: "Baby", 2: "Growing", 3: "Adult"}.get(pet.stage, "Unknown")
            self.pet_label.setText(f"{pet.icon} Current Pet: {pet.name} ({stage_name})")
        else:
            self.pet_label.setText("No current pet 🕊")

    def start_clicked(self):
        self.start_callback(self.selected_minutes)

    def show_history(self):
        """查看历史"""
        history = get_history()
        if not history:
            QMessageBox.information(self, "History", "No focus records yet.")
            return
        text = "Date\tMinutes\n" + "-" * 22 + "\n"
        for day, minutes in sorted(history.items()):
            text += f"{day}\t{minutes} min\n"
        QMessageBox.information(self, "Focus History", text)

    def show_garden(self):
        """打开花园"""
        self.garden_window = GardenPage()
        self.garden_window.show()




