"""程序入口"""
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from core.config_manager import ConfigManager
from ui.main_window import MainWindow
from ui.style_manager import apply_style


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("文档转 Markdown · AI 助手")

    config = ConfigManager()
    apply_style(app)

    window = MainWindow(config)
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
