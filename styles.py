MAIN_STYLE = """
QMainWindow {
    background-color: #f5f6fa;
}

QWidget {
    font-family: "Microsoft YaHei", Arial;
    font-size: 14px;
}

QLabel {
    color: #2c3e50;
    font-weight: bold;
}

QTabWidget::pane {
    border: 1px solid #dcdde1;
    background: white;
    border-radius: 4px;
}

QTabWidget::tab-bar {
    left: 5px;
}

QTabBar::tab {
    background: #f1f2f6;
    border: 1px solid #dcdde1;
    padding: 10px 15px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    color: #2f3542;
    font-weight: bold;
}

QTabBar::tab:hover {
    background: #dfe4ea;
}

QTabBar::tab:selected {
    background: #3498db;
    color: white;
    border-bottom-color: #3498db;
}

QLineEdit {
    padding: 8px;
    border: 2px solid #dcdde1;
    border-radius: 4px;
    background: white;
    selection-background-color: #3498db;
    color: black;
}

QLineEdit:focus {
    border-color: #3498db;
}

QLineEdit:disabled {
    background: #f1f2f6;
}

QComboBox {
    padding: 8px;
    border: 2px solid #dcdde1;
    border-radius: 4px;
    background: white;
    min-width: 100px;
    color: black;
}

QComboBox:hover {
    border-color: #3498db;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: url(down_arrow.png);  /* 需要准备一个下拉箭头图标 */
    width: 12px;
    height: 12px;
}

QPushButton {
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
    min-width: 80px;
}

/* 普通按钮样式 */
QPushButton {
    background-color: #3498db;
    color: white;
    border: none;
}

QPushButton:hover {
    background-color: #2980b9;
}

QPushButton:pressed {
    background-color: #2475a7;
}

/* 生成按钮特殊样式 */
QPushButton#generateButton {
    background-color: #2ecc71;
    font-size: 15px;
    padding: 10px 20px;
}

QPushButton#generateButton:hover {
    background-color: #27ae60;
}

QPushButton#generateButton:pressed {
    background-color: #219a52;
}

/* 预览按钮样式 */
QPushButton#previewButton {
    background-color: #9b59b6;
}

QPushButton#previewButton:hover {
    background-color: #8e44ad;
}

QProgressBar {
    border: 2px solid #dcdde1;
    border-radius: 5px;
    text-align: center;
    background-color: #f5f6fa;
    height: 20px;
    color: #2c3e50;
    font-weight: bold;
}

QProgressBar::chunk {
    background-color: #2ecc71;
    border-radius: 3px;
}

QTextEdit {
    border: 2px solid #dcdde1;
    border-radius: 4px;
    background: white;
    padding: 8px;
    selection-background-color: #3498db;
    color: black;
}

QTextEdit:focus {
    border-color: #3498db;
}

QRadioButton {
    spacing: 8px;
    color: #2c3e50;
}

QRadioButton::indicator {
    width: 16px;
    height: 16px;
}

QRadioButton::indicator:unchecked {
    background-color: white;
    border: 2px solid #dcdde1;
    border-radius: 8px;
}

QRadioButton::indicator:checked {
    background-color: #3498db;
    border: 2px solid #3498db;
    border-radius: 8px;
}

QRadioButton::indicator:unchecked:hover {
    border-color: #3498db;
}

/* 日期编辑器样式 */
QDateEdit {
    padding: 8px;
    border: 2px solid #dcdde1;
    border-radius: 4px;
    background: white;
    color: black;
}

QDateEdit:hover {
    border-color: #3498db;
}

QDateEdit::drop-down {
    border: none;
    width: 20px;
}

/* 状态文本框特殊样式 */
QTextEdit#statusText {
    background-color: #f8f9fa;
    border: 2px solid #e9ecef;
    color: black;
    font-family: Consolas, Monaco, monospace;
}

/* 预览文本框特殊样式 */
QTextEdit#previewText {
    font-family: Consolas, Monaco, monospace;
    line-height: 1.4;
    color: black;
}
""" 