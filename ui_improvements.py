from PyQt6.QtWidgets import QWidget, QVBoxLayout, QProgressBar
from PyQt6.QtCore import Qt

class LoadingOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 10px;
            }
        """)
        layout.addWidget(self.progress)
        self.setLayout(layout)
        
    def start_loading(self):
        self.progress.setRange(0, 0)  # 显示忙碌状态
        self.show()
        
    def stop_loading(self):
        self.progress.setRange(0, 100)
        self.hide() 