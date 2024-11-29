import PyInstaller.__main__
import os
import sys

def build_exe():
    # 确保资源文件存在
    required_files = [
        'main.py',
        'panel_generator.py',
        'styles.py',
        'updater.py',
        'icon.ico'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"错误: 找不到文件 {file}")
            sys.exit(1)

    # PyInstaller 参数
    params = [
        'main.py',  # 主程序文件
        '--name=经济数据面板生成器',  # 生成的exe名称
        '--version-file=version_info.txt',  # 添加版本信息文件
        '--windowed',  # 不显示控制台窗口
        '--onefile',  # 打包成单个文件
        '--clean',  # 清理临时文件
        '--noconfirm',  # 不确认覆盖
        '--icon=icon.ico',  # 程序图标
        
        # 添加数据文件
        '--add-data=styles.py;.',
        '--add-data=panel_generator.py;.',
        '--add-data=updater.py;.',
        '--add-data=icon.ico;.',
        
        # 添加必要的依赖
        '--hidden-import=pandas',
        '--hidden-import=openpyxl',
        '--hidden-import=PyQt6',
        '--hidden-import=requests',  # 添加 requests 依赖
        '--hidden-import=urllib3',   # requests 的依赖
        '--hidden-import=chardet',   # requests 的依赖
        '--hidden-import=certifi',   # requests 的依赖
        '--hidden-import=idna',      # requests 的依赖
    ]

    print("开始打包...")
    PyInstaller.__main__.run(params)
    print("打包完成！")

if __name__ == '__main__':
    build_exe() 