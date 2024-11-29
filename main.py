import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QTabWidget, QLabel, QStatusBar, QMenuBar, QToolBar)
from PyQt6.QtGui import QAction  # 从 QtGui 导入 QAction
from PyQt6.QtCore import Qt
from panel_generator import PanelGenerator
from updater import UpdateChecker, Updater

class MainWindow(QMainWindow):
    VERSION = "1.1.0"  # 版本号
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'经济数据面板生成器 {self.VERSION}')
        self.setGeometry(100, 100, 800, 600)
        
        # 创建主布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # 创建菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        help_menu = menubar.addMenu('帮助')
        settings_menu = menubar.addMenu('设置')
        
        # 添加菜单项
        theme_action = QAction('切换主题', self)
        theme_action.triggered.connect(self.toggle_theme)
        settings_menu.addAction(theme_action)
        
        # 创建工具栏
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # 创建标签页
        tabs = QTabWidget()
        tabs.addTab(self.create_province_tab(), "省份面板")
        tabs.addTab(self.create_city_tab(), "城市面板")
        tabs.addTab(self.create_custom_tab(), "自定义面板")
        layout.addWidget(tabs)
        
        # 添加状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        # 添加版权信息
        copyright_label = QLabel("© 2024 经济数据面板生成器. 保留所有权利。")
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        copyright_label.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 12px;
                padding: 10px;
                border-top: 1px solid #dcdde1;
            }
        """)
        layout.addWidget(copyright_label)
        
        # 创建更新检查器
        self.update_checker = UpdateChecker()
        self.update_checker.update_available.connect(self.show_update_dialog)
        self.update_checker.error_occurred.connect(self.show_update_error)
        
        # 启动更新检查
        self.update_checker.start()
    
    def create_province_tab(self):
        """创建省份面板标签页"""
        widget = QWidget()
        # 添加省份面板的具体内容
        return widget
    
    def create_city_tab(self):
        """创建城市面板标签页"""
        widget = QWidget()
        # 添加城市面板的具体内容
        return widget
    
    def create_custom_tab(self):
        """创建自定义面板标签页"""
        widget = QWidget()
        # 添加自定义面板的具体内容
        return widget
    
    def toggle_theme(self):
        """切换主题"""
        # 实现主题切换功能
        pass

    def show_update_dialog(self, new_version, changelog):
        """显示更新对话框"""
        reply = QMessageBox.question(
            self,
            '发现新版本',
            f'发现新版本 {new_version}\n\n更新内容：\n{changelog}\n\n是否现在更新？',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.start_update()
    
    def show_update_error(self, error):
        """显示更新错误"""
        QMessageBox.warning(
            self,
            '更新检查失败',
            f'检查更新时出错：{error}'
        )
    
    def start_update(self):
        """开始更新"""
        self.progress_dialog = QProgressDialog('正在下载更新...', '取消', 0, 100, self)
        self.progress_dialog.setWindowTitle('更新进度')
        self.progress_dialog.setAutoClose(True)
        self.progress_dialog.setAutoReset(True)
        
        self.updater = Updater(
            "https://github.com/twy93007/Pannel-maker/releases/latest/download/经济数据面板生成器.exe"
        )
        self.updater.progress.connect(self.progress_dialog.setValue)
        self.updater.finished.connect(self.on_update_finished)
        self.updater.error.connect(self.on_update_error)
        
        self.updater.start()
        self.progress_dialog.show()
    
    def on_update_finished(self):
        """更新完成"""
        QMessageBox.information(
            self,
            '更新完成',
            '更新已下载完成，程序将重启以完成更新。'
        )
        QApplication.quit()
    
    def on_update_error(self, error):
        """更新错误"""
        QMessageBox.warning(
            self,
            '更新失败',
            f'更新过程中出错：{error}'
        )

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 