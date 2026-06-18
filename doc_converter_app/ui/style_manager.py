"""白绿色主题样式管理"""

# 颜色常量
COLORS = {
    "bg_primary": "#F5FBF6",
    "bg_secondary": "#FFFFFF",
    "bg_card": "#FFFFFF",
    "accent": "#4CAF7E",
    "accent_hover": "#3D9E6D",
    "accent_light": "#E8F5ED",
    "text_primary": "#2C3E2C",
    "text_secondary": "#6B7C6B",
    "border": "#D4E8D8",
    "border_focus": "#4CAF7E",
    "success": "#4CAF7E",
    "warning": "#F5A623",
    "error": "#E57373",
}

GLOBAL_QSS = f"""
* {{
    font-family: "Microsoft YaHei", "微软雅黑", "Segoe UI", sans-serif;
    font-size: 10pt;
    color: {COLORS["text_primary"]};
}}

QMainWindow, QWidget#rootWidget {{
    background-color: {COLORS["bg_primary"]};
}}

/* Tab 控件 */
QTabWidget::pane {{
    border: 1px solid {COLORS["border"]};
    border-radius: 8px;
    background: {COLORS["bg_secondary"]};
    top: -1px;
}}

QTabBar::tab {{
    background: {COLORS["bg_primary"]};
    border: 1px solid {COLORS["border"]};
    border-bottom: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    padding: 10px 24px;
    margin-right: 4px;
    color: {COLORS["text_secondary"]};
    font-size: 11pt;
}}

QTabBar::tab:selected {{
    background: {COLORS["accent"]};
    color: white;
    border-color: {COLORS["accent"]};
}}

QTabBar::tab:hover:!selected {{
    background: {COLORS["accent_light"]};
    color: {COLORS["text_primary"]};
}}

/* 普通按钮 */
QPushButton {{
    background-color: {COLORS["accent"]};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 20px;
    font-size: 10pt;
    min-height: 20px;
}}

QPushButton:hover {{
    background-color: {COLORS["accent_hover"]};
}}

QPushButton:pressed {{
    background-color: #357A5A;
}}

QPushButton:disabled {{
    background-color: #B5CFBC;
    color: #E5F0E8;
}}

/* 次要按钮（白色背景） */
QPushButton#secondaryBtn {{
    background-color: {COLORS["bg_secondary"]};
    color: {COLORS["accent"]};
    border: 1px solid {COLORS["accent"]};
}}

QPushButton#secondaryBtn:hover {{
    background-color: {COLORS["accent_light"]};
    border-color: {COLORS["accent_hover"]};
}}

/* 输入框 */
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox {{
    background-color: {COLORS["bg_secondary"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 6px;
    padding: 6px 10px;
    selection-background-color: {COLORS["accent"]};
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus {{
    border: 1px solid {COLORS["border_focus"]};
}}

QComboBox::drop-down {{
    border: none;
    width: 20px;
}}

QComboBox QAbstractItemView {{
    border: 1px solid {COLORS["border"]};
    background-color: {COLORS["bg_secondary"]};
    selection-background-color: {COLORS["accent_light"]};
    selection-color: {COLORS["text_primary"]};
}}

/* 标签 */
QLabel#titleLabel {{
    font-size: 18pt;
    font-weight: bold;
    color: {COLORS["accent"]};
}}

QLabel#subtitleLabel {{
    font-size: 11pt;
    color: {COLORS["text_secondary"]};
}}

QLabel#hintLabel {{
    font-size: 9pt;
    color: {COLORS["text_secondary"]};
}}

/* 卡片容器 */
QFrame#cardFrame {{
    background-color: {COLORS["bg_card"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 10px;
}}

/* 进度条 */
QProgressBar {{
    background-color: {COLORS["accent_light"]};
    border: none;
    border-radius: 6px;
    height: 12px;
    text-align: center;
    color: {COLORS["text_primary"]};
}}

QProgressBar::chunk {{
    background-color: {COLORS["accent"]};
    border-radius: 6px;
}}

/* 列表/表格 */
QListWidget, QTableWidget {{
    background-color: {COLORS["bg_secondary"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 8px;
    padding: 4px;
}}

QListWidget::item, QTableWidget::item {{
    padding: 6px;
    border-bottom: 1px solid {COLORS["border"]};
}}

QListWidget::item:selected, QTableWidget::item:selected {{
    background-color: {COLORS["accent_light"]};
    color: {COLORS["text_primary"]};
}}

QHeaderView::section {{
    background-color: {COLORS["accent_light"]};
    border: none;
    padding: 8px;
    font-weight: bold;
    color: {COLORS["text_primary"]};
}}

/* 滚动条 */
QScrollBar:vertical {{
    background: {COLORS["bg_primary"]};
    width: 10px;
    border-radius: 5px;
}}

QScrollBar::handle:vertical {{
    background: {COLORS["accent"]};
    border-radius: 5px;
    min-height: 24px;
}}

QScrollBar::handle:vertical:hover {{
    background: {COLORS["accent_hover"]};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background: {COLORS["bg_primary"]};
    height: 10px;
    border-radius: 5px;
}}

QScrollBar::handle:horizontal {{
    background: {COLORS["accent"]};
    border-radius: 5px;
    min-width: 24px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {COLORS["accent_hover"]};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}

/* 复选框 */
QCheckBox {{
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1px solid {COLORS["border"]};
    background-color: {COLORS["bg_secondary"]};
}}

QCheckBox::indicator:checked {{
    background-color: {COLORS["accent"]};
    border-color: {COLORS["accent"]};
    image: none;
}}

/* 状态标签 */
QLabel#successLabel {{
    color: {COLORS["success"]};
    font-weight: bold;
}}

QLabel#errorLabel {{
    color: {COLORS["error"]};
    font-weight: bold;
}}

QLabel#warningLabel {{
    color: {COLORS["warning"]};
    font-weight: bold;
}}
"""


def apply_style(app) -> None:
    """将白绿色主题样式应用到 QApplication"""
    app.setStyleSheet(GLOBAL_QSS)
