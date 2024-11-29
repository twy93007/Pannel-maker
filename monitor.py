import psutil
import time
from PyQt6.QtCore import QThread, pyqtSignal

class PerformanceMonitor(QThread):
    stats_updated = pyqtSignal(dict)
    
    def run(self):
        while True:
            stats = {
                'cpu': psutil.cpu_percent(),
                'memory': psutil.Process().memory_percent(),
                'disk_io': psutil.disk_io_counters(),
                'network': psutil.net_io_counters()
            }
            self.stats_updated.emit(stats)
            time.sleep(1) 