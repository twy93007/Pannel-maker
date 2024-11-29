import PyInstaller.__main__
import os

def build_app():
    params = [
        'main.py',
        '--name=经济数据面板生成器',
        '--windowed',
        '--onefile',
        '--clean',
        '--icon=icon.ico',
        '--add-data=panel_generator.py:.',
        '--add-data=data_processor.py:.',
        '--add-data=ui_improvements.py:.',
        '--add-data=security.py:.',
        '--add-data=backup.py:.',
        '--add-data=monitor.py:.',
        '--add-data=icon.ico:.',
        '--hidden-import=pandas',
        '--hidden-import=PyQt6',
        '--hidden-import=openpyxl',
        '--hidden-import=requests',
        '--hidden-import=numpy',
        '--hidden-import=matplotlib',
        '--hidden-import=psutil',
        '--hidden-import=cryptography',
    ]
    
    PyInstaller.__main__.run(params)

if __name__ == '__main__':
    build_app() 