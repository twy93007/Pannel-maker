MODERN_STYLE = """
/* 全局样式 */
QWidget {
    background-color: #f5f6fa;
    color: #2f3542;
    font-family: 'Segoe UI', 'Microsoft YaHei';
    font-size: 14px;
}

/* 卡片样式 */
QFrame#settingsCard, QFrame#customCard {
    background-color: white;
    border-radius: 10px;
    padding: 20px;
    border: 1px solid #dcdde1;
}

/* 标签样式 */
QLabel#settingLabel {
    font-weight: bold;
    min-width: 80px;
}

/* 按钮样式 */
QPushButton {
    background-color: #5352ed;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 8px 15px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #6c5ce7;
}

QPushButton:pressed {
    background-color: #4834d4;
}

QPushButton#generateButton {
    background-color: #2ed573;
    font-size: 16px;
    padding: 12px;
    margin-top: 10px;
}

QPushButton#generateButton:hover {
    background-color: #26de81;
}

/* 下拉框样式 */
QComboBox {
    background-color: white;
    border: 1px solid #dcdde1;
    border-radius: 5px;
    padding: 5px 10px;
    min-width: 120px;
}

QComboBox:drop-down {
    border: none;
    width: 20px;
}

QComboBox:down-arrow {
    image: url(icons/down-arrow.png);
    width: 12px;
    height: 12px;
}

/* 日期选择器样式 */
QDateEdit {
    background-color: white;
    border: 1px solid #dcdde1;
    border-radius: 5px;
    padding: 5px 10px;
    min-width: 120px;
}

QDateEdit::drop-down {
    border: none;
    width: 20px;
}

/* 输入框样式 */
QLineEdit {
    background-color: white;
    border: 1px solid #dcdde1;
    border-radius: 5px;
    padding: 8px;
}

QLineEdit:focus {
    border: 2px solid #5352ed;
}

/* 进度条样式 */
QProgressBar {
    background-color: #f1f2f6;
    border: none;
    border-radius: 5px;
    text-align: center;
    height: 10px;
}

QProgressBar::chunk {
    background-color: #2ed573;
    border-radius: 5px;
}

/* 表格样式 */
QTableWidget {
    background-color: white;
    border: 1px solid #dcdde1;
    border-radius: 5px;
    gridline-color: #f1f2f6;
}

QTableWidget::item {
    padding: 5px;
}

QTableWidget::item:selected {
    background-color: #5352ed;
    color: white;
}

QHeaderView::section {
    background-color: #f5f6fa;
    color: #2f3542;
    padding: 8px;
    border: none;
    border-right: 1px solid #dcdde1;
    border-bottom: 1px solid #dcdde1;
    font-weight: bold;
}

/* 滚动条样式 */
QScrollBar:vertical {
    border: none;
    background-color: #f1f2f6;
    width: 8px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: #dcdde1;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #a4b0be;
}
""" 