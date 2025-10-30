# main.py
import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget, QMessageBox, QDialog
from ui.menu_page import MenuPage
from ui.pomodoro_page import PomodoroPage
from ui.pet_setup import PetSetupDialog
from core.state_manager import add_focus
from core.pet_manager import load_growing, add_to_garden, clear_growing

class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.menu = MenuPage(self.start_pomodoro)
        self.addWidget(self.menu)
        self.setCurrentWidget(self.menu)
        self.setWindowTitle("Pomodoro Pet Timer")
        self.resize(320, 220)

    # --------------------------------------------------------
    # 启动番茄钟：若无宠物 → 弹出创建窗口（主页面保留）
    # --------------------------------------------------------
    def start_pomodoro(self, minutes):
        pet = load_growing()
        if pet is None:
            dlg = PetSetupDialog(self)
            # 主页面不隐藏，弹窗置顶在前方
            dlg.setModal(True)
            if dlg.exec_() != QDialog.Accepted:
                return  # 用户取消创建
            pet = load_growing()  # 创建完成后重新加载

        # 启动浮窗番茄钟
        self.hide()
        self.pomodoro = PomodoroPage(
            minutes,
            lambda: self.finish_pomodoro(minutes),
            self.quit_pomodoro
        )
        self.pomodoro.show()

    # --------------------------------------------------------
    # 完成番茄钟：记录数据、成长宠物
    # --------------------------------------------------------
    def finish_pomodoro(self, minutes):
        add_focus(minutes)

        # --- 宠物成长逻辑 ---
        pet = load_growing()
        if pet:
            stage_changed, matured = pet.add_progress(minutes)
            if stage_changed and not matured:
                QMessageBox.information(self, "Growth", "Your pet has grown!")
            if matured:
                add_to_garden(pet)
                clear_growing()
                QMessageBox.information(
                    self,
                    "Garden",
                    "Your pet has fully grown and moved to the Garden!\n"
                    "You can create a new pet next time you start a Pomodoro."
                )

        # --- 回主界面 ---
        if hasattr(self, "pomodoro"):
            self.pomodoro.close()
        self.show()
        self.activateWindow()
        self.menu.refresh_stats()

    # --------------------------------------------------------
    # 手动退出番茄钟（不成长、不计时）
    # --------------------------------------------------------
    def quit_pomodoro(self):
        if hasattr(self, "pomodoro"):
            self.pomodoro.close()
        self.show()
        self.activateWindow()

# ------------------------------------------------------------
# 启动应用
# ------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


