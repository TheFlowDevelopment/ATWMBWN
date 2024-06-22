from win32api import GetMonitorInfo, MonitorFromPoint

class MonitorHandler():
    def __init__(self) -> None:
        self.MonitorWorkableX = None
        self.MonitorWorkableY = None

    def setup(self):
        monitorWorkable = GetMonitorInfo(MonitorFromPoint((0, 0))).get('Work')
        self.MonitorWorkableX = monitorWorkable[2]
        self.MonitorWorkableY = monitorWorkable[3]