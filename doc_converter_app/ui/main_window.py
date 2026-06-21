"""主窗口 — UI v2（卡片式布局 / 眼睛按钮 / 内联测试状态 / 模型下拉框）"""
import os
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from core.config_manager import ConfigManager

# ── 常用模型列表（可编辑下拉） ─────────────────────────────────────────────
POPULAR_MODELS = [
    "gpt-4o-mini",
    "gpt-4o",
    "gpt-5.4-mini",
    "deepseek-chat",
    "deepseek-reasoner",
    "glm-4-flash",
    "glm-4",
    "qwen-plus",
    "qwen-turbo",
    "moonshot-v1-8k",
    "claude-3-haiku-20240307",
]


# ── 工具函数：创建带阴影的卡片 Frame ──────────────────────────────────────
def make_card() -> QFrame:
    """返回带圆角、阴影的白色卡片 QFrame"""
    frame = QFrame()
    frame.setObjectName("cardFrame")

    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(18)
    shadow.setOffset(0, 3)
    shadow.setColor(QColor(30, 41, 59, 28))   # 暗蓝半透明阴影
    frame.setGraphicsEffect(shadow)

    return frame


# ── 后台线程：文档转换 ─────────────────────────────────────────────────────
class ConverterWorker(QThread):
    finished_single = Signal(str, str)
    error_single    = Signal(str, str)
    progress        = Signal(int, int)
    all_done        = Signal()

    def __init__(self, files: list[str], output_dir: str | None):
        super().__init__()
        self.files      = files
        self.output_dir = output_dir

    def run(self) -> None:
        from converters.converter_dispatcher import convert_file

        total = len(self.files)
        for i, fpath in enumerate(self.files):
            self.progress.emit(i + 1, total)
            fname = os.path.basename(fpath)
            try:
                out_path = convert_file(fpath, self.output_dir)
                self.finished_single.emit(fpath, f"✅ {fname} → {out_path}")
            except Exception as exc:  # noqa: BLE001
                self.error_single.emit(fpath, f"❌ {fname} 转换失败：{exc}")
        self.all_done.emit()


# ── 后台线程：AI 任务 ──────────────────────────────────────────────────────
class AIWorker(QThread):
    finished = Signal(str)
    error    = Signal(str)

    def __init__(self, mode: str, ai_cfg: dict, **kwargs):
        super().__init__()
        self.mode   = mode
        self.ai_cfg = ai_cfg
        self.kwargs = kwargs

    def run(self) -> None:
        try:
            from core.ai_client import AIConfig, AIClient

            cfg = AIConfig(
                base_url=self.ai_cfg.get("base_url", ""),
                api_key=self.ai_cfg.get("api_key", ""),
                model=self.ai_cfg.get("model", ""),
                temperature=float(self.ai_cfg.get("temperature", 0.7)),
            )
            err = cfg.validate()
            if err:
                self.error.emit(err)
                return

            client = AIClient(cfg)
            if self.mode == "test":
                ok, info = client.test_connection()
                if ok:
                    self.finished.emit(info)
                else:
                    self.error.emit(info)
            elif self.mode == "summarize":
                self.finished.emit(client.summarize_markdown(self.kwargs["md_path"]))
            elif self.mode == "keywords":
                self.finished.emit(client.extract_keywords(self.kwargs["md_path"]))
            elif self.mode == "qa":
                self.finished.emit(
                    client.keyword_qa(self.kwargs["md_path"], self.kwargs["question"])
                )
            elif self.mode == "chat":
                self.finished.emit(client.chat(self.kwargs["messages"]).content)
            else:
                self.error.emit(f"未知模式：{self.mode}")
        except Exception as exc:  # noqa: BLE001
            self.error.emit(str(exc))


# ══════════════════════════════════════════════════════════════════════════════
#  文档转换 Tab
# ══════════════════════════════════════════════════════════════════════════════
class ConverterTab(QWidget):

    def __init__(self, config: ConfigManager):
        super().__init__()
        self.config         = config
        self.selected_files: list[str] = []
        self.worker: ConverterWorker | None = None
        self._build_ui()

    # ── 构建界面 ──────────────────────────────────────────────────────────
    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 24, 24, 24)
        outer.setSpacing(18)

        # 标题区
        title = QLabel("📄 文档 → Markdown 转换")
        title.setObjectName("titleLabel")
        outer.addWidget(title)

        subtitle = QLabel(
            "支持 Word (.docx)、PDF (.pdf)、TXT (.txt)、Excel (.xlsx) — 一键批量转换为 Markdown"
        )
        subtitle.setObjectName("subtitleLabel")
        subtitle.setWordWrap(True)
        outer.addWidget(subtitle)

        outer.addSpacing(6)

        # ── 卡片 1：输出目录 ──────────────────────────────────────────────
        card_out = make_card()
        cl1 = QVBoxLayout(card_out)
        cl1.setContentsMargins(22, 18, 22, 18)
        cl1.setSpacing(12)

        cl1.addWidget(self._section_title("📂 输出目录"))

        out_row = QHBoxLayout()
        out_row.setSpacing(10)
        self.output_edit = QLineEdit()
        self.output_edit.setPlaceholderText("留空则保存到源文件同目录")
        cfg = self.config.get_output_config()
        default_dir = cfg.get("output_dir") or ""
        if default_dir and default_dir != str(Path.cwd() / "output"):
            self.output_edit.setText(default_dir)
        self.btn_pick_output = QPushButton("选择…")
        self.btn_pick_output.setObjectName("secondaryBtn")
        self.btn_pick_output.clicked.connect(self._pick_output_dir)
        self.btn_clear_output = QPushButton("清空")
        self.btn_clear_output.setObjectName("secondaryBtn")
        self.btn_clear_output.clicked.connect(lambda: self.output_edit.clear())
        out_row.addWidget(self.output_edit, 1)
        out_row.addWidget(self.btn_pick_output)
        out_row.addWidget(self.btn_clear_output)
        cl1.addLayout(out_row)

        outer.addWidget(card_out)

        # ── 卡片 2：文件操作区 ────────────────────────────────────────────
        card_files = make_card()
        cl2 = QVBoxLayout(card_files)
        cl2.setContentsMargins(22, 18, 22, 18)
        cl2.setSpacing(14)

        cl2.addWidget(self._section_title("📋 文件列表"))

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        self.btn_add = QPushButton("➕ 添加文件")
        self.btn_add.clicked.connect(self._pick_files)
        self.btn_clear = QPushButton("🗑 清空列表")
        self.btn_clear.setObjectName("secondaryBtn")
        self.btn_clear.clicked.connect(self._clear_files)
        self.btn_convert = QPushButton("🚀 开始转换")
        self.btn_convert.clicked.connect(self._start_conversion)
        btn_row.addWidget(self.btn_add)
        btn_row.addWidget(self.btn_clear)
        btn_row.addStretch(1)
        btn_row.addWidget(self.btn_convert)
        cl2.addLayout(btn_row)

        self.file_list = QListWidget()
        cl2.addWidget(self.file_list, 1)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        cl2.addWidget(self.progress_bar)

        self.status_label = QLabel("")
        self.status_label.setObjectName("hintLabel")
        self.status_label.setWordWrap(True)
        cl2.addWidget(self.status_label)

        outer.addWidget(card_files, 2)

        # ── 卡片 3：转换结果 ──────────────────────────────────────────────
        card_result = make_card()
        cl3 = QVBoxLayout(card_result)
        cl3.setContentsMargins(22, 18, 22, 18)
        cl3.setSpacing(12)

        cl3.addWidget(self._section_title("📋 转换结果"))

        self.result_text = QPlainTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setPlaceholderText("转换结果会显示在这里…")
        cl3.addWidget(self.result_text, 1)

        outer.addWidget(card_result, 1)

    # ── 事件处理 ──────────────────────────────────────────────────────────
    def _pick_files(self) -> None:
        filters = (
            "所有支持文件 (*.docx *.pdf *.txt *.xlsx);;"
            "Word 文档 (*.docx);;PDF 文档 (*.pdf);;纯文本 (*.txt);;Excel 表格 (*.xlsx);;所有文件 (*.*)"
        )
        file_paths, _ = QFileDialog.getOpenFileNames(self, "选择要转换的文档", "", filters)
        for fp in file_paths:
            if fp not in self.selected_files:
                self.selected_files.append(fp)
                item = QListWidgetItem(os.path.basename(fp))
                item.setToolTip(fp)
                self.file_list.addItem(item)
        self.status_label.setText(f"已选择 {len(self.selected_files)} 个文件")

    def _clear_files(self) -> None:
        self.selected_files.clear()
        self.file_list.clear()
        self.status_label.setText("")

    def _pick_output_dir(self) -> None:
        directory = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if directory:
            self.output_edit.setText(directory)

    def _start_conversion(self) -> None:
        if not self.selected_files:
            QMessageBox.information(self, "提示", "请先添加要转换的文件！")
            return
        output_dir = self.output_edit.text().strip() or None
        if output_dir:
            self.config.set_output_config(output_dir=output_dir)
        self.btn_convert.setEnabled(False)
        self.btn_add.setEnabled(False)
        self.result_text.clear()
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(self.selected_files))
        self.progress_bar.setValue(0)
        self.worker = ConverterWorker(self.selected_files, output_dir)
        self.worker.progress.connect(self._on_progress)
        self.worker.finished_single.connect(self._on_one_done)
        self.worker.error_single.connect(self._on_one_error)
        self.worker.all_done.connect(self._on_all_done)
        self.worker.start()

    def _on_progress(self, current: int, total: int) -> None:
        self.progress_bar.setValue(current)
        self.status_label.setText(f"正在转换 ({current}/{total})…")

    def _on_one_done(self, fpath: str, message: str) -> None:
        now = datetime.now().strftime("%H:%M:%S")
        self.result_text.appendPlainText(f"[{now}] {message}")
        self.config.add_history({"type": "convert", "file": fpath, "time": now, "status": "ok"})

    def _on_one_error(self, fpath: str, message: str) -> None:
        now = datetime.now().strftime("%H:%M:%S")
        self.result_text.appendPlainText(f"[{now}] {message}")

    def _on_all_done(self) -> None:
        self.status_label.setText("✅ 全部转换完成！")
        self.progress_bar.setVisible(False)
        self.btn_convert.setEnabled(True)
        self.btn_add.setEnabled(True)

    # ── 辅助 ──────────────────────────────────────────────────────────────
    @staticmethod
    def _section_title(text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("sectionTitle")
        return lbl


# ══════════════════════════════════════════════════════════════════════════════
#  AI 助手 Tab
# ══════════════════════════════════════════════════════════════════════════════
class AITab(QWidget):

    def __init__(self, config: ConfigManager):
        super().__init__()
        self.config       = config
        self.worker: AIWorker | None = None
        self.selected_md: str | None = None
        self._key_visible = False
        self._build_ui()
        self._load_ai_config()

    # ── 构建界面 ──────────────────────────────────────────────────────────
    def _build_ui(self) -> None:
        # 外层用 QScrollArea 防止内容溢出
        outer_widget = QWidget()
        outer = QVBoxLayout(outer_widget)
        outer.setContentsMargins(24, 24, 24, 24)
        outer.setSpacing(18)

        # 标题区
        title = QLabel("🤖 AI 文档助手")
        title.setObjectName("titleLabel")
        outer.addWidget(title)

        subtitle = QLabel("让 AI 帮你总结文档内容、提取关键词、根据文档回答你的问题。")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setWordWrap(True)
        outer.addWidget(subtitle)

        outer.addSpacing(6)

        # ── 卡片 1：API 配置 ──────────────────────────────────────────────
        card_cfg = make_card()
        cc = QVBoxLayout(card_cfg)
        cc.setContentsMargins(22, 20, 22, 20)
        cc.setSpacing(18)

        cc.addWidget(self._section_title("⚙️  API 配置"))

        # Base URL 行
        url_row = QHBoxLayout()
        url_row.setSpacing(12)
        url_lbl = QLabel("Base URL")
        url_lbl.setMinimumWidth(88)
        url_lbl.setAlignment(Qt.AlignVCenter)
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("例如：https://api.deepseek.com/v1")
        url_row.addWidget(url_lbl)
        url_row.addWidget(self.url_input, 1)
        cc.addLayout(url_row)

        # API Key 行（眼睛按钮 + 测试连接 + 内联状态，全在同一行）
        key_row = QHBoxLayout()
        key_row.setSpacing(10)
        key_lbl = QLabel("API Key")
        key_lbl.setMinimumWidth(88)
        key_lbl.setAlignment(Qt.AlignVCenter)
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("粘贴你的 API Key（本地加密保存）")
        self.key_input.setEchoMode(QLineEdit.Password)

        self.btn_eye = QPushButton("👁")
        self.btn_eye.setObjectName("eyeBtn")
        self.btn_eye.setToolTip("显示 / 隐藏 API Key")
        self.btn_eye.setFixedWidth(42)
        self.btn_eye.clicked.connect(self._toggle_key_visibility)

        self.btn_test_cfg = QPushButton("🧪 测试连接")
        self.btn_test_cfg.setObjectName("secondaryBtn")
        self.btn_test_cfg.clicked.connect(self._test_connection)

        self.inline_status = QLabel("")
        self.inline_status.setObjectName("inlineNeutral")
        self.inline_status.setMinimumWidth(110)

        key_row.addWidget(key_lbl)
        key_row.addWidget(self.key_input, 1)
        key_row.addWidget(self.btn_eye)
        key_row.addWidget(self.btn_test_cfg)
        key_row.addWidget(self.inline_status)
        cc.addLayout(key_row)

        # 模型名称行（可编辑下拉框）
        model_row = QHBoxLayout()
        model_row.setSpacing(12)
        model_lbl = QLabel("模型名称")
        model_lbl.setMinimumWidth(88)
        model_lbl.setAlignment(Qt.AlignVCenter)
        self.model_combo = QComboBox()
        self.model_combo.setEditable(True)
        self.model_combo.addItems(POPULAR_MODELS)
        self.model_combo.lineEdit().setPlaceholderText("从列表选择或手动输入模型名称")
        model_row.addWidget(model_lbl)
        model_row.addWidget(self.model_combo, 1)
        cc.addLayout(model_row)

        # 保存按钮行
        save_row = QHBoxLayout()
        self.btn_save_cfg = QPushButton("💾 保存配置")
        self.btn_save_cfg.clicked.connect(self._save_ai_config)
        save_row.addWidget(self.btn_save_cfg)
        save_row.addStretch(1)
        cc.addLayout(save_row)

        outer.addWidget(card_cfg)

        # ── 卡片 2：文档选择 ──────────────────────────────────────────────
        card_doc = make_card()
        cd = QVBoxLayout(card_doc)
        cd.setContentsMargins(22, 20, 22, 20)
        cd.setSpacing(12)

        cd.addWidget(self._section_title("📂 选择要分析的文档"))

        doc_row = QHBoxLayout()
        doc_row.setSpacing(10)
        self.doc_label = QLabel("未选择文档（可手动选 .md，或从转换历史选）")
        self.doc_label.setObjectName("hintLabel")
        self.doc_label.setWordWrap(True)
        self.btn_pick_md     = QPushButton("📂 选择文件…")
        self.btn_pick_md.setObjectName("secondaryBtn")
        self.btn_pick_md.clicked.connect(self._pick_md_file)
        self.btn_from_history = QPushButton("🕓 历史记录…")
        self.btn_from_history.setObjectName("secondaryBtn")
        self.btn_from_history.clicked.connect(self._pick_from_history)
        self.btn_clear_doc   = QPushButton("清除")
        self.btn_clear_doc.setObjectName("secondaryBtn")
        self.btn_clear_doc.clicked.connect(self._clear_doc)
        doc_row.addWidget(self.doc_label, 1)
        doc_row.addWidget(self.btn_pick_md)
        doc_row.addWidget(self.btn_from_history)
        doc_row.addWidget(self.btn_clear_doc)
        cd.addLayout(doc_row)

        outer.addWidget(card_doc)

        # ── 卡片 3：一键 AI 操作 ──────────────────────────────────────────
        card_quick = make_card()
        cq = QVBoxLayout(card_quick)
        cq.setContentsMargins(22, 20, 22, 20)
        cq.setSpacing(14)

        cq.addWidget(self._section_title("⚡ 一键 AI 操作"))

        hint_quick = QLabel("需先在上方选择好要分析的 Markdown 文档")
        hint_quick.setObjectName("hintLabel")
        cq.addWidget(hint_quick)

        quick_row = QHBoxLayout()
        quick_row.setSpacing(12)
        self.btn_summarize = QPushButton("📝 总结文档")
        self.btn_summarize.clicked.connect(lambda: self._run_ai("summarize"))
        self.btn_keywords  = QPushButton("🔑 提取关键词")
        self.btn_keywords.setObjectName("secondaryBtn")
        self.btn_keywords.clicked.connect(lambda: self._run_ai("keywords"))
        quick_row.addWidget(self.btn_summarize)
        quick_row.addWidget(self.btn_keywords)
        quick_row.addStretch(1)
        cq.addLayout(quick_row)

        outer.addWidget(card_quick)

        # ── 卡片 4：对话区（可拉伸） ─────────────────────────────────────
        card_chat = make_card()
        ch = QVBoxLayout(card_chat)
        ch.setContentsMargins(22, 20, 22, 20)
        ch.setSpacing(12)

        ch.addWidget(self._section_title("💬 AI 对话 / 问答"))

        self.chat_text = QPlainTextEdit()
        self.chat_text.setReadOnly(True)
        self.chat_text.setPlaceholderText(
            "AI 回答会显示在这里。\n"
            "• 已选文档 → 基于文档内容回答\n"
            "• 未选文档 → 与模型自由对话"
        )
        ch.addWidget(self.chat_text, 1)

        query_row = QHBoxLayout()
        query_row.setSpacing(10)
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("输入你的问题，按 Enter 发送…")
        self.query_input.returnPressed.connect(self._send_query)
        self.btn_send = QPushButton("发送 ▶")
        self.btn_send.setFixedWidth(100)
        self.btn_send.clicked.connect(self._send_query)
        query_row.addWidget(self.query_input, 1)
        query_row.addWidget(self.btn_send)
        ch.addLayout(query_row)

        outer.addWidget(card_chat, 1)

        # 包裹到 ScrollArea（防止窗口过小时内容被截断）
        scroll = QScrollArea(self)
        scroll.setWidget(outer_widget)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addWidget(scroll)

    # ── API Key 显隐 ──────────────────────────────────────────────────────
    def _toggle_key_visibility(self) -> None:
        self._key_visible = not self._key_visible
        if self._key_visible:
            self.key_input.setEchoMode(QLineEdit.Normal)
            self.btn_eye.setText("🙈")
            self.btn_eye.setToolTip("隐藏 API Key")
        else:
            self.key_input.setEchoMode(QLineEdit.Password)
            self.btn_eye.setText("👁")
            self.btn_eye.setToolTip("显示 API Key")

    # ── 配置 ──────────────────────────────────────────────────────────────
    def _load_ai_config(self) -> None:
        ai = self.config.get_ai_config()
        self.url_input.setText(ai.get("base_url", ""))
        self.key_input.setText(ai.get("api_key", ""))
        model = ai.get("model", "")
        if model:
            idx = self.model_combo.findText(model)
            if idx >= 0:
                self.model_combo.setCurrentIndex(idx)
            else:
                self.model_combo.setCurrentText(model)

    def _save_ai_config(self) -> None:
        self.config.set_ai_config(
            base_url=self.url_input.text().strip(),
            api_key=self.key_input.text().strip(),
            model=self.model_combo.currentText().strip(),
        )
        self._set_inline_status("✅ 已保存", success=True)

    def _set_inline_status(self, text: str, success: bool | None = None) -> None:
        self.inline_status.setText(text)
        if success is True:
            name = "inlineSuccess"
        elif success is False:
            name = "inlineError"
        else:
            name = "inlineNeutral"
        self.inline_status.setObjectName(name)
        self.inline_status.style().unpolish(self.inline_status)
        self.inline_status.style().polish(self.inline_status)

    def _test_connection(self) -> None:
        ai_cfg = self._collect_ai_cfg()
        if not ai_cfg["api_key"] or not ai_cfg["base_url"]:
            self._set_inline_status("❌ 请先填写 Base URL 和 Key", success=False)
            return
        self._set_inline_status("🔄 连接中…", success=None)
        self._set_buttons_enabled(False)
        self.worker = AIWorker("test", ai_cfg)
        self.worker.finished.connect(lambda _: self._on_test_done(True))
        self.worker.error.connect(lambda _: self._on_test_done(False))
        self.worker.start()

    def _on_test_done(self, success: bool) -> None:
        self._set_inline_status("✅ 连接成功" if success else "❌ 连接失败", success=success)
        self._set_buttons_enabled(True)

    def _collect_ai_cfg(self) -> dict:
        return {
            "base_url":    self.url_input.text().strip(),
            "api_key":     self.key_input.text().strip(),
            "model":       self.model_combo.currentText().strip(),
            "temperature": 0.7,
        }

    # ── 文档选择 ──────────────────────────────────────────────────────────
    def _pick_md_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "选择要分析的 Markdown 文档", "", "Markdown 文件 (*.md);;所有文件 (*.*)"
        )
        if path:
            self._use_doc(path)

    def _pick_from_history(self) -> None:
        history = self.config.get_history()
        valid   = [h for h in history if h.get("type") == "convert" and h.get("file")]
        if not valid:
            QMessageBox.information(self, "提示", "暂无转换历史。请先在「文档转换」页转换一份文档。")
            return
        from PySide6.QtWidgets import QInputDialog
        choice, ok = QInputDialog.getItem(
            self, "从历史选择", "选择文档（自动查找同目录的 .md）",
            [h["file"] for h in valid], 0, False,
        )
        if ok and choice:
            md_path = Path(choice).with_suffix(".md")
            if md_path.exists():
                self._use_doc(str(md_path))
            else:
                out_cfg   = self.config.get_output_config()
                out_dir   = out_cfg.get("output_dir")
                candidate = Path(out_dir) / md_path.name if out_dir else None
                if candidate and candidate.exists():
                    self._use_doc(str(candidate))
                else:
                    QMessageBox.warning(
                        self, "未找到对应的 .md",
                        f"没找到：\n{md_path}\n\n请先在「文档转换」页将它转为 .md。",
                    )

    def _use_doc(self, path: str) -> None:
        self.selected_md = path
        self.doc_label.setText(f"✅ 已选择：{path}")

    def _clear_doc(self) -> None:
        self.selected_md = None
        self.doc_label.setText("未选择文档（可手动选 .md，或从转换历史选）")

    # ── AI 任务 ───────────────────────────────────────────────────────────
    def _run_ai(self, mode: str) -> None:
        ai_cfg = self._collect_ai_cfg()
        if not ai_cfg["api_key"] or not ai_cfg["base_url"] or not ai_cfg["model"]:
            QMessageBox.warning(self, "提示", "请先填写 Base URL、API Key 和模型名称！")
            return
        if mode in ("summarize", "keywords", "qa") and not self.selected_md:
            QMessageBox.warning(self, "提示", "请先选择要分析的 Markdown 文档！")
            return

        self._set_buttons_enabled(False)
        label_map = {
            "summarize": "📝 正在总结文档…",
            "keywords":  "🔑 正在提取关键词…",
            "qa":        "🤖 正在回答问题…",
        }
        self._append_chat("系统", label_map.get(mode, "🤖 正在调用 AI…"))

        kwargs: dict = {}
        if mode == "summarize":
            kwargs["md_path"] = self.selected_md
            self._append_chat("你", f"【总结】{Path(self.selected_md).name}")
        elif mode == "keywords":
            kwargs["md_path"] = self.selected_md
            self._append_chat("你", f"【关键词】{Path(self.selected_md).name}")
        elif mode == "qa":
            kwargs["md_path"]  = self.selected_md
            kwargs["question"] = self.query_input.text().strip()
            self._append_chat("你", f"（基于文档）{kwargs['question']}")

        self.worker = AIWorker(mode, ai_cfg, **kwargs)
        self.worker.finished.connect(self._on_ai_reply)
        self.worker.error.connect(self._on_ai_error)
        self.worker.start()

    def _send_query(self) -> None:
        query = self.query_input.text().strip()
        if not query:
            return
        self.query_input.clear()
        ai_cfg = self._collect_ai_cfg()
        if not ai_cfg["api_key"] or not ai_cfg["base_url"] or not ai_cfg["model"]:
            QMessageBox.warning(self, "提示", "请先填写 Base URL、API Key 和模型名称！")
            return
        self._set_buttons_enabled(False)
        if self.selected_md:
            self._append_chat("你", f"（基于文档）{query}")
            self._append_chat("系统", "🤖 正在回答问题…")
            self.worker = AIWorker("qa", ai_cfg, md_path=self.selected_md, question=query)
        else:
            self._append_chat("你", query)
            self.worker = AIWorker(
                "chat", ai_cfg, messages=[{"role": "user", "content": query}]
            )
        self.worker.finished.connect(self._on_ai_reply)
        self.worker.error.connect(self._on_ai_error)
        self.worker.start()

    # ── UI 辅助 ───────────────────────────────────────────────────────────
    def _set_buttons_enabled(self, enabled: bool) -> None:
        for w in (
            self.btn_save_cfg, self.btn_test_cfg,
            self.btn_pick_md, self.btn_from_history, self.btn_clear_doc,
            self.btn_summarize, self.btn_keywords, self.btn_send,
        ):
            w.setEnabled(enabled)

    def _append_chat(self, who: str, content: str) -> None:
        now  = datetime.now().strftime("%H:%M:%S")
        icon = {"你": "🧑", "AI": "🤖", "系统": "ℹ️"}.get(who, "•")
        self.chat_text.appendPlainText(f"{icon} [{who} · {now}]\n{content}\n")

    def _on_ai_reply(self, content: str) -> None:
        self._append_chat("AI", content)
        self._set_buttons_enabled(True)

    def _on_ai_error(self, err: str) -> None:
        self._append_chat("系统", f"❌ 出错了：{err}")
        self._set_buttons_enabled(True)

    @staticmethod
    def _section_title(text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("sectionTitle")
        return lbl


# ══════════════════════════════════════════════════════════════════════════════
#  主窗口
# ══════════════════════════════════════════════════════════════════════════════
class MainWindow(QMainWindow):

    def __init__(self, config: ConfigManager):
        super().__init__()
        self.config = config
        self.setWindowTitle("📚 文档转 Markdown · AI 助手")
        self.resize(980, 780)

        root = QWidget()
        root.setObjectName("rootWidget")
        self.setCentralWidget(root)

        layout = QVBoxLayout(root)
        layout.setContentsMargins(16, 16, 16, 12)
        layout.setSpacing(12)

        self.tabs = QTabWidget()
        self.converter_tab = ConverterTab(config)
        self.ai_tab        = AITab(config)
        self.tabs.addTab(self.converter_tab, "📄 文档转换")
        self.tabs.addTab(self.ai_tab,        "🤖 AI 助手")
        self.tabs.setCurrentIndex(config.get_last_tab())
        self.tabs.currentChanged.connect(self._on_tab_changed)
        layout.addWidget(self.tabs)

        status_label = QLabel(
            "✨ 文档转 Markdown + AI 助手已就绪（支持 .docx / .pdf / .txt / .xlsx）"
        )
        status_label.setObjectName("hintLabel")
        status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(status_label)

    def _on_tab_changed(self, index: int) -> None:
        self.config.set_last_tab(index)

    def closeEvent(self, event) -> None:
        event.accept()
