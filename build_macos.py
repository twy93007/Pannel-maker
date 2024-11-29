import PyInstaller.__main__
import os
import sys
import plistlib

def create_info_plist():
    """创建 Info.plist 文件"""
    info = {
        'CFBundleName': '经济数据面板生成器',
        'CFBundleDisplayName': '经济数据面板生成器',
        'CFBundleIdentifier': 'com.yourcompany.panelmaker',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundlePackageType': 'APPL',
        'CFBundleSignature': '????',
        'LSMinimumSystemVersion': '10.10.0',
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,
    }
    
    with open('Info.plist', 'wb') as f:
        plistlib.dump(info, f)

def build_app():
    # 确保资源文件存在
    required_files = [
        'main.py',
        'panel_generator.py',
        'styles.py',
        'updater.py',
        'icon.png'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"错误: 找不到文件 {file}")
            sys.exit(1)
    
    # 创建 icns 图标
    print("正在创建图标...")
    os.system('''
        mkdir icon.iconset
        sips -z 16 16   icon.png --out icon.iconset/icon_16x16.png
        sips -z 32 32   icon.png --out icon.iconset/icon_16x16@2x.png
        sips -z 32 32   icon.png --out icon.iconset/icon_32x32.png
        sips -z 64 64   icon.png --out icon.iconset/icon_32x32@2x.png
        sips -z 128 128 icon.png --out icon.iconset/icon_128x128.png
        sips -z 256 256 icon.png --out icon.iconset/icon_128x128@2x.png
        sips -z 256 256 icon.png --out icon.iconset/icon_256x256.png
        iconutil -c icns icon.iconset
        rm -rf icon.iconset
    ''')

    # PyInstaller 参数
    params = [
        'main.py',  # 主程序文件
        '--name=经济数据面板生成器',  # 生成的应用名称
        '--windowed',  # 不显示控制台窗口
        '--onefile',  # 打包成单个文件
        '--clean',  # 清理临时文件
        '--noconfirm',  # 不确认覆盖
        '--icon=icon.icns',  # 使用创建的图标
        
        # 添加数据文件
        '--add-data=styles.py:.',
        '--add-data=panel_generator.py:.',
        '--add-data=updater.py:.',
        '--add-data=icon.icns:.',
        
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

    # 创建 DMG 文件
    print("正在创建 DMG 文件...")
    os.system(f'''
        create-dmg \\
          --volname "经济数据面板生成器" \\
          --volicon "icon.icns" \\
          --window-pos 200 120 \\
          --window-size 600 400 \\
          --icon-size 100 \\
          --icon "经济数据面板生成器.app" 175 120 \\
          --app-drop-link 425 120 \\
          --no-internet-enable \\
          "经济数据面板生成器.dmg" \\
          "dist/经济数据面板生成器.app"
    ''')
    print("DMG 文件创建完成！")

    # 清理临时文件
    os.remove('icon.icns')

if __name__ == '__main__':
    build_app() 