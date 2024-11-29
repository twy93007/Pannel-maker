import PyInstaller.__main__
import os

def build_app():
    params = [
        'main.py',
        '--name=经济数据面板生成器',
        '--windowed',
        '--onefile',
        '--clean',
        '--add-data=data_processor.py:.',
        '--add-data=ui_improvements.py:.',
        '--add-data=security.py:.',
        '--add-data=backup.py:.',
        '--add-data=monitor.py:.',
        '--hidden-import=psutil',
        '--hidden-import=cryptography',
    ]
    
    PyInstaller.__main__.run(params)

if __name__ == '__main__':
    build_app() 