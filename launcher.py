import sys
import os
from pathlib import Path

def resource_path(relative_path):
    """ 获取资源文件的绝对路径 """
    try:
        # PyInstaller创建临时文件夹，将路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    # 设置工作目录
    if getattr(sys, 'frozen', False):
        # 如果是打包后的exe运行
        os.chdir(os.path.dirname(sys.executable))
    
    # 导入主程序
    from main import PanelGenerator, QApplication
    
    # 创建应用
    app = QApplication(sys.argv)
    
    # 设置应用图标
    icon_path = resource_path('icon.png')
    if os.path.exists(icon_path):
        from PyQt6.QtGui import QIcon
        app.setWindowIcon(QIcon(icon_path))
    
    # 创建主窗口
    window = PanelGenerator()
    window.show()
    
    # 运行应用
    sys.exit(app.exec()) 