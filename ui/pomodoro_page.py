 # ui/pomodoro_page.py
# ------------------------------------------------
# 番茄钟倒计时界面：半透明圆角深色面板、置顶、右下角、全区域可拖动
# ------------------------------------------------
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QApplication
)
from PyQt5.QtCore import Qt, QPoint, QEvent
from core.timer import PomodoroTimer

class PomodoroPage(QWidget):
    def __init__(self, minutes, on_finish, on_quit):
        # 顶层窗口：用 QWidget 作为独立窗体（不是栈里的子页）
        super().__init__(parent=None)
        self.on_finish = on_finish
        self.on_quit = on_quit
        self.is_paused = False
        self._dragging = False
        self._drag_pos = QPoint()

        # —— 窗口外观：半透明+无边框+置顶（不进任务栏） ——
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(
            Qt.Window |                # 顶层窗口
            Qt.Tool |                  # 不占任务栏
            Qt.FramelessWindowHint |   # 无标题栏
            Qt.WindowStaysOnTopHint    # 永远置顶
        )

        # —— 外层根布局（透明），内层面板提供可读背景 ——
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        self.panel = QWidget(self)            # 深色半透明圆角底
        self.panel.setObjectName("panel")
        self.panel.setStyleSheet("""
            #panel {
                background-color: rgba(20, 20, 20, 200);   /* 深色半透明 */
                border-radius: 14px;
            }
            QLabel {
                color: white;                /* 文本高对比 */
            }
        """)
        panel_layout = QVBoxLayout(self.panel)
        panel_layout.setContentsMargins(16, 16, 16, 16)
        panel_layout.setSpacing(12)

        # --- Timer display ---
        self.label = QLabel("00:00", self.panel)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 36px; font-weight: bold;")

        # --- Buttons ---
        self.btn_pause = QPushButton("Pause", self.panel)
        self.btn_quit  = QPushButton("Quit",  self.panel)
        for b in (self.btn_pause, self.btn_quit):
            b.setFixedHeight(36)
            b.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255,255,255,0.18);
                    color: white;
                    font-size: 14px;
                    border: 0px;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: rgba(255,255,255,0.30);
                }
                QPushButton:pressed {
                    background-color: rgba(255,255,255,0.38);
                }
            """)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        btn_row.addWidget(self.btn_pause)
        btn_row.addWidget(self.btn_quit)

        panel_layout.addWidget(self.label)
        panel_layout.addLayout(btn_row)

        root.addWidget(self.panel)

        # —— 设定默认尺寸与右下角位置 ——
        w, h = 260, 160
        self.resize(w, h)
        screen_geo = QApplication.primaryScreen().availableGeometry()
        x = screen_geo.right()  - w - 24
        y = screen_geo.bottom() - h - 24
        self.move(x, y)

        # —— 全区域可拖动：对 self 与 panel、label 安装事件过滤器 —
        for wdg in (self, self.panel, self.label):
            wdg.installEventFilter(self)

        # --- Timer logic ---
        self.timer = PomodoroTimer(minutes, self.update_time, self.finish_session)
        self.timer.start()

        # --- Button events ---
        self.btn_pause.clicked.connect(self.toggle_pause)
        self.btn_quit.clicked.connect(self.quit_session)

    # 事件过滤器：在非按钮区域拖动窗口（按钮仍可正常点击）
    def eventFilter(self, obj, event):
        # 不拦截按钮点击
        if obj in (self.btn_pause, self.btn_quit):
            return super().eventFilter(obj, event)

        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            self._dragging = True
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            return True

        if event.type() == QEvent.MouseMove and self._dragging:
            self.move(event.globalPos() - self._drag_pos)
            return True

        if event.type() == QEvent.MouseButtonRelease:
            self._dragging = False
            return True

        return super().eventFilter(obj, event)

    # --- Timer updates ---
    def update_time(self, remaining):
        mins, secs = divmod(remaining, 60)
        self.label.setText(f"{mins:02d}:{secs:02d}")

    def toggle_pause(self):
        if self.is_paused:
            self.timer.resume()
            self.btn_pause.setText("Pause")
            self.is_paused = False
        else:
            self.timer.pause()
            self.btn_pause.setText("Resume")
            self.is_paused = True

    def finish_session(self):
        self.on_finish()
        self.close()

    def quit_session(self):
        self.timer.stop()
        self.on_quit()
        self.close()



