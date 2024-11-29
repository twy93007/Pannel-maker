import json
import os
import sys
import requests
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal
import tempfile
import subprocess
from packaging import version

class UpdateChecker(QThread):
    """更新检查线程"""
    update_available = pyqtSignal(str, str)  # 版本号, 更新日志
    error_occurred = pyqtSignal(str)
    
    CURRENT_VERSION = "1.1.3"
    VERSION_URL = "https://raw.githubusercontent.com/twy93007/Pannel-maker/main/version.json"
    
    def run(self):
        try:
            response = requests.get(self.VERSION_URL, timeout=5)
            version_info = response.json()
            
            current = version.parse(self.CURRENT_VERSION)
            latest = version.parse(version_info["version"])
            
            if latest > current:
                self.update_available.emit(
                    version_info["version"],
                    version_info["changelog"]
                )
        except Exception as e:
            self.error_occurred.emit(str(e))

class Updater(QThread):
    """更新下载器"""
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, download_url):
        super().__init__()
        self.download_url = download_url
        
    def run(self):
        try:
            response = requests.get(self.download_url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            # 使用英文名称的临时文件
            temp_dir = tempfile.gettempdir()
            temp_file = os.path.join(temp_dir, "EconPanelMaker_new.exe")
            
            block_size = 1024
            downloaded = 0
            
            with open(temp_file, 'wb') as f:
                for data in response.iter_content(block_size):
                    downloaded += len(data)
                    f.write(data)
                    progress = int((downloaded / total_size) * 100)
                    self.progress.emit(progress)
            
            # 创建更新批处理文件
            batch_file = os.path.join(temp_dir, "update.bat")
            current_exe = sys.executable
            
            with open(batch_file, 'w', encoding='utf-8') as f:
                f.write('@echo off\n')
                f.write('timeout /t 2 /nobreak > nul\n')
                f.write(f'del "{current_exe}"\n')
                f.write(f'move /Y "{temp_file}" "{current_exe}"\n')
                f.write(f'start "" "{current_exe}"\n')
                f.write('del "%~f0"\n')
            
            subprocess.Popen(['cmd', '/c', batch_file], 
                           shell=True, 
                           creationflags=subprocess.CREATE_NO_WINDOW)
            
            self.finished.emit()
            
        except Exception as e:
            self.error.emit(str(e)) 