from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFileDialog, QComboBox, QLineEdit,
                            QTableWidget, QTableWidgetItem, QMessageBox,
                            QProgressBar, QGroupBox, QFrame, QDateEdit)
from PyQt6.QtCore import Qt, QSettings, QDate
from PyQt6.QtGui import QIcon, QFont
import pandas as pd
import os
from styles import MODERN_STYLE
from base_data import PROVINCES, CITIES
from datetime import datetime

class PanelTab(QWidget):
    def __init__(self, panel_type="province"):
        super().__init__()
        self.panel_type = panel_type
        self.data = None
        self.settings = QSettings('PanelMaker', 'EconomicPanel')
        self.setup_ui()
        
    def setup_ui(self):
        # 应用全局样式
        self.setStyleSheet(MODERN_STYLE)
        
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 创建设置卡片
        settings_card = QFrame()
        settings_card.setObjectName("settingsCard")
        card_layout = QVBoxLayout(settings_card)
        
        # 时间频次选择，默认设置为"年"
        freq_layout = QHBoxLayout()
        freq_label = QLabel("时间频次")
        freq_label.setObjectName("settingLabel")
        self.freq_combo = QComboBox()
        self.freq_combo.addItems(["年", "季度", "月", "周", "日"])
        self.freq_combo.setCurrentText("年")  # 设置默认值为"年"
        self.freq_combo.currentTextChanged.connect(self.on_freq_changed)
        freq_layout.addWidget(freq_label)
        freq_layout.addWidget(self.freq_combo)
        card_layout.addLayout(freq_layout)
        
        # 时间选择区域
        time_layout = QHBoxLayout()
        time_label = QLabel("时间范围")
        time_label.setObjectName("settingLabel")
        
        # 创建开始时间和结束时间的布局
        self.start_time_layout = QHBoxLayout()
        self.end_time_layout = QHBoxLayout()
        
        # 初始化时间选择器
        self.init_time_selectors()
        
        time_layout.addWidget(time_label)
        time_layout.addLayout(self.start_time_layout)
        time_layout.addWidget(QLabel("至"))
        time_layout.addLayout(self.end_time_layout)
        card_layout.addLayout(time_layout)
        
        # 连接频次改变信号
        self.freq_combo.currentTextChanged.connect(self.on_freq_changed)
        
        # 输出格式选择
        format_layout = QHBoxLayout()
        format_label = QLabel("输出格式")
        format_label.setObjectName("settingLabel")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["Excel", "CSV"])
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        card_layout.addLayout(format_layout)
        
        # 输出路径选择
        path_layout = QHBoxLayout()
        path_label = QLabel("输出路径")
        path_label.setObjectName("settingLabel")
        self.path_input = QLineEdit()
        self.path_input.setReadOnly(True)
        self.path_input.setPlaceholderText("选择保存位置...")
        self.browse_btn = QPushButton("浏览")
        self.browse_btn.clicked.connect(self.select_save_path)
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.browse_btn)
        card_layout.addLayout(path_layout)
        
        main_layout.addWidget(settings_card)
        
        # 自定义面板特有设置
        if self.panel_type == "custom":
            custom_card = QFrame()
            custom_card.setObjectName("customCard")
            custom_layout = QVBoxLayout(custom_card)
            
            # 文件选择和列数输入
            file_layout = QHBoxLayout()
            self.file_btn = QPushButton("导入Excel")
            self.file_btn.clicked.connect(self.select_file)
            
            self.col_input = QLineEdit()
            self.col_input.setPlaceholderText("列数")
            
            self.preview_btn = QPushButton("预览")
            self.preview_btn.clicked.connect(self.preview_data)
            
            file_layout.addWidget(self.file_btn)
            file_layout.addWidget(self.col_input)
            file_layout.addWidget(self.preview_btn)
            custom_layout.addLayout(file_layout)
            
            # 预览表格
            self.table = QTableWidget()
            custom_layout.addWidget(self.table)
            
            main_layout.addWidget(custom_card)
        
        # 进度条
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setTextVisible(True)
        self.progress.setFormat("%p%")
        main_layout.addWidget(self.progress)
        
        # 生成按钮
        self.generate_btn = QPushButton("生成面板")
        self.generate_btn.setObjectName("generateButton")
        self.generate_btn.clicked.connect(self.generate_panel)
        main_layout.addWidget(self.generate_btn)
        
        self.setLayout(main_layout)
    
    def init_time_selectors(self):
        """初始化时间选择器"""
        current_year = QDate.currentDate().year()
        
        # 创建年份选择器
        self.start_year = QComboBox()
        self.end_year = QComboBox()
        years = [str(year) for year in range(2000, current_year + 2)]
        self.start_year.addItems(years)
        self.end_year.addItems(years)
        self.start_year.setCurrentText(str(current_year - 1))
        self.end_year.setCurrentText(str(current_year))
        
        # 创建季度选择器
        self.start_quarter = QComboBox()
        self.end_quarter = QComboBox()
        quarters = ["Q1", "Q2", "Q3", "Q4"]
        self.start_quarter.addItems(quarters)
        self.end_quarter.addItems(quarters)
        
        # 创建月份选择器
        self.start_month = QComboBox()
        self.end_month = QComboBox()
        months = [f"{i:02d}" for i in range(1, 13)]
        self.start_month.addItems(months)
        self.end_month.addItems(months)
        
        # 创建周选择器
        self.start_week = QComboBox()
        self.end_week = QComboBox()
        weeks = [f"W{i:02d}" for i in range(1, 54)]
        self.start_week.addItems(weeks)
        self.end_week.addItems(weeks)
        
        # 创建日期选择器
        self.start_date = QDateEdit()
        self.end_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.end_date.setCalendarPopup(True)
        self.start_date.setDate(QDate(current_year - 1, 1, 1))
        self.end_date.setDate(QDate(current_year, 1, 1))
        
        # 存储所有选择器的引用
        self.time_selectors = {
            'start_year': self.start_year,
            'end_year': self.end_year,
            'start_quarter': self.start_quarter,
            'end_quarter': self.end_quarter,
            'start_month': self.start_month,
            'end_month': self.end_month,
            'start_week': self.start_week,
            'end_week': self.end_week,
            'start_date': self.start_date,
            'end_date': self.end_date
        }
        
        # 初始显示年份选择器
        self.update_time_selectors("年")
    
    def update_time_selectors(self, freq):
        """根据频次更新时间选择器"""
        # 先隐藏所有选择器
        for selector in self.time_selectors.values():
            selector.hide()
        
        # 清空布局
        self.clear_layout(self.start_time_layout)
        self.clear_layout(self.end_time_layout)
        
        # 根据频次显示相应的选择器
        if freq == "年":
            self.start_year.show()
            self.end_year.show()
            self.start_time_layout.addWidget(self.start_year)
            self.end_time_layout.addWidget(self.end_year)
        
        elif freq == "季度":
            self.start_year.show()
            self.start_quarter.show()
            self.end_year.show()
            self.end_quarter.show()
            self.start_time_layout.addWidget(self.start_year)
            self.start_time_layout.addWidget(self.start_quarter)
            self.end_time_layout.addWidget(self.end_year)
            self.end_time_layout.addWidget(self.end_quarter)
        
        elif freq == "月":
            self.start_year.show()
            self.start_month.show()
            self.end_year.show()
            self.end_month.show()
            self.start_time_layout.addWidget(self.start_year)
            self.start_time_layout.addWidget(self.start_month)
            self.end_time_layout.addWidget(self.end_year)
            self.end_time_layout.addWidget(self.end_month)
        
        elif freq == "周":
            self.start_year.show()
            self.start_week.show()
            self.end_year.show()
            self.end_week.show()
            self.start_time_layout.addWidget(self.start_year)
            self.start_time_layout.addWidget(self.start_week)
            self.end_time_layout.addWidget(self.end_year)
            self.end_time_layout.addWidget(self.end_week)
        
        else:  # 日
            self.start_date.show()
            self.end_date.show()
            self.start_time_layout.addWidget(self.start_date)
            self.end_time_layout.addWidget(self.end_date)
    
    def clear_layout(self, layout):
        """清空布局中的所有部件"""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
    
    def on_freq_changed(self, freq):
        """频次改变时的处理"""
        self.update_time_selectors(freq)
    
    def select_save_path(self):
        """选择保存路径"""
        last_dir = self.settings.value('last_directory', '')
        file_format = ".xlsx" if self.format_combo.currentText() == "Excel" else ".csv"
        
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "选择保存位置",
            os.path.join(last_dir, f"面板数据{file_format}"),
            "Excel Files (*.xlsx);;CSV Files (*.csv)" if file_format == ".xlsx" else "CSV Files (*.csv)"
        )
        
        if file_name:
            self.settings.setValue('last_directory', os.path.dirname(file_name))
            self.path_input.setText(file_name)
    
    def select_file(self):
        """选择数据文件"""
        last_dir = self.settings.value('last_directory', '')
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "选择Excel文件",
            last_dir,
            "Excel Files (*.xlsx)"
        )
        
        if file_name:
            self.settings.setValue('last_directory', os.path.dirname(file_name))
            try:
                self.data = pd.read_excel(file_name)
                self.file_btn.setText(os.path.basename(file_name))
            except Exception as e:
                QMessageBox.warning(self, "错误", f"读取文件失败：{str(e)}")
    
    def preview_data(self):
        """预览数据"""
        if self.data is None:
            QMessageBox.warning(self, "错误", "请先导入Excel文件")
            return
            
        try:
            cols = int(self.col_input.text())
            if cols <= 0 or cols > len(self.data.columns):
                raise ValueError("列数无效")
                
            self.table.setRowCount(min(10, len(self.data)))
            self.table.setColumnCount(cols)
            self.table.setHorizontalHeaderLabels(self.data.columns[:cols])
            
            for i in range(min(10, len(self.data))):
                for j in range(cols):
                    item = QTableWidgetItem(str(self.data.iloc[i, j]))
                    self.table.setItem(i, j, item)
                    
        except ValueError as e:
            QMessageBox.warning(self, "错误", str(e))
        except Exception as e:
            QMessageBox.warning(self, "错误", f"预览数据失败：{str(e)}")

    def validate_time_format(self, time_str):
        """验证时间格式"""
        freq = self.freq_combo.currentText()
        try:
            if freq == "年":
                return len(time_str) == 4 and time_str.isdigit()
            elif freq == "季度":
                year, quarter = time_str.split('-Q')
                return len(year) == 4 and year.isdigit() and quarter in ['1', '2', '3', '4']
            elif freq == "月":
                year, month = time_str.split('-')
                return len(year) == 4 and year.isdigit() and 1 <= int(month) <= 12
            elif freq == "周":
                year, week = time_str.split('-W')
                return len(year) == 4 and year.isdigit() and 1 <= int(week) <= 53
            elif freq == "日":
                pd.to_datetime(time_str)
                return True
        except:
            return False
    
    def get_time_str(self):
        """获取当前选择的时间字符串"""
        freq = self.freq_combo.currentText()
        
        if freq == "年":
            start_time = self.start_year.currentText()
            end_time = self.end_year.currentText()
        
        elif freq == "季度":
            start_time = f"{self.start_year.currentText()}-{self.start_quarter.currentText()}"
            end_time = f"{self.end_year.currentText()}-{self.end_quarter.currentText()}"
        
        elif freq == "月":
            start_time = f"{self.start_year.currentText()}-{self.start_month.currentText()}"
            end_time = f"{self.end_year.currentText()}-{self.end_month.currentText()}"
        
        elif freq == "周":
            start_time = f"{self.start_year.currentText()}-{self.start_week.currentText()}"
            end_time = f"{self.end_year.currentText()}-{self.end_week.currentText()}"
        
        else:  # 日
            start_time = self.start_date.date().toString("yyyy-MM-dd")
            end_time = self.end_date.date().toString("yyyy-MM-dd")
        
        return start_time, end_time
    
    def validate_input(self):
        """验证输入数据"""
        # 获取格式化的时间字符串
        start_time, end_time = self.get_time_str()
        
        # 验证时间格式
        if not self.validate_time_format(start_time):
            QMessageBox.warning(self, "错误", "开始时间格式不正确")
            return False
            
        if not self.validate_time_format(end_time):
            QMessageBox.warning(self, "错误", "结束时间格式不正确")
            return False
            
        # 验证时间范围
        if self.start_date.date() > self.end_date.date():
            QMessageBox.warning(self, "错误", "开始时间不能晚于结束时间")
            return False
            
        # 验证输出路径
        if not self.path_input.text():
            QMessageBox.warning(self, "错误", "请选择输出路径")
            return False
            
        # 验证自定义面板的特殊要求
        if self.panel_type == "custom":
            if self.data is None:
                QMessageBox.warning(self, "错误", "请先导入Excel文件")
                return False
                
            try:
                cols = int(self.col_input.text())
                if cols <= 0 or cols > len(self.data.columns):
                    QMessageBox.warning(self, "错误", "列数无效")
                    return False
            except ValueError:
                QMessageBox.warning(self, "错误", "请输入有效的列数")
                return False
                
        return True
    
    def generate_panel(self):
        """生成面板数据"""
        # 验证输入
        if not self.validate_input():
            return
            
        # 显示进度条
        self.progress.setVisible(True)
        self.progress.setValue(0)
        
        try:
            # 根据面板类型处理数据
            if self.panel_type == "province":
                self.generate_province_panel()
            elif self.panel_type == "city":
                self.generate_city_panel()
            else:
                self.generate_custom_panel()
                
        except Exception as e:
            QMessageBox.warning(self, "错误", f"生成面板失败：{str(e)}")
        finally:
            self.progress.setVisible(False)
    
    def get_save_path(self):
        """获取保存路径"""
        last_dir = self.settings.value('last_directory', '')
        file_format = ".xlsx" if self.format_combo.currentText() == "Excel" else ".csv"
        
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "保存文件",
            os.path.join(last_dir, f"面板数据{file_format}"),
            "Excel Files (*.xlsx);;CSV Files (*.csv)" if file_format == ".xlsx" else "CSV Files (*.csv);;Excel Files (*.xlsx)"
        )
        
        if file_name:
            self.settings.setValue('last_directory', os.path.dirname(file_name))
            return file_name
        return None
    
    def get_time_range(self):
        """获取时间范围"""
        freq = self.freq_combo.currentText()
        
        if freq == "年":
            start_year = int(self.start_year.currentText())
            end_year = int(self.end_year.currentText())
            return [str(year) for year in range(start_year, end_year + 1)]
        
        elif freq == "季度":
            # 构建完整的季度范围
            start_year = int(self.start_year.currentText())
            start_q = int(self.start_quarter.currentText().replace('Q', ''))
            end_year = int(self.end_year.currentText())
            end_q = int(self.end_quarter.currentText().replace('Q', ''))
            
            # 使用pandas生成日期范围，然后转换为季度格式
            dates = pd.date_range(
                start=f"{start_year}-{(start_q-1)*3 + 1}-01",
                end=f"{end_year}-{end_q*3}-01",
                freq='Q',
                inclusive='both'
            )
            return [f"{d.year}-Q{(d.month-1)//3 + 1}" for d in dates]
        
        elif freq == "月":
            # 构建完整的月份范围
            start_year = int(self.start_year.currentText())
            start_month = int(self.start_month.currentText())
            end_year = int(self.end_year.currentText())
            end_month = int(self.end_month.currentText())
            
            # 使用pandas生成日期范围
            dates = pd.date_range(
                start=pd.Timestamp(f"{start_year}-{start_month:02d}-01"),
                end=pd.Timestamp(f"{end_year}-{end_month:02d}-01"),
                freq='MS',  # 月初
                inclusive='both'  # 包含开始和结束日期
            )
            return [d.strftime("%Y-%m") for d in dates]
        
        elif freq == "周":
            # 构建完整的周范围
            start_year = int(self.start_year.currentText())
            start_week = int(self.start_week.currentText().replace('W', ''))
            end_year = int(self.end_year.currentText())
            end_week = int(self.end_week.currentText().replace('W', ''))
            
            # 转换为日期
            start_date = datetime.strptime(f"{start_year}-W{start_week:02d}-1", "%Y-W%W-%w")
            # 对于结束周，我们使用周日作为结束日期
            end_date = datetime.strptime(f"{end_year}-W{end_week:02d}-0", "%Y-W%W-%w")
            
            # 使用pandas生成日期范围
            dates = pd.date_range(
                start=start_date,
                end=end_date,
                freq='W-MON',  # 每周一
                inclusive='both'
            )
            return [f"{d.year}-W{d.isocalendar()[1]:02d}" for d in dates]
        
        else:  # 日
            # 使用pandas生成日期范围
            dates = pd.date_range(
                start=self.start_date.date().toPyDate(),
                end=self.end_date.date().toPyDate(),
                freq='D',
                inclusive='both'
            )
            return [d.strftime("%Y-%m-%d") for d in dates]
    
    def generate_province_panel(self):
        """生成省份面板"""
        save_path = self.path_input.text()
        if not save_path:
            return
        
        try:
            # 获取时间范围（包含结束时间）
            time_range = self.get_time_range()
            
            # 创建数据框架
            data = []
            total_steps = len(PROVINCES) * len(time_range)
            current_step = 0
            
            for province, abbr in PROVINCES.items():
                for time in time_range:
                    data.append({
                        "省份": province,
                        "简称": abbr,
                        "时间": time
                    })
                    current_step += 1
                    self.progress.setValue(int(current_step * 100 / total_steps))
            
            df = pd.DataFrame(data)
            
            # 保存数据
            if save_path.endswith('.xlsx'):
                df.to_excel(save_path, index=False)
            else:
                df.to_csv(save_path, index=False, encoding='utf-8-sig')
                
            QMessageBox.information(self, "成功", "面板生成成功！")
            
        except Exception as e:
            QMessageBox.warning(self, "错误", f"保存文件失败：{str(e)}")
    
    def generate_city_panel(self):
        """生成城市面板"""
        save_path = self.path_input.text()
        if not save_path:
            return
        
        try:
            # 获取时间范围（包含结束时间）
            time_range = self.get_time_range()
            
            # 创建数据框架
            data = []
            total_steps = sum(len(cities) for cities in CITIES.values()) * len(time_range)
            current_step = 0
            
            for province, city_list in CITIES.items():
                for city in city_list:
                    for time in time_range:
                        data.append({
                            "省份": province,
                            "城市": city,
                            "时间": time
                        })
                        current_step += 1
                        self.progress.setValue(int(current_step * 100 / total_steps))
            
            df = pd.DataFrame(data)
            
            # 保存数据
            if save_path.endswith('.xlsx'):
                df.to_excel(save_path, index=False)
            else:
                df.to_csv(save_path, index=False, encoding='utf-8-sig')
                
            QMessageBox.information(self, "成功", "面板生成成功！")
            
        except Exception as e:
            QMessageBox.warning(self, "错误", f"保存文件失败：{str(e)}")
    
    def generate_custom_panel(self):
        """生成自定义面板"""
        if self.data is None:
            QMessageBox.warning(self, "错误", "请先导入Excel文件")
            return
        
        save_path = self.path_input.text()
        if not save_path:
            return
        
        try:
            cols = int(self.col_input.text())
            selected_data = self.data.iloc[:, :cols]
            
            # 获取完整的时间范围
            time_range = self.get_time_range()
            
            # 创建数据框架
            final_data = []
            total_steps = len(time_range)
            
            # 为每个时间点复制数据
            for i, time in enumerate(time_range):
                temp_data = selected_data.copy()
                temp_data['时间'] = time
                final_data.append(temp_data)
                self.progress.setValue(int((i + 1) * 100 / total_steps))
            
            # 合并所有数据
            result = pd.concat(final_data, ignore_index=True)
            
            # 调整列顺序，确保时间列在前面
            cols = ['时间'] + [col for col in result.columns if col != '时间']
            result = result[cols]
            
            # 保存数据
            if save_path.endswith('.xlsx'):
                result.to_excel(save_path, index=False)
            else:
                result.to_csv(save_path, index=False, encoding='utf-8-sig')
                
            QMessageBox.information(self, "成功", "面板生成成功！")
            
        except ValueError as e:
            QMessageBox.warning(self, "错误", "请输入有效的列数")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"生成面板失败：{str(e)}")
    
    def get_freq_str(self):
        """获取时间频率字符串"""
        freq_map = {
            "年": "Y",
            "季度": "Q",
            "月": "M",
            "周": "W",
            "日": "D"
        }
        return freq_map[self.freq_combo.currentText()]
    
    def get_time_format(self):
        """获取时间格式字符串"""
        format_map = {
            "年": "%Y",
            "季度": "%Y-Q%q",
            "月": "%Y-%m",
            "周": "%Y-W%W",
            "日": "%Y-%m-%d"
        }
        return format_map[self.freq_combo.currentText()]
    
    def export_data(self):
        """导出数据"""
        if self.data is None:
            QMessageBox.warning(self, "错误", "没有可导出的数据")
            return
            
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "导出数据",
            "",
            "Excel Files (*.xlsx);;CSV Files (*.csv)"
        )
        
        if file_name:
            try:
                if file_name.endswith('.xlsx'):
                    self.data.to_excel(file_name, index=False)
                else:
                    self.data.to_csv(file_name, index=False)
                QMessageBox.information(self, "成功", "数据导出成功")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"导出数据失败：{str(e)}") 