"""双击启动用：由 pythonw 执行，不弹出控制台窗口。"""

from pathlib import Path
import runpy

_root = Path(__file__).resolve().parent
runpy.run_path(str(_root / "main.py"), run_name="__main__")
