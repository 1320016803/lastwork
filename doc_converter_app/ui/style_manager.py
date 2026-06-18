"""现代深蓝主题样式管理 — UI优化版本"""

# 颜色常量（深蓝现代配色）
COLORS = {
    "bg_primary": "#F0F2F5",
    "bg_secondary": "#FFFFFF",
    "bg_card": "#FFFFFF",
    "accent": "#4A6CF7",
    "accent_hover": "#3555E8",
    "accent_light": "#EEF1FE",
    "text_primary": "#1E293B",
    "text_secondary": "#64748B",
    "border": "#E2E8F0",
    "border_focus": "#4A6CF7",
    "success": "#10B981",
    "warning": "#F59E0B",
    "error": "#EF4444",
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
    border: 2px solid {COLORS["border"]};
    border-radius: 12px;
    background: {COLORS["bg_secondary"]};
    top: -1px;
    padding-top: 12px;
}}

QTabBar::tab {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {COLORS["bg_secondary"]}, stop:1 #F8FAFC);
    border: 2px solid {COLORS["border"]};
    border-bottom: none;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    padding: 10px 28px;
    margin-right: 6px;
    color: {COLORS["text_secondary"]};
    font-size: 11pt;
    font-weight: 500;
}}

QTabBar::tab:selected {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {COLORS["accent"]}, stop:1 {COLORS["accent_hover"]});
    color: white;
    border-color: {COLORS["accent"]};
    font-weight: bold;
}}

QTabBar::tab:hover:!selected {{
    background: {COLORS["accent_light"]};
    color: {COLORS["text_primary"]};
}}

/* 普通按钮 */
QPushButton {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {COLORS["accent"]}, stop:1 {COLORS["accent_hover"]});
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-size: 10pt;
    font-weight: bold;
    min-height: 22px;
}}

QPushButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #6083FF, stop:1 {COLORS["accent"]});
}}

QPushButton:pressed {{
    background-color: #2D4BD6;
}}

QPushButton:disabled {{
    background-color: #CBD5E1;
    color: #94A3B8;
}}

/* 次要按钮 */
QPushButton#secondaryBtn {{
    background: transparent;
    color: {COLORS["accent"]};
    border: 2px solid {COLORS["accent"]};
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 600;
}}

QPushButton#secondaryBtn:hover {{
    background: {COLORS["accent_light"]};
    border-color: {COLORS["accent_hover"]};
    color: {COLORS["accent_hover"]};
}}

/* 输入框 */
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox {{
    background-color: {COLORS["bg_secondary"]};
    border: 2px solid {COLORS["border"]};
    border-radius: 8px;
    padding: 8px 14px;
    selection-background-color: {COLORS["accent_light"]};
    selection-color: {COLORS["text_primary"]};
    font-size: 10pt;
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus {{
    border: 2px solid {COLORS["accent"]};
    box-shadow: 0 0 8px rgba(74,108,247,0.15);
}}

QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover, QComboBox:hover {{
    border-color: #C7D2FE;
}}

QComboBox::drop-down {{
    border: none;
    width: 24px;
    subcontrol-origin: padding;
    subcontrol-position: center right;
}}

QComboBox::down-arrow {{
    width: 12px;
    height: 12px;
}}

QComboBox QAbstractItemView {{
    border: 2px solid {COLORS["border"]};
    border-radius: 8px;
    background-color: {COLORS["bg_secondary"]};
    selection-background-color: {COLORS["accent_light"]};
    selection-color: {COLORS["text_primary"]};
    padding: 4px;
}}

/* 标签 */
QLabel#titleLabel {{
    font-size: 20pt;
    font-weight: bold;
    color: {COLORS["accent"]};
}}

QLabel#subtitleLabel {{
    font-size: 11pt;
    color: {COLORS["text_secondary"]};
    line-height: 1.4;
}}

QLabel#hintLabel {{
    font-size: 9pt;
    color: {COLORS["text_secondary"]};
}}

/* 卡片容器 */
QFrame#cardFrame {{
    background-color: {COLORS["bg_card"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 12px;
}}

/* 进度条 */
QProgressBar {{
    background-color: {COLORS["accent_light"]};
    border: none;
    border-radius: 10px;
    height: 16px;
    text-align: center;
    color: {COLORS["text_primary"]};
    font-weight: bold;
    font-size: 9pt;
}}

QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {COLORS["accent"]}, stop:1 #7C95FF);
    border-radius: 10px;
}}

/* 列表/表格 */
QListWidget, QTableWidget {{
    background-color: {COLORS["bg_secondary"]};
    border: 2px solid {COLORS["border"]};
    border-radius: 10px;
    padding: 6px;
    outline: none;
}}

QListWidget::item, QTableWidget::item {{
    padding: 8px 10px;
    border-bottom: 1px solid {COLORS["border"]};
    border-radius: 4px;
    margin: 1px 2px;
}}

QListWidget::item:selected, QTableWidget::item:selected {{
    background-color: {COLORS["accent_light"]};
    color: {COLORS["text_primary"]};
    border: 1px solid {COLORS["accent"]};
}}

QListWidget::item:hover:!selected, QTableWidget::item:hover:!selected {{
    background-color: #F8FAFC;
}}

QHeaderView::section {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #F8FAFC, stop:1 #F1F5F9);
    border: none;
    border-bottom: 2px solid {COLORS["border"]};
    padding: 10px;
    font-weight: bold;
    color: {COLORS["text_primary"]};
    font-size: 10pt;
}}

/* 滚动条 */
QScrollBar:vertical {{
    background: {COLORS["bg_primary"]};
    width: 12px;
    border-radius: 6px;
    margin: 2px;
}}

QScrollBar::handle:vertical {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {COLORS["accent"]}, stop:1 #7C95FF);
    border-radius: 6px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: {COLORS["accent_hover"]};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background: {COLORS["bg_primary"]};
    height: 12px;
    border-radius: 6px;
    margin: 2px;
}}

QScrollBar::handle:horizontal {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {COLORS["accent"]}, stop:1 #7C95FF);
    border-radius: 6px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {COLORS["accent_hover"]};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}

/* 复选框 */
QCheckBox {{
    spacing: 10px;
    font-size: 10pt;
}}

QCheckBox::indicator {{
    width: 20px;
    height: 20px;
    border-radius: 6px;
    border: 2px solid {COLORS["border"]};
    background-color: {COLORS["bg_secondary"]};
}}

QCheckBox::indicator:hover {{
    border-color: {COLORS["accent"]};
}}

QCheckBox::indicator:checked {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {COLORS["accent"]}, stop:1 {COLORS["accent_hover"]});
    border-color: {COLORS["accent"]};
    image: url(none);
}}

/* 状态标签 */
QLabel#successLabel {{
    color: {COLORS["success"]};
    font-weight: bold;
    font-size: 10pt;
}}

QLabel#errorLabel {{
    color: {COLORS["error"]};
    font-weight: bold;
    font-size: 10pt;
}}

QLabel#warningLabel {{
    color: {COLORS["warning"]};
    font-weight: bold;
    font-size: 10pt;
}}
"""


def apply_style(app) -> None:
    """将现代深蓝主题样式应用到 QApplication"""
    app.setStyleSheet(GLOBAL_QSS)
