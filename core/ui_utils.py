from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon

def show_pretty_message(title, text):
    """A soft, clean popup used across the whole app."""
    msg = QMessageBox(QMessageBox.NoIcon, title, text)
    msg.setWindowIcon(QIcon())                         # 去掉标题栏小书
    msg.setWindowFlags(msg.windowFlags() & ~0x00000040) # 防止系统默认图标
    msg.setStyleSheet("""
        QMessageBox {
            background-color: #fffaf3;
            border: 1px solid #e4d3b4;
            border-radius: 10px;
        }
        QLabel {
            color: #3a2f2f;
            font-size: 14px;
        }
        QPushButton {
            background-color: #f7e7c2;
            color: #3a2f2f;
            font-weight: bold;
            border-radius: 8px;
            padding: 4px 12px;
        }
        QPushButton:hover {
            background-color: #f3d9a8;
        }
    """)
    msg.exec_()
