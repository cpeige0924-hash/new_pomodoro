# main.py
# ----------------------------
# 程序入口：负责页面切换和数据记录。
# ----------------------------
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
        """进入番茄钟页面"""
        self.pomodoro = PomodoroPage(minutes, 
                                     lambda: self.finish_pomodoro(minutes),
                                     self.quit_pomodoro)
        self.addWidget(self.pomodoro)
        self.setCurrentWidget(self.pomodoro)

    def finish_pomodoro(self, minutes):
        """番茄钟完成：保存并返回主菜单"""
        add_focus(minutes)
        self.show_menu()

    def quit_pomodoro(self):
        """退出番茄钟：不计入时长"""
        self.show_menu()

    def show_menu(self):
        """回主菜单并刷新显示"""
        self.menu.refresh_stats()
        self.setCurrentWidget(self.menu)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
