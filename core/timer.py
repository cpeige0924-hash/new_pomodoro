from PyQt5.QtCore import QTimer, QObject

print(" Loading NEW_POMODORO/core/timer.py ...")

class PomodoroTimer(QObject):
    """控制番茄钟倒计时的类"""

    def __init__(self, minutes, on_update, on_finish):
        super().__init__()  # 先初始化父类

        # TEST MODE SWITCH
        testmode = False
        if testmode:
            print("Test mode active: 25 min = 6 s, 50 min = 12 s")

        # 确保参数是数字（可能是 25 / 25.0 / "25"）
        try:
            m = float(minutes)
        except Exception:
            m = 0

        # 根据是否测试模式决定秒数
        if testmode:
            if 24 <= m <= 26:
                total_seconds = 6
            elif 49 <= m <= 51:
                total_seconds = 12
            else:
                total_seconds = int(m * 60)
        else:
            total_seconds = int(m * 60)

        self.remaining = total_seconds           # 不要再重新覆盖
        print(f" total_seconds = {self.remaining}")

        self.on_update = on_update               # 每秒更新界面
        self.on_finish = on_finish               # 结束时回调
        self.qtimer = QTimer()
        self.qtimer.timeout.connect(self._tick)  # 每秒执行 _tick

    def start(self):
        """开始计时"""
        self.qtimer.start(1000)

    def pause(self):
        """暂停计时"""
        self.qtimer.stop()

    def resume(self):
        """继续计时"""
        self.qtimer.start(1000)

    def stop(self):
        """停止计时"""
        self.qtimer.stop()

    def _tick(self):
        """每秒执行：减少剩余时间，更新界面，到 0 停止"""
        self.remaining -= 1
        self.on_update(self.remaining)
        if self.remaining <= 0:
            self.qtimer.stop()
            self.on_finish()


