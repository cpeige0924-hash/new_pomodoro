# main.py
import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from ui.menu_page import MenuPage
from ui.pomodoro_page import PomodoroPage
from core.state_manager import add_focus

class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.menu = MenuPage(self.start_pomodoro)
        self.addWidget(self.menu)
        self.setCurrentWidget(self.menu)
        self.setWindowTitle("Pomodoro Timer")
        self.resize(300, 200)

    def start_pomodoro(self, minutes):
        """启动番茄钟并隐藏主界面"""
        self.hide()  # 🩵 启动后隐藏主窗口

        self.pomodoro = PomodoroPage(
            minutes,
            lambda: self.finish_pomodoro(minutes),
            self.quit_pomodoro
        )
        self.pomodoro.show()

    def finish_pomodoro(self, minutes):
        """番茄钟完成：保存并返回主菜单"""
        add_focus(minutes)
        self.pomodoro.close()
        self.show()              # 🩵 重新显示主界面
        self.activateWindow()    # 可选：聚焦窗口
        self.menu.refresh_stats()

    def quit_pomodoro(self):
        """退出番茄钟：不计入时长"""
        if hasattr(self, "pomodoro"):
            self.pomodoro.close()
        self.show()              # 🩵 回到主界面
        self.activateWindow()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

