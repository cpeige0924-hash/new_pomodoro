# ui/menu_page.py
# ----------------------------
# 主菜单界面：选择番茄钟长度、显示今日专注时长、进入计时页面。
# ----------------------------
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from core.state_manager import get_history
from datetime import date

class MenuPage(QWidget):
    def __init__(self, start_callback):
        super().__init__()
        self.start_callback = start_callback
        self.selected_minutes = 25  # 默认25分钟

        # --- Title ---
        title = QLabel("🍅 Pomodoro Timer")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")

        # --- Today's focus ---
        from datetime import date
        history = get_history()
        today = date.today().isoformat()
        total = history.get(today, 0)
        self.stats = QLabel(f"Today's Focus: {total} min")

        # --- Mode selection ---
        label = QLabel("Select your session length:")
        label.setStyleSheet("font-size: 14px;")

        self.btn_25 = QPushButton("25 min")
        self.btn_50 = QPushButton("50 min")
        self.btn_start = QPushButton("Start")

        for b in [self.btn_25, self.btn_50, self.btn_start]:
            b.setFixedHeight(35)
            b.setStyleSheet("font-size:14px;")

        # Layout for 25/50 buttons
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(self.btn_25)
        mode_layout.addWidget(self.btn_50)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.stats)
        layout.addWidget(label)
        layout.addLayout(mode_layout)
        layout.addWidget(self.btn_start)
        # --- History button ---
        self.btn_history = QPushButton("📅 View History")
        self.btn_history.clicked.connect(self.show_history)
        layout.addWidget(self.btn_history)
        self.setLayout(layout)
        # --- Connect events ---
        self.btn_25.clicked.connect(lambda: self.select_mode(25))
        self.btn_50.clicked.connect(lambda: self.select_mode(50))
        self.btn_start.clicked.connect(self.start_clicked)

    def select_mode(self, minutes):
        """切换模式（按钮高亮）"""
        self.selected_minutes = minutes
        if minutes == 25:
            self.btn_25.setStyleSheet("background:#f87171; color:white; font-size:14px;")
            self.btn_50.setStyleSheet("font-size:14px;")
        else:
            self.btn_50.setStyleSheet("background:#f87171; color:white; font-size:14px;")
            self.btn_25.setStyleSheet("font-size:14px;")

    def refresh_stats(self):
        """刷新今日专注时长"""
        history = get_history()
        today = date.today().isoformat()
        total = history.get(today, 0)
        self.stats.setText(f"Today's Focus: {total} min")
        
    def start_clicked(self):
        """点击开始，调用主界面函数"""
        self.start_callback(self.selected_minutes)

    def show_history(self):
        """显示历史专注时长"""
        history = get_history()
        if not history:
            QMessageBox.information(self, "History", "No focus records yet.")
            return

        text = "Date\tMinutes\n" + "-"*22 + "\n"
        for day, minutes in sorted(history.items()):
            text += f"{day}\t{minutes} min\n"

        QMessageBox.information(self, "Focus History", text)

