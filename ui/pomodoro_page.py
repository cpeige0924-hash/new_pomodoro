# ui/pomodoro_page.py
# ---------------------------------------------------------
# Pomodoro floating window: timer + pet ASCII display
# ---------------------------------------------------------
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea, QApplication
from PyQt5.QtCore import Qt
from core.timer import PomodoroTimer
from core.pet_manager import load_growing
from core.ascii_art import get_ascii


class PomodoroPage(QWidget):
    def __init__(self, minutes, on_finish, on_quit):
        super().__init__()
        self.on_finish = on_finish
        self.on_quit = on_quit
        self.is_paused = False

        # 🐾 load growing pet only
        self.pet = load_growing()
        self.pet_species = self.pet.species
        self.pet_stage = self.pet.stage

        # --- Pet display ---
        self.pet_label = QLabel()
        self.pet_label.setAlignment(Qt.AlignCenter)
        self.pet_label.setStyleSheet("""
            QLabel {
                font-family: 'Courier New', monospace;
                font-size: 14px;
                color: #2d2a26;
                background-color: rgba(255,255,245,80);
                border-radius: 8px;
                padding: 4px;
            }
        """)
        self.pet_label.setText(get_ascii(self.pet_species, self.pet_stage))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        scroll.setWidget(self.pet_label)

        # --- Timer display ---
        self.timer_label = QLabel("00:00")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #2d2a26;")

        # --- Buttons ---
        self.btn_pause = QPushButton("Pause")
        self.btn_quit = QPushButton("Quit")
        for btn in [self.btn_pause, self.btn_quit]:
            btn.setFixedHeight(34)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f1e6cf;
                    color: #3a2f2f;
                    font-weight: bold;
                    border-radius: 10px;
                }
                QPushButton:hover { background-color: #e9dcc2; }
            """)

        layout_btn = QHBoxLayout()
        layout_btn.addWidget(self.btn_pause)
        layout_btn.addWidget(self.btn_quit)

        # --- Layout ---
        layout = QVBoxLayout()
        layout.addWidget(scroll)
        layout.addWidget(self.timer_label)
        layout.addLayout(layout_btn)
        layout.setSpacing(8)
        self.setLayout(layout)

        # --- Window appearance ---
        self.setWindowTitle("Pomodoro Pet")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowOpacity(0.92)
        self.setStyleSheet("background-color: rgba(255, 250, 240, 230); border: 1px solid #d9cbb5;")

        # position: bottom right
        screen = QApplication.primaryScreen().geometry()
        window_size = self.sizeHint()
        x = screen.width() - window_size.width() - 40
        y = screen.height() - window_size.height() - 80
        self.move(x, y)

        # enable dragging
        self._drag_pos = None
        self.mousePressEvent = self._start_drag
        self.mouseMoveEvent = self._move_window
        self.mouseReleaseEvent = self._end_drag

        # --- Timer logic ---
        self.timer = PomodoroTimer(minutes, self.update_time, self.finish_session)
        self.timer.start()

        # --- Events ---
        self.btn_pause.clicked.connect(self.toggle_pause)
        self.btn_quit.clicked.connect(self.quit_session)

    # -------------------------------
    # Timer update methods
    # -------------------------------
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
        """When the timer completes, close window and return to menu"""
        self.timer.stop()
        self.close()
        self.on_finish()

    def quit_session(self):
        """Manual quit"""
        self.timer.stop()
        self.close()
        self.on_quit()

    # -------------------------------
    # Dragging implementation
    # -------------------------------
    def _start_drag(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()

    def _move_window(self, event):
        if event.buttons() == Qt.LeftButton and self._drag_pos:
            self.move(event.globalPos() - self._drag_pos)

    def _end_drag(self, event):
        self._drag_pos = None








