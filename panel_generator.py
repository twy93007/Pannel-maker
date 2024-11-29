from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFileDialog, QComboBox, QSpinBox,
                            QTableWidget, QTableWidgetItem, QMessageBox)
from PyQt6.QtCore import Qt
import pandas as pd
import os

class PanelTab(QWidget):
    def __init__(self, panel_type="province"):
        super().__init__()
        self.panel_type = panel_type
        self.data = None
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # 顶部控制区
        control_layout = QHBoxLayout()
        
        # 文件选择
        self.file_btn = QPushButton("选择数据文件")
        self.file_btn.clicked.connect(self.select_file)
        control_layout.addWidget(self.file_btn)
        
        # 年份选择
        year_layout = QHBoxLayout()
        year_layout.addWidget(QLabel("年份:"))
        self.year_spin = QSpinBox()
        self.year_spin.setRange(1990, 2100)
        self.year_spin.setValue(2024)
        year_layout.addWidget(self.year_spin)
        control_layout.addLayout(year_layout)
        
        # 地区选择
        if self.panel_type in ["province", "city"]:
            region_layout = QHBoxLayout()
            region_layout.addWidget(QLabel("地区:"))
            self.region_combo = QComboBox()
            self.update_region_list()
            region_layout.addWidget(self.region_combo)
            control_layout.addLayout(region_layout)
        
        # 生成按钮
        self.generate_btn = QPushButton("生成面板")
        self.generate_btn.clicked.connect(self.generate_panel)
        control_layout.addWidget(self.generate_btn)
        
        # 导出按钮
        self.export_btn = QPushButton("导出数据")
        self.export_btn.clicked.connect(self.export_data)
        control_layout.addWidget(self.export_btn)
        
        layout.addLayout(control_layout)
        
        # 数据预览表格
        self.table = QTableWidget()
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def update_region_list(self):
        """更新地区列表"""
        if not hasattr(self, 'region_combo'):
            return
            
        if self.panel_type == "province":
            regions = [
                "北京", "天津", "河北", "山西", "内蒙古",
                "辽宁", "吉林", "黑龙江", "上海", "江苏",
                "浙江", "安徽", "福建", "江西", "山东",
                "河南", "湖北", "湖南", "广东", "广西",
                "海南", "重庆", "四川", "贵州", "云南",
                "西藏", "陕西", "甘肃", "青海", "宁夏",
                "新疆"
            ]
        elif self.panel_type == "city":
            # 这里可以根据选择的省份动态加载城市列表
            regions = ["示例城市1", "示例城市2", "示例城市3"]
        
        self.region_combo.clear()
        self.region_combo.addItems(regions)
    
    def select_file(self):
        """选择数据文件"""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "选择数据文件",
            "",
            "Excel Files (*.xlsx *.xls);;CSV Files (*.csv)"
        )
        
        if file_name:
            try:
                if file_name.endswith(('.xlsx', '.xls')):
                    self.data = pd.read_excel(file_name)
                else:
                    self.data = pd.read_csv(file_name)
                self.update_table()
                self.file_btn.setText(os.path.basename(file_name))
            except Exception as e:
                QMessageBox.warning(self, "错误", f"读取文件失败：{str(e)}")
    
    def update_table(self):
        """更新数据预览表格"""
        if self.data is None:
            return
            
        self.table.setRowCount(len(self.data))
        self.table.setColumnCount(len(self.data.columns))
        self.table.setHorizontalHeaderLabels(self.data.columns)
        
        for i in range(len(self.data)):
            for j in range(len(self.data.columns)):
                item = QTableWidgetItem(str(self.data.iloc[i, j]))
                self.table.setItem(i, j, item)
    
    def generate_panel(self):
        """生成面板数据"""
        if self.data is None:
            QMessageBox.warning(self, "错误", "请先选择数据文件")
            return
            
        try:
            # 根据面板类型处理数据
            if self.panel_type == "province":
                region = self.region_combo.currentText()
                year = self.year_spin.value()
                # 处理省份数据
                filtered_data = self.data[
                    (self.data['省份'] == region) &
                    (self.data['年份'] == year)
                ]
            elif self.panel_type == "city":
                region = self.region_combo.currentText()
                year = self.year_spin.value()
                # 处理城市数据
                filtered_data = self.data[
                    (self.data['城市'] == region) &
                    (self.data['年份'] == year)
                ]
            else:
                # 处理自定义面板
                filtered_data = self.data
            
            # 更新表格显示
            self.data = filtered_data
            self.update_table()
            
        except Exception as e:
            QMessageBox.warning(self, "错误", f"生成面板失败：{str(e)}")
    
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