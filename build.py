import PyInstaller.__main__
import os
import sys

def build_exe():
    # 确保资源文件存在
    required_files = [
        'main.py',
        'panel_generator.py',
        'styles.py',
        'icon.png'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"错误: 找不到文件 {file}")
            sys.exit(1)

    # PyInstaller 参数
    params = [
        'main.py',  # 主程序文件
        '--name=经济数据面板生成器',  # 生成的exe名称
        '--windowed',  # 不显示控制台窗口
        '--onefile',  # 打包成单个文件
        '--clean',  # 清理临时文件
        '--noconfirm',  # 不确认覆盖
        '--icon=icon.png',  # 程序图标
        
        # 添加数据文件
        '--add-data=styles.py;.',  # Windows使用分号作为分隔符
        '--add-data=panel_generator.py;.',
        '--add-data=icon.png;.',
        
        # 添加必要的依赖
        '--hidden-import=pandas',
        '--hidden-import=openpyxl',
        '--hidden-import=PyQt6',
        
        # 优化选项
        '--noupx',  # 不使用UPX压缩
        '--disable-windowed-traceback',  # 禁用窗口化错误回溯
    ]

    print("开始打包...")
    PyInstaller.__main__.run(params)
    print("打包完成！")

if __name__ == '__main__':
    build_exe() 