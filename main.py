import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QTabWidget, 
                            QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
                            QPushButton, QFileDialog, QLineEdit, QTextEdit,
                            QDateEdit, QProgressBar, QRadioButton, QButtonGroup,
                            QProgressDialog, QMessageBox, QStatusBar, QToolBar, QAction)
from PyQt6.QtCore import Qt, QDate, QTimer
from PyQt6.QtGui import QIcon
import pandas as pd
from datetime import datetime, timedelta
import os
from panel_generator import DataPanelGenerator
import json
from pathlib import Path
from styles import MAIN_STYLE
from updater import UpdateChecker, Updater

def resource_path(relative_path):
    """ 获取资源文件的绝对路径 """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class PanelGenerator(QMainWindow):
    VERSION = "V1.0.1"  # 版本号
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'经济数据面板生成器 {self.VERSION}')
        self.setGeometry(100, 100, 800, 600)
        
        # 设置窗口图标
        self.setWindowIcon(QIcon(resource_path('icon.png')))  # 需要准备一个icon.png文件
        
        # 加载配置
        self.config = self.load_config()
        
        # 首先设置进度条样式
        self.progress_bar_style = """
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 10px;
                margin: 0.5px;
            }
        """
        
        # 创建主窗口部件和布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # 创建标签页
        tabs = QTabWidget()
        tabs.addTab(self.create_province_tab(), '省份面板')
        tabs.addTab(self.create_city_tab(), '城市面板')
        tabs.addTab(self.create_custom_tab(), '自定义面板')
        
        layout.addWidget(tabs)
        
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
        
        # 加载基础数据
        self.load_base_data()
        
        # 应用样式表
        app = QApplication.instance()
        app.setStyleSheet(MAIN_STYLE)
        
        # 创建更新检查器
        self.update_checker = UpdateChecker()
        self.update_checker.update_available.connect(self.show_update_dialog)
        self.update_checker.error_occurred.connect(self.show_update_error)
        
        # 启动更新检查
        self.update_checker.start()
        
        # 添加状态栏显示处理进度
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        # 添加菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        help_menu = menubar.addMenu('帮助')
        
        # 添加工具栏
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # 添加主题切换功能
        settings_menu = menubar.addMenu('设置')
        theme_action = QAction('切换主题', self)
        settings_menu.addAction(theme_action)
    
    def load_config(self):
        """加载配置文件"""
        config_path = Path.home() / '.panel_generator_config.json'
        default_config = {
            'last_export_path': str(Path.home()),
            'last_import_path': str(Path.home()),
            'default_format': 'xlsx'
        }
        
        try:
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return default_config
        except Exception:
            return default_config
            
    def save_config(self):
        """保存配置文件"""
        config_path = Path.home() / '.panel_generator_config.json'
        config = {
            'last_export_path': self.province_export_path.text() or str(Path.home()),
            'last_import_path': self.custom_import_path.text() or str(Path.home()),
            'default_format': 'xlsx' if self.province_format_group.checkedId() == 1 else 'csv'
        }
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置文件失败: {e}")

    def closeEvent(self, event):
        """窗口关闭时保存配置"""
        self.save_config()
        event.accept()

    def load_base_data(self):
        # 加载省份数据
        self.province_data = {
            '北京市': '北京', '天津市': '天津', '河北省': '河北',
            # ... 其他省份数据 ...
        }
        
        # 加载城市数据
        self.city_data = {
            '安徽省': ['安庆市', '蚌埠市', '亳州市'],
            # ... 其他城市数据 ...
        }

    def create_province_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 时间频次选择
        freq_layout = QHBoxLayout()
        freq_label = QLabel('时间频次:')
        self.province_freq_combo = QComboBox()
        self.province_freq_combo.addItems(['年', '季度', '月', '周', '日'])
        freq_layout.addWidget(freq_label)
        freq_layout.addWidget(self.province_freq_combo)
        freq_layout.addStretch()
        
        # 时间范围选择
        time_layout = QHBoxLayout()
        start_label = QLabel('开始时间:')
        self.province_start_date = QDateEdit()
        self.province_start_date.setDisplayFormat('yyyy-MM-dd')
        self.province_start_date.setDate(QDate.currentDate().addYears(-1))
        
        end_label = QLabel('结束时间:')
        self.province_end_date = QDateEdit()
        self.province_end_date.setDisplayFormat('yyyy-MM-dd')
        self.province_end_date.setDate(QDate.currentDate())
        
        time_layout.addWidget(start_label)
        time_layout.addWidget(self.province_start_date)
        time_layout.addWidget(end_label)
        time_layout.addWidget(self.province_end_date)
        
        # 输出格式选择
        format_layout = QHBoxLayout()
        format_label = QLabel('输出格式:')
        self.province_format_group = QButtonGroup()
        xlsx_radio = QRadioButton('Excel (xlsx)')
        csv_radio = QRadioButton('CSV')
        xlsx_radio.setChecked(True)
        
        self.province_format_group.addButton(xlsx_radio, 1)
        self.province_format_group.addButton(csv_radio, 2)
        
        format_layout.addWidget(format_label)
        format_layout.addWidget(xlsx_radio)
        format_layout.addWidget(csv_radio)
        format_layout.addStretch()
        
        # 导出路径选择
        export_layout = QHBoxLayout()
        export_label = QLabel('导出路径:')
        self.province_export_path = QLineEdit()
        export_btn = QPushButton('选择导出路径')
        
        # 修改导出按钮的连接方式
        def update_export_path():
            file_filter = 'Excel 文件 (*.xlsx)' if xlsx_radio.isChecked() else 'CSV 文件 (*.csv)'
            self.select_export_path(self.province_export_path, file_filter)
        
        export_btn.clicked.connect(update_export_path)
        
        export_layout.addWidget(export_label)
        export_layout.addWidget(self.province_export_path)
        export_layout.addWidget(export_btn)
        
        # 状态显示区域
        self.province_status = QTextEdit()
        self.province_status.setReadOnly(True)
        self.province_status.setMaximumHeight(100)
        self.province_status.setPlaceholderText('执行状态将在这里显示...')
        self.province_status.setObjectName('statusText')
        
        # 添加进度条
        self.province_progress = QProgressBar()
        self.province_progress.setStyleSheet(self.progress_bar_style)
        self.province_progress.hide()
        
        # 生成按钮
        generate_btn = QPushButton('生成面板')
        generate_btn.setObjectName('generateButton')
        generate_btn.clicked.connect(self.generate_province_panel)
        generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        # 添加所有组件到布局
        layout.addLayout(freq_layout)
        layout.addLayout(time_layout)
        layout.addLayout(format_layout)
        layout.addLayout(export_layout)
        layout.addWidget(self.province_progress)
        layout.addWidget(self.province_status)
        layout.addWidget(generate_btn)
        layout.addStretch()
        
        return tab

    def create_city_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 时间频次选择
        freq_layout = QHBoxLayout()
        freq_label = QLabel('时间频次:')
        self.city_freq_combo = QComboBox()
        self.city_freq_combo.addItems(['年', '季度', '月', '周', '日'])
        freq_layout.addWidget(freq_label)
        freq_layout.addWidget(self.city_freq_combo)
        freq_layout.addStretch()
        
        # 时间范围选择
        time_layout = QHBoxLayout()
        start_label = QLabel('开始时间:')
        self.city_start_date = QDateEdit()
        self.city_start_date.setDisplayFormat('yyyy-MM-dd')
        self.city_start_date.setDate(QDate.currentDate().addYears(-1))
        
        end_label = QLabel('结束时间:')
        self.city_end_date = QDateEdit()
        self.city_end_date.setDisplayFormat('yyyy-MM-dd')
        self.city_end_date.setDate(QDate.currentDate())
        
        time_layout.addWidget(start_label)
        time_layout.addWidget(self.city_start_date)
        time_layout.addWidget(end_label)
        time_layout.addWidget(self.city_end_date)
        
        # 输出格式选择
        format_layout = QHBoxLayout()
        format_label = QLabel('输出格式:')
        self.city_format_group = QButtonGroup()
        xlsx_radio = QRadioButton('Excel (xlsx)')
        csv_radio = QRadioButton('CSV')
        xlsx_radio.setChecked(True)
        
        self.city_format_group.addButton(xlsx_radio, 1)
        self.city_format_group.addButton(csv_radio, 2)
        
        format_layout.addWidget(format_label)
        format_layout.addWidget(xlsx_radio)
        format_layout.addWidget(csv_radio)
        format_layout.addStretch()
        
        # 导出路径选择
        export_layout = QHBoxLayout()
        export_label = QLabel('导出路径:')
        self.city_export_path = QLineEdit()
        export_btn = QPushButton('选择导出路径')
        
        # 修改导出按钮的连接方式
        def update_export_path():
            file_filter = 'Excel 文件 (*.xlsx)' if xlsx_radio.isChecked() else 'CSV 文件 (*.csv)'
            self.select_export_path(self.city_export_path, file_filter)
        
        export_btn.clicked.connect(update_export_path)
        
        export_layout.addWidget(export_label)
        export_layout.addWidget(self.city_export_path)
        export_layout.addWidget(export_btn)
        
        # 状态显示区域
        self.city_status = QTextEdit()
        self.city_status.setReadOnly(True)
        self.city_status.setMaximumHeight(100)
        self.city_status.setPlaceholderText('执行状态将在这里显示...')
        self.city_status.setObjectName('statusText')
        
        # 添加进度条
        self.city_progress = QProgressBar()
        self.city_progress.setStyleSheet(self.progress_bar_style)
        self.city_progress.hide()
        
        # 生成按钮
        generate_btn = QPushButton('生成面板')
        generate_btn.setObjectName('generateButton')
        generate_btn.clicked.connect(self.generate_city_panel)
        generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        # 添加所有组件到布局
        layout.addLayout(freq_layout)
        layout.addLayout(time_layout)
        layout.addLayout(format_layout)
        layout.addLayout(export_layout)
        layout.addWidget(self.city_progress)
        layout.addWidget(self.city_status)
        layout.addWidget(generate_btn)
        layout.addStretch()
        
        return tab

    def create_custom_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 时间频次选择
        freq_layout = QHBoxLayout()
        freq_label = QLabel('时间频次:')
        self.custom_freq_combo = QComboBox()
        self.custom_freq_combo.addItems(['年', '��度', '月', '周', '日'])
        freq_layout.addWidget(freq_label)
        freq_layout.addWidget(self.custom_freq_combo)
        freq_layout.addStretch()
        
        # 导入文件选择
        import_layout = QHBoxLayout()
        import_label = QLabel('导入文件:')
        self.custom_import_path = QLineEdit()
        import_btn = QPushButton('选择文件')
        import_btn.clicked.connect(self.select_import_file)
        
        import_layout.addWidget(import_label)
        import_layout.addWidget(self.custom_import_path)
        import_layout.addWidget(import_btn)
        
        # 导入列数选择
        column_layout = QHBoxLayout()
        column_label = QLabel('导入列数:')
        self.custom_column_input = QLineEdit()
        self.custom_column_input.setPlaceholderText('请输入需要导入的列数')
        
        column_layout.addWidget(column_label)
        column_layout.addWidget(self.custom_column_input)
        column_layout.addStretch()
        
        # 预览按钮和预览区域
        preview_layout = QHBoxLayout()
        preview_btn = QPushButton('预览数据')
        preview_btn.setObjectName('previewButton')
        preview_btn.clicked.connect(self.preview_custom_data)
        preview_layout.addWidget(preview_btn)
        preview_layout.addStretch()
        
        self.custom_preview = QTextEdit()
        self.custom_preview.setReadOnly(True)
        self.custom_preview.setMaximumHeight(150)
        self.custom_preview.setPlaceholderText('数据预览将在这里显示...')
        self.custom_preview.setObjectName('previewText')
        
        # 时间范围选择
        time_layout = QHBoxLayout()
        start_label = QLabel('开始时间:')
        self.custom_start_date = QDateEdit()
        self.custom_start_date.setDisplayFormat('yyyy-MM-dd')
        self.custom_start_date.setDate(QDate.currentDate().addYears(-1))
        
        end_label = QLabel('结时间:')
        self.custom_end_date = QDateEdit()
        self.custom_end_date.setDisplayFormat('yyyy-MM-dd')
        self.custom_end_date.setDate(QDate.currentDate())
        
        time_layout.addWidget(start_label)
        time_layout.addWidget(self.custom_start_date)
        time_layout.addWidget(end_label)
        time_layout.addWidget(self.custom_end_date)
        
        # 输出格式选择
        format_layout = QHBoxLayout()
        format_label = QLabel('输出格式:')
        self.custom_format_group = QButtonGroup()
        xlsx_radio = QRadioButton('Excel (xlsx)')
        csv_radio = QRadioButton('CSV')
        xlsx_radio.setChecked(True)
        
        self.custom_format_group.addButton(xlsx_radio, 1)
        self.custom_format_group.addButton(csv_radio, 2)
        
        format_layout.addWidget(format_label)
        format_layout.addWidget(xlsx_radio)
        format_layout.addWidget(csv_radio)
        format_layout.addStretch()
        
        # 导出路径选择
        export_layout = QHBoxLayout()
        export_label = QLabel('导出路径:')
        self.custom_export_path = QLineEdit()
        export_btn = QPushButton('选择导出路径')
        
        # 修改导出按钮的连接方式
        def update_export_path():
            file_filter = 'Excel 文件 (*.xlsx)' if xlsx_radio.isChecked() else 'CSV 文件 (*.csv)'
            self.select_export_path(self.custom_export_path, file_filter)
        
        export_btn.clicked.connect(update_export_path)
        
        export_layout.addWidget(export_label)
        export_layout.addWidget(self.custom_export_path)
        export_layout.addWidget(export_btn)
        
        # 状态显示区域
        self.custom_status = QTextEdit()
        self.custom_status.setReadOnly(True)
        self.custom_status.setMaximumHeight(100)
        self.custom_status.setPlaceholderText('执行状态将在这里显示...')
        self.custom_status.setObjectName('statusText')
        
        # 添加进度条
        self.custom_progress = QProgressBar()
        self.custom_progress.setStyleSheet(self.progress_bar_style)
        self.custom_progress.hide()
        
        # 生成按钮
        generate_btn = QPushButton('生成面板')
        generate_btn.setObjectName('generateButton')
        generate_btn.clicked.connect(self.generate_custom_panel)
        generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        # 添加所有组件到布局
        layout.addLayout(freq_layout)
        layout.addLayout(import_layout)
        layout.addLayout(column_layout)
        layout.addLayout(preview_layout)
        layout.addWidget(self.custom_preview)
        layout.addLayout(time_layout)
        layout.addLayout(format_layout)
        layout.addLayout(export_layout)
        layout.addWidget(self.custom_progress)
        layout.addWidget(self.custom_status)
        layout.addWidget(generate_btn)
        layout.addStretch()
        
        return tab

    def select_export_path(self, line_edit, file_filter):
        """选择导出路径"""
        initial_path = os.path.dirname(line_edit.text()) or self.config['last_export_path']
        path = QFileDialog.getSaveFileName(self, '选择保存位置', initial_path, file_filter)[0]
        if path:
            line_edit.setText(path)
            self.config['last_export_path'] = os.path.dirname(path)

    def select_import_file(self):
        """选择导入文件"""
        initial_path = os.path.dirname(self.custom_import_path.text()) or self.config['last_import_path']
        file_path = QFileDialog.getOpenFileName(self, '选择导入文件', initial_path, 'Excel文件 (*.xlsx)')[0]
        if file_path:
            self.custom_import_path.setText(file_path)
            self.config['last_import_path'] = os.path.dirname(file_path)

    def calculate_progress(self, current, total):
        """计算进度百分比"""
        return int((current / total) * 100) if total > 0 else 0

    def update_progress(self, progress_bar, progress):
        """更新进度条"""
        progress_bar.setValue(progress)
        QApplication.processEvents()  # 保持UI响应

    def generate_province_panel(self):
        """生成省份面板的处理函数"""
        try:
            # 获取用户输入
            freq = self.province_freq_combo.currentText()
            start_date = self.province_start_date.date().toPyDate()
            end_date = self.province_end_date.date().toPyDate()
            export_path = self.province_export_path.text()
            
            # 获取选择的输出格式
            is_xlsx = self.province_format_group.checkedId() == 1
            
            # 详细的输入验证
            if not export_path:
                self.province_status.append('错误：请选择导出路径')
                return
            
            # 验证文件扩展名
            if is_xlsx:
                if not export_path.endswith('.xlsx'):
                    export_path += '.xlsx'
            else:
                if not export_path.endswith('.csv'):
                    export_path += '.csv'
            
            if start_date > end_date:
                self.province_status.append('错误：开始时间不能晚于结束时间')
                return
            
            # 验证导出路径的文件夹是否存在且可写
            export_dir = os.path.dirname(export_path)
            if not os.path.exists(export_dir):
                self.province_status.append('错误：导出路径不存在')
                return
            
            if not os.access(export_dir, os.W_OK):
                self.province_status.append('错误：导出路径没有写入权限')
                return
            
            self.province_status.append('开始生成省份面板...')
            
            # 显示进度条
            self.province_progress.setRange(0, 100)
            self.province_progress.setValue(0)
            self.province_progress.show()
            
            try:
                # 生成面板
                panel_generator = DataPanelGenerator()
                df = panel_generator.generate_province_panel(start_date, end_date, freq)
                
                # 根据格式导出
                self.province_progress.setValue(95)
                if is_xlsx:
                    df.to_excel(export_path, index=False)
                else:
                    df.to_csv(export_path, index=False, encoding='utf-8-sig')  # 使用 utf-8-sig 编码支持中文
                self.province_progress.setValue(100)
                
                self.province_status.append(f'面板生成成功！已保存到：{export_path}')
                self.province_status.append(f'共生成 {len(df)} 条记录')
                
            except ValueError as ve:
                self.province_status.append(f'错误：{str(ve)}')
            except PermissionError:
                self.province_status.append('错误：无法写入文件，可能是文件被占用')
            except Exception as e:
                self.province_status.append(f'错误：生成过程中出现异常 - {str(e)}')
                
        except Exception as e:
            self.province_status.append(f'错误：{str(e)}')
        finally:
            # 3秒后隐藏进度条
            QTimer.singleShot(3000, self.province_progress.hide)

    def generate_city_panel(self):
        try:
            # 获取用户输入
            freq = self.city_freq_combo.currentText()
            start_date = self.city_start_date.date().toPyDate()
            end_date = self.city_end_date.date().toPyDate()
            export_path = self.city_export_path.text()
            
            # 验输入
            if not export_path:
                self.city_status.append('错误：请选择导出路径')
                return
            if start_date > end_date:
                self.city_status.append('错误：开始时间不能晚于结束时间')
                return
            
            self.city_status.append('开始生成城市面板...')
            
            # 显示并初始化进度条
            self.city_progress.setRange(0, 100)
            self.city_progress.setValue(0)
            self.city_progress.show()
            
            # 生成面板
            panel_generator = DataPanelGenerator()
            
            # 计算总步骤数
            time_series = panel_generator.generate_time_series(start_date, end_date, freq)
            total_cities = sum(len(cities) for cities in panel_generator.city_data.values())
            total_steps = len(time_series) * total_cities
            current_step = 0
            
            rows = []
            for time in time_series:
                for province, cities in panel_generator.city_data.items():
                    for city in cities:
                        rows.append({
                            '省份': province,
                            '城市': city,
                            '时间': time
                        })
                        current_step += 1
                        progress = int((current_step / total_steps) * 100)
                        self.city_progress.setValue(progress)
                        QApplication.processEvents()  # 保持UI响应
            
            df = pd.DataFrame(rows)
            
            # 获取选择的输出格式
            is_xlsx = self.city_format_group.checkedId() == 1
            
            # 验证文件扩展名
            if is_xlsx and not export_path.endswith('.xlsx'):
                export_path += '.xlsx'
            elif not is_xlsx and not export_path.endswith('.csv'):
                export_path += '.csv'
            
            # 根据格式导出
            if is_xlsx:
                df.to_excel(export_path, index=False)
            else:
                df.to_csv(export_path, index=False, encoding='utf-8-sig')
            
            self.city_progress.setValue(95)
            self.city_progress.setValue(100)
            
            self.city_status.append(f'面板生成成功！已保存到：{export_path}')
            self.city_status.append(f'共生成 {len(df)} 条记录')
            
        except Exception as e:
            self.city_status.append(f'错误：{str(e)}')
        finally:
            # 3秒后隐藏进度条
            QTimer.singleShot(3000, self.city_progress.hide)

    def generate_custom_panel(self):
        try:
            # 获取用户输入
            freq = self.custom_freq_combo.currentText()
            start_date = self.custom_start_date.date().toPyDate()
            end_date = self.custom_end_date.date().toPyDate()
            import_path = self.custom_import_path.text()
            export_path = self.custom_export_path.text()
            column_input = self.custom_column_input.text()
            
            # 验证输入
            if not import_path:
                self.custom_status.append('错误：请选择导入文件')
                return
            if not export_path:
                self.custom_status.append('错误：请选择导出路径')
                return
            if not column_input.isdigit():
                self.custom_status.append('错误：请输入有效的列数')
                return
            if start_date > end_date:
                self.custom_status.append('错误：开始时间不能晚于结束时间')
                return
            
            self.custom_status.append('开始生成自定义面板...')
            
            # 显示并初始化进度条
            self.custom_progress.setRange(0, 100)
            self.custom_progress.setValue(0)
            self.custom_progress.show()
            
            # 创建面板生成器实例
            panel_generator = DataPanelGenerator()
            
            # 读取数据
            self.custom_progress.setValue(10)
            usecols = range(int(column_input))
            input_data = pd.read_excel(import_path, usecols=usecols)
            self.custom_progress.setValue(30)
            
            # 生成时间序列
            time_series = panel_generator.generate_time_series(start_date, end_date, freq)
            total_steps = len(time_series) * len(input_data)
            current_step = 0
            
            rows = []
            for time in time_series:
                for _, row in input_data.iterrows():
                    new_row = row.to_dict()
                    new_row['时间'] = time
                    rows.append(new_row)
                    current_step += 1
                    progress = 30 + int((current_step / total_steps) * 60)  # 30-90%
                    self.custom_progress.setValue(progress)
                    QApplication.processEvents()
            
            df = pd.DataFrame(rows)
            
            # 获取选择的输出格式
            is_xlsx = self.custom_format_group.checkedId() == 1
            
            # 验证文件扩展名
            if is_xlsx and not export_path.endswith('.xlsx'):
                export_path += '.xlsx'
            elif not is_xlsx and not export_path.endswith('.csv'):
                export_path += '.csv'
            
            # 根据格式导出
            if is_xlsx:
                df.to_excel(export_path, index=False)
            else:
                df.to_csv(export_path, index=False, encoding='utf-8-sig')
            
            self.custom_progress.setValue(95)
            self.custom_progress.setValue(100)
            
            self.custom_status.append(f'面板生成成功！已保存到：{export_path}')
            self.custom_status.append(f'共生成 {len(df)} 条记录')
            
        except Exception as e:
            self.custom_status.append(f'错误：{str(e)}')
        finally:
            # 3秒后隐藏进度条
            QTimer.singleShot(3000, self.custom_progress.hide)

    def preview_custom_data(self):
        try:
            import_path = self.custom_import_path.text()
            if not import_path:
                self.custom_preview.setText('错误：请先选择导入文件')
                return
            
            column_input = self.custom_column_input.text()
            if not column_input.isdigit():
                self.custom_preview.setText('错误：请输入有效的列数')
                return
            
            usecols = range(int(column_input))
            df = pd.read_excel(import_path, usecols=usecols)
            
            # 显示前5行数据
            preview_text = "数据预览（前5行）：\n\n"
            preview_text += df.head().to_string()
            preview_text += f"\n\n总行数：{len(df)}"
            self.custom_preview.setText(preview_text)
            
        except Exception as e:
            self.custom_preview.setText(f'错误：{str(e)}')
    
    def show_update_dialog(self, new_version, changelog):
        """显示更新对话框"""
        msg = QMessageBox(self)
        msg.setWindowTitle('发现新版本')
        msg.setText(f'发现新版本 {new_version}\n\n更新内容：\n{changelog}')
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | 
            QMessageBox.StandardButton.No |
            QMessageBox.StandardButton.SaveAll
        )
        msg.button(QMessageBox.StandardButton.Yes).setText('更新并替换')
        msg.button(QMessageBox.StandardButton.SaveAll).setText('保留旧版本并更新')
        msg.button(QMessageBox.StandardButton.No).setText('取消')
        
        reply = msg.exec()
        
        if reply == QMessageBox.StandardButton.Yes:
            self.start_update(keep_old=False)
        elif reply == QMessageBox.StandardButton.SaveAll:
            self.start_update(keep_old=True)
    
    def show_update_error(self, error):
        """显示更新错误"""
        QMessageBox.warning(
            self,
            '更新检查失败',
            f'检查更新时出错：{error}'
        )
    
    def start_update(self, keep_old=False):
        """开始更新"""
        self.progress_dialog = QProgressDialog('正在下载更新...', '取消', 0, 100, self)
        self.progress_dialog.setWindowTitle('更新进度')
        self.progress_dialog.setAutoClose(True)
        self.progress_dialog.setAutoReset(True)
        
        self.updater = Updater(
            "https://github.com/twy93007/Pannel-maker/releases/latest/download/经济数据面板生成器.exe",
            keep_old=keep_old
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
        # 确保完全退出
        QApplication.quit()
    
    def on_update_error(self, error):
        """更新错误"""
        QMessageBox.warning(
            self,
            '更新失败',
            f'更新过程中出错：{error}'
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PanelGenerator()
    window.show()
    sys.exit(app.exec()) 