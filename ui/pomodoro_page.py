# ---------------------------------------------------------
# Pomodoro floating window: timer + pet ASCII display
# ---------------------------------------------------------
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QApplication
from PyQt5.QtCore import Qt
from core.timer import PomodoroTimer
from core.pet_manager import load_growing
from core.ascii_art import get_ascii


class PomodoroPage(QWidget):
    def __init__(self, minutes, on_finish, on_quit, pet):
        super().__init__()
        self.on_finish = on_finish
        self.on_quit = on_quit
        self.is_paused = False

        #  加载成长中宠物
        self.pet = pet
        self.pet_species = self.pet.species
        self.pet_stage = self.pet.stage

        # --- 宠物 ASCII 区 ---
        self.pet_label = QLabel()
        self.pet_label.setAlignment(Qt.AlignCenter)
        self.pet_label.setStyleSheet("""
            QLabel {
                font-family: 'Courier New', monospace;
                font-size: 14px;
                color: #3a2f2f;
                background-color: rgba(255,255,250,0.8);
                border-radius: 12px;
                padding: 6px;
                border: 1px solid #e6d6b8;
            }
        """)
        self.pet_label.setText(get_ascii(self.pet_species, self.pet_stage))

        # --- 陪伴文字 ---
        self.accompany_label = QLabel(
            f"Your {self.pet.species} {self.pet.name} is accompanying you 💗"
        )
        self.accompany_label.setAlignment(Qt.AlignCenter)
        self.accompany_label.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-style: italic;
                color: #5c4b3b;
                background: transparent;
                margin-bottom: 6px;
            }
        """)

        # --- 倒计时显示 ---
        self.timer_label = QLabel("00:00")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("""
            QLabel {
                font-size: 30px;
                font-weight: bold;
                color: #3a2f2f;
                margin-top: 4px;
            }
        """)

        # --- 按钮 ---
        self.btn_pause = QPushButton("Pause")
        self.btn_quit = QPushButton("Quit")
        for btn in [self.btn_pause, self.btn_quit]:
            btn.setFixedHeight(36)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f7e7c2;
                    color: #3a2f2f;
                    font-weight: bold;
                    border-radius: 10px;
                    padding: 4px 10px;
                }
                QPushButton:hover {
                    background-color: #f3d9a8;
                }
            """)

        btn_row = QHBoxLayout()
        btn_row.addWidget(self.btn_pause)
        btn_row.addWidget(self.btn_quit)

        # --- 总体布局 ---
        layout = QVBoxLayout()
        layout.addWidget(self.pet_label)
        layout.addWidget(self.accompany_label)
        layout.addWidget(self.timer_label)
        layout.addLayout(btn_row)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        self.setLayout(layout)

        # --- 窗口外观 ---
        self.setWindowTitle("Pomodoro Pet")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowOpacity(0.94)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 250, 240, 0.92);
                border: 1px solid #e4d3b4;
                border-radius: 14px;
            }
        """)

        # --- 初始位置（右下角） ---
        screen = QApplication.primaryScreen().geometry()
        window_size = self.sizeHint()
        x = screen.width() - window_size.width() - 40
        y = screen.height() - window_size.height() - 80
        self.move(x, y)

        # --- 可拖动浮窗 ---
        self._drag_pos = None
        self.mousePressEvent = self._start_drag
        self.mouseMoveEvent = self._move_window
        self.mouseReleaseEvent = self._end_drag

        # --- 定时逻辑 ---
        self.timer = PomodoroTimer(minutes, self.update_time, self.finish_session)
        self.timer.start()

        # --- 按钮事件 ---
        self.btn_pause.clicked.connect(self.toggle_pause)
        self.btn_quit.clicked.connect(self.quit_session)

    # ---------------- 计时更新 ----------------
    def update_time(self, remaining):
        mins, secs = divmod(remaining, 60)
        self.timer_label.setText(f"{mins:02d}:{secs:02d}")

    def toggle_pause(self):
        if self.is_paused:
            self.timer.resume()
            self.btn_pause.setText("Pause")
        else:
            self.timer.pause()
            self.btn_pause.setText("Resume")
        self.is_paused = not self.is_paused

    def finish_session(self):
        self.timer.stop()
        self.close()
        self.on_finish()

    def quit_session(self):
        self.timer.stop()
        self.close()
        self.on_quit()

    # ------------- 拖动逻辑 -------------
    def _start_drag(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
    def _move_window(self, event):
        if event.buttons() == Qt.LeftButton and self._drag_pos:
            self.move(event.globalPos() - self._drag_pos)
    def _end_drag(self, event):
        self._drag_pos = None









