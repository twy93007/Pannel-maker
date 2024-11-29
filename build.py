import PyInstaller.__main__
import os

def build_app():
    params = [
        'main.py',
        '--name=EconPanelMaker',
        '--windowed',
        '--onefile',
        '--clean',
        '--icon=icon.ico',
        '--add-data=panel_generator.py;.',
        '--add-data=base_data.py;.',
        '--add-data=styles.py;.',
        '--add-data=updater.py;.',
        '--add-data=icon.ico;.',
        '--add-data=使用说明_小红书版.txt;.',
        '--hidden-import=pandas',
        '--hidden-import=PyQt6',
        '--hidden-import=openpyxl',
        '--hidden-import=requests',
        '--hidden-import=packaging',
    ]
    
    PyInstaller.__main__.run(params)

if __name__ == '__main__':
    build_app() 