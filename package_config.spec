# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],  # 主程序文件
    pathex=[],
    binaries=[],
    datas=[
        ('styles.py', '.'),  # 包含样式文件
        ('panel_generator.py', '.'),  # 包含面板生成器
        ('icon.png', '.'),  # 包含图标文件
        ('使用说明.md', '.'),  # 包含说明文件
        ('使用说明_小红书版.txt', '.')  # 包含小红书版说明
    ],
    hiddenimports=[
        'pandas',
        'PyQt6',
        'openpyxl'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='经济数据面板生成器',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 设置为False表示不显示控制台窗口
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'  # 程序图标
) 