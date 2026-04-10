"""可爱小计时器 PySide6 实现"""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QIcon, QMouseEvent
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

# ========== 发布时请修改（窗口标题会显示在任务栏）==========
APP_TITLE = "hh计时器"
# ============================================================

_APP_DIR = Path(__file__).resolve().parent


def _window_icon() -> QIcon | None:
    ico = _APP_DIR / "assets" / "app.ico"
    if ico.is_file():
        return QIcon(str(ico))
    return None


CUTE_QSS = """
QWidget {
    background-color: #fff5f7;
    color: #593144;
    font-size: 14px;
}
QLabel#title {
    font-size: 28px;
    font-weight: 700;
    color: #ec4899;
    padding: 8px 0 12px 0;
}
QLabel#timeDisplay {
    font-size: 72px;
    font-weight: 800;
    color: #db2777;
    background-color: #fce7f3;
    border-radius: 24px;
    padding: 32px 24px;
    margin: 16px 0;
    qproperty-alignment: AlignCenter;
}
QLabel#hint {
    color: #9d6b87;
    font-size: 13px;
}
QPushButton {
    border: none;
    border-radius: 18px;
    padding: 14px 32px;
    font-weight: 700;
    font-size: 16px;
    min-width: 100px;
}
QPushButton#startBtn {
    background-color: #f472b6;
    color: #4a044e;
}
QPushButton#startBtn:hover { background-color: #ec4899; }
QPushButton#startBtn:pressed { background-color: #db2777; }
QPushButton#pauseBtn {
    background-color: #60a5fa;
    color: #1e3a8a;
}
QPushButton#pauseBtn:hover { background-color: #3b82f6; }
QPushButton#pauseBtn:pressed { background-color: #2563eb; }
QPushButton#resetBtn {
    background-color: #fbbf24;
    color: #78350f;
}
QPushButton#resetBtn:hover { background-color: #f59e0b; }
QPushButton#resetBtn:pressed { background-color: #d97706; }
"""


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.setMinimumSize(520, 420)
        icon = _window_icon()
        if icon is not None:
            self.setWindowIcon(icon)

        # 计时器相关变量
        self.total_seconds = 25 * 60  # 默认25分钟
        self.is_running = False
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self._update_time)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(32, 28, 32, 28)

        title = QLabel("⏰ hh计时器 ⏰")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        # 时间显示
        self.time_label = QLabel()
        self.time_label.setObjectName("timeDisplay")
        self._format_time()

        # 按钮区域
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(16)

        self.start_btn = QPushButton("开始")
        self.start_btn.setObjectName("startBtn")
        self.start_btn.clicked.connect(self._start_timer)

        self.pause_btn = QPushButton("暂停")
        self.pause_btn.setObjectName("pauseBtn")
        self.pause_btn.clicked.connect(self._pause_timer)
        self.pause_btn.setEnabled(False)

        self.reset_btn = QPushButton("重置")
        self.reset_btn.setObjectName("resetBtn")
        self.reset_btn.clicked.connect(self._reset_timer)

        btn_layout.addStretch()
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.pause_btn)
        btn_layout.addWidget(self.reset_btn)
        btn_layout.addStretch()

        hint = QLabel("✨ 默认专注25分钟，点击时间可以快速调整哦 ✨")
        hint.setObjectName("hint")
        hint.setAlignment(Qt.AlignCenter)
        hint.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(self.time_label)
        layout.addLayout(btn_layout)
        layout.addStretch()
        layout.addWidget(hint)

    def _format_time(self) -> None:
        minutes = self.total_seconds // 60
        seconds = self.total_seconds % 60
        self.time_label.setText(f"{minutes:02d}:{seconds:02d}")

    def _start_timer(self) -> None:
        self.is_running = True
        self.timer.start()
        self.start_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)

    def _pause_timer(self) -> None:
        self.is_running = False
        self.timer.stop()
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)

    def _reset_timer(self) -> None:
        self.is_running = False
        self.timer.stop()
        self.total_seconds = 25 * 60
        self._format_time()
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)

    def _update_time(self) -> None:
        if self.total_seconds > 0:
            self.total_seconds -= 1
            self._format_time()
        else:
            self._pause_timer()
            self.time_label.setText("🎉 时间到！")

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.time_label.underMouse():
            # 点击时间区域快速调整时间（每次加5分钟）
            if not self.is_running:
                self.total_seconds = (self.total_seconds // 300 + 1) * 300
                if self.total_seconds > 3600:  # 最多1小时
                    self.total_seconds = 5 * 60  # 循环回到5分钟
                self._format_time()
        super().mousePressEvent(event)


def main() -> int:
    app = QApplication(sys.argv)
    icon = _window_icon()
    if icon is not None:
        app.setWindowIcon(icon)
    app.setStyle("Fusion")
    app.setStyleSheet(CUTE_QSS)

    font = QFont()
    font.setFamilies(["Microsoft YaHei UI", "PingFang SC", "Segoe UI", "sans-serif"])
    font.setPointSize(10)
    app.setFont(font)

    win = MainWindow()
    win.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
