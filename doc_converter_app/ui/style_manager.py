"""现代深蓝主题样式管理 — UI v2（卡片式 / 分级按钮 / 更大留白）"""

# 颜色常量
COLORS = {
    "bg_primary":    "#F0F2F5",
    "bg_secondary":  "#FFFFFF",
    "bg_card":       "#FFFFFF",
    "accent":        "#4A6CF7",
    "accent_hover":  "#3555E8",
    "accent_light":  "#EEF1FE",
    "text_primary":  "#1E293B",
    "text_secondary":"#94A3B8",   # 更浅的灰，主次分明
    "border":        "#E2E8F0",
    "success":       "#10B981",
    "warning":       "#F59E0B",
    "error":         "#EF4444",
}

GLOBAL_QSS = f"""
/* ── 全局基础 ─────────────────────────────────── */
* {{
    font-family: "Microsoft YaHei", "微软雅黑", "Segoe UI", sans-serif;
    font-size: 10pt;
    color: {COLORS["text_primary"]};
}}

QMainWindow, QWidget#rootWidget {{
    background-color: {COLORS["bg_primary"]};
}}

/* ── Tab 控件 ──────────────────────────────────── */
QTabWidget::pane {{
    border: 1.5px solid {COLORS["border"]};
    border-radius: 12px;
    background: {COLORS["bg_primary"]};
    top: -1px;
    padding-top: 10px;
}}

QTabBar::tab {{
    background: {COLORS["bg_secondary"]};
    border: 1.5px solid {COLORS["border"]};
    border-bottom: none;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    padding: 10px 30px;
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

/* ── 卡片容器 ──────────────────────────────────── */
QFrame#cardFrame {{
    background-color: {COLORS["bg_card"]};
    border: 1.5px solid {COLORS["border"]};
    border-radius: 14px;
}}

/* ── 主要按钮（填充样式，更大） ─────────────────── */
QPushButton {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {COLORS["accent"]}, stop:1 {COLORS["accent_hover"]});
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 28px;
    font-size: 10pt;
    font-weight: bold;
    min-height: 38px;
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

/* ── 次要按钮（描边样式） ─────────────────────── */
QPushButton#secondaryBtn {{
    background: transparent;
    color: {COLORS["accent"]};
    border: 2px solid {COLORS["accent"]};
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 600;
    min-height: 34px;
}}

QPushButton#secondaryBtn:hover {{
    background: {COLORS["accent_light"]};
    border-color: {COLORS["accent_hover"]};
    color: {COLORS["accent_hover"]};
}}

QPushButton#secondaryBtn:disabled {{
    background: transparent;
    border-color: #CBD5E1;
    color: #CBD5E1;
}}

/* ── 眼睛图标按钮 ─────────────────────────────── */
QPushButton#eyeBtn {{
    background: transparent;
    border: 1.5px solid {COLORS["border"]};
    border-radius: 8px;
    color: {COLORS["text_secondary"]};
    padding: 0px;
    min-width: 38px;
    min-height: 38px;
    font-size: 15pt;
}}

QPushButton#eyeBtn:hover {{
    background: {COLORS["accent_light"]};
    border-color: {COLORS["accent"]};
    color: {COLORS["accent"]};
}}

/* ── 输入框（加高至 38px） ─────────────────────── */
QLineEdit, QTextEdit, QPlainTextEdit {{
    background-color: {COLORS["bg_secondary"]};
    border: 1.5px solid {COLORS["border"]};
    border-radius: 8px;
    padding: 8px 14px;
    selection-background-color: {COLORS["accent_light"]};
    selection-color: {COLORS["text_primary"]};
    font-size: 10pt;
    min-height: 38px;
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border: 2px solid {COLORS["accent"]};
}}

QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover {{
    border-color: #C7D2FE;
}}

/* ── 下拉框 ───────────────────────────────────── */
QComboBox {{
    background-color: {COLORS["bg_secondary"]};
    border: 1.5px solid {COLORS["border"]};
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 10pt;
    min-height: 38px;
    color: {COLORS["text_primary"]};
}}

QComboBox:focus {{
    border: 2px solid {COLORS["accent"]};
}}

QComboBox:hover {{
    border-color: #C7D2FE;
}}

QComboBox::drop-down {{
    border: none;
    width: 28px;
    subcontrol-origin: padding;
    subcontrol-position: center right;
}}

QComboBox::down-arrow {{
    width: 14px;
    height: 14px;
}}

QComboBox QAbstractItemView {{
    border: 1.5px solid {COLORS["border"]};
    border-radius: 8px;
    background-color: {COLORS["bg_secondary"]};
    selection-background-color: {COLORS["accent_light"]};
    selection-color: {COLORS["text_primary"]};
    padding: 4px;
    outline: none;
}}

QComboBox QAbstractItemView::item {{
    padding: 8px 14px;
    min-height: 32px;
}}

/* ── 标签层级 ─────────────────────────────────── */
QLabel#titleLabel {{
    font-size: 20pt;
    font-weight: bold;
    color: {COLORS["accent"]};
}}

QLabel#subtitleLabel {{
    font-size: 10pt;
    color: {COLORS["text_secondary"]};
    line-height: 1.5;
}}

QLabel#sectionTitle {{
    font-size: 11pt;
    font-weight: bold;
    color: {COLORS["text_primary"]};
}}

QLabel#hintLabel {{
    font-size: 9pt;
    color: {COLORS["text_secondary"]};
}}

/* ── 内联状态标签 ─────────────────────────────── */
QLabel#inlineSuccess {{
    color: {COLORS["success"]};
    font-weight: bold;
    font-size: 10pt;
    padding: 0 6px;
}}

QLabel#inlineError {{
    color: {COLORS["error"]};
    font-weight: bold;
    font-size: 10pt;
    padding: 0 6px;
}}

QLabel#inlineNeutral {{
    color: {COLORS["text_secondary"]};
    font-size: 10pt;
    padding: 0 6px;
}}

/* ── 进度条 ───────────────────────────────────── */
QProgressBar {{
    background-color: {COLORS["accent_light"]};
    border: none;
    border-radius: 10px;
    height: 14px;
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

/* ── 列表 ─────────────────────────────────────── */
QListWidget {{
    background-color: {COLORS["bg_secondary"]};
    border: 1.5px solid {COLORS["border"]};
    border-radius: 10px;
    padding: 6px;
    outline: none;
}}

QListWidget::item {{
    padding: 8px 10px;
    border-bottom: 1px solid {COLORS["border"]};
    border-radius: 4px;
    margin: 1px 2px;
}}

QListWidget::item:selected {{
    background-color: {COLORS["accent_light"]};
    color: {COLORS["text_primary"]};
    border: 1px solid {COLORS["accent"]};
}}

QListWidget::item:hover:!selected {{
    background-color: #F8FAFC;
}}

/* ── 滚动条 ───────────────────────────────────── */
QScrollBar:vertical {{
    background: {COLORS["bg_primary"]};
    width: 10px;
    border-radius: 5px;
    margin: 2px;
}}

QScrollBar::handle:vertical {{
    background: #CBD5E1;
    border-radius: 5px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: {COLORS["accent"]};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background: {COLORS["bg_primary"]};
    height: 10px;
    border-radius: 5px;
    margin: 2px;
}}

QScrollBar::handle:horizontal {{
    background: #CBD5E1;
    border-radius: 5px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {COLORS["accent"]};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}

/* ── 状态标签 ─────────────────────────────────── */
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
