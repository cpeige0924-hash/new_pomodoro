#minimal, safe and aligned with pet_manager.py / pet.py
# Run this script to start the program: main.py
# Dependencies required: PyQt5
# Note: This program uses a GUI and will NOT run on EdStem environment. 
# Please run locally on a Python 3.10+ environment with PyQt5 installed.

import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget, QDialog
from PyQt5.QtGui import QIcon

from ui.menu_page import MenuPage
from ui.pomodoro_page import PomodoroPage
from ui.pet_setup import PetSetupDialog

from core.state_manager import add_focus
from core.pet_manager import (
    load_growing, save_growing, add_to_garden, clear_growing
)
from core.pet import Pet

# Optional pretty message (if you have it); otherwise we won't break.
try:
    from core.ui_utils import show_pretty_message as _pretty_msg
except Exception:
    _pretty_msg = None
    from PyQt5.QtWidgets import QMessageBox
    def _fallback_msg(title, text):
        m = QMessageBox(QMessageBox.NoIcon, title, text)
        m.setWindowIcon(QIcon())
        m.exec_()

def show_msg(title, text):
    if _pretty_msg:
        _pretty_msg(title, text)
    else:
        _fallback_msg(title, text)


app = QApplication(sys.argv)
app.setWindowIcon(QIcon())  # 全局无图标


class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.menu = MenuPage(self.start_pomodoro)
        self.addWidget(self.menu)
        self.setCurrentWidget(self.menu)
        self.setWindowTitle("Pomodoro Pet Timer")
        self.resize(320, 220)

    # ---------------- 启动番茄钟 ----------------
    def start_pomodoro(self, minutes):
        """
        逻辑与 pet_manager/pet 对齐：
        1) 先尝试载入成长中宠物；
        2) 若无 -> 弹出创建对话框，拿到 (name, species)，构造 Pet 并 save_growing；
        3) 将 pet 作为参数传给 PomodoroPage（不在页面里重复 load）。
        """
        pet = load_growing()
        if pet is None:
            dlg = PetSetupDialog(self)
            dlg.setModal(True)
            if dlg.exec_() != QDialog.Accepted:
                return  # 用户取消创建，不进入番茄钟
            name, species = dlg.get_data()
            # 与 core/pet.py 对齐：Pet(name, species)
            pet = Pet(name, species)
            save_growing(pet)  # 关键：立刻保存为“成长中的宠物”

        # 到这里 pet 一定有效
        self.hide()
        self.pomodoro = PomodoroPage(
            minutes,
            lambda: self.finish_pomodoro(minutes),
            self.quit_pomodoro,
            pet  # 传入页面，避免内部重复 load
        )
        self.pomodoro.show()

    # ---------------- 完成番茄钟 ----------------
    def finish_pomodoro(self, minutes):
        """
        1) 记录专注；
        2) 载入成长中宠物（若存在） -> add_progress(minutes)；
        3) 若成长阶段变化/成熟 -> 提示；成熟则入园并清空成长中；
        4) 关闭浮窗，回到主菜单并刷新统计。
        """
        add_focus(minutes)

        pet = load_growing()
        if pet:
            stage_changed, matured = pet.add_progress(minutes)
            # pet.add_progress 内部已 self.save()；如需冗余安全也可再 save_growing(pet)

            if stage_changed and not matured:
                show_msg("Growth", "Your pet has grown!")

            if matured:
                add_to_garden(pet)
                clear_growing()
                show_msg(
                    "Garden",
                    "Your pet has fully grown and moved to the Garden!\n"
                    "You can create a new pet next time you start a Pomodoro."
                )

        if hasattr(self, "pomodoro"):
            self.pomodoro.close()
        self.show()
        self.activateWindow()
        # 主界面统计刷新（确保你已有此方法）
        try:
            self.menu.refresh_stats()
        except Exception:
            pass

    # ---------------- 手动退出番茄钟 ----------------
    def quit_pomodoro(self):
        if hasattr(self, "pomodoro"):
            self.pomodoro.close()
        self.show()
        self.activateWindow()


if __name__ == "__main__":
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())




