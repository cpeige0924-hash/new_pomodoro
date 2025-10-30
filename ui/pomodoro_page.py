# ui/pomodoro_page.py
# ----------------------------
# 番茄钟倒计时界面：显示剩余时间、暂停、退出。
# ----------------------------
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from core.timer import PomodoroTimer

class PomodoroPage(QWidget):
    def __init__(self, minutes, on_finish, on_quit):
        super().__init__()
        self.on_finish = on_finish
        self.on_quit = on_quit
        self.is_paused = False

        # --- Timer display ---
        self.label = QLabel("00:00")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 36px; font-weight: bold;")

        # --- Buttons ---
        self.btn_pause = QPushButton("Pause")
        self.btn_quit = QPushButton("Quit")

        self.btn_pause.setFixedHeight(35)
        self.btn_quit.setFixedHeight(35)

        layout_btn = QHBoxLayout()
        layout_btn.addWidget(self.btn_pause)
        layout_btn.addWidget(self.btn_quit)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(layout_btn)
        self.setLayout(layout)

        # 半透明浮窗效果
        self.setWindowOpacity(0.85)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # --- Timer logic ---
        self.timer = PomodoroTimer(minutes, self.update_time, self.finish_session)
        self.timer.start()

        # --- Button events ---
        self.btn_pause.clicked.connect(self.toggle_pause)
        self.btn_quit.clicked.connect(self.quit_session)

    def update_time(self, remaining):
        """更新倒计时显示"""
        mins, secs = divmod(remaining, 60)
        self.label.setText(f"{mins:02d}:{secs:02d}")

    def toggle_pause(self):
        """暂停/继续"""
        if self.is_paused:
            self.timer.resume()
            self.btn_pause.setText("Pause")
            self.is_paused = False
        else:
            self.timer.pause()
            self.btn_pause.setText("Resume")
            self.is_paused = True

    def finish_session(self):
        """计时结束"""
        self.on_finish()

    def quit_session(self):
        """手动退出"""
        self.timer.stop()
        self.on_quit()
