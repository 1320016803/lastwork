import os
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QFileDialog,
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
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from core.config_manager import ConfigManager


class ConverterWorker(QThread):
    """后台转换任务（第 2 阶段：真实调用转换器）"""

    finished_single = Signal(str, str)
    error_single = Signal(str, str)
    progress = Signal(int, int)
    all_done = Signal()

    def __init__(self, files: list[str], output_dir: str | None):
        super().__init__()
        self.files = files
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


class AIWorker(QThread):
    """后台 AI 任务（通用：可跑 test/summarize/keywords/qa）"""

    finished = Signal(str)
    error = Signal(str)

    def __init__(self, mode: str, ai_cfg: dict, **kwargs):
        """
        mode: 'test' | 'summarize' | 'keywords' | 'qa' | 'chat'
        kwargs: 根据 mode 不同，提供 md_path / question / messages 等
        """
        super().__init__()
        self.mode = mode
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
                md_path = self.kwargs["md_path"]
                result = client.summarize_markdown(md_path)
                self.finished.emit(result)
            elif self.mode == "keywords":
                md_path = self.kwargs["md_path"]
                result = client.extract_keywords(md_path)
                self.finished.emit(result)
            elif self.mode == "qa":
                md_path = self.kwargs["md_path"]
                question = self.kwargs["question"]
                result = client.keyword_qa(md_path, question)
                self.finished.emit(result)
            elif self.mode == "chat":
                messages = self.kwargs["messages"]
                result = client.chat(messages).content
                self.finished.emit(result)
            else:
                self.error.emit(f"未知模式：{self.mode}")
        except Exception as exc:  # noqa: BLE001
            self.error.emit(str(exc))


class ConverterTab(QWidget):
    """文档转换标签页"""

    def __init__(self, config: ConfigManager):
        super().__init__()
        self.config = config
        self.selected_files: list[str] = []
        self.worker: ConverterWorker | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        title = QLabel("📄 文档 → Markdown 转换")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        subtitle = QLabel("支持 Word (.docx)、PDF (.pdf)、TXT (.txt)、Excel (.xlsx) — 一键转换为 Markdown")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        # 输出目录选择
        output_row = QHBoxLayout()
        output_row.setSpacing(10)
        output_label = QLabel("📂 输出目录：")
        output_label.setMinimumWidth(80)
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
        output_row.addWidget(output_label)
        output_row.addWidget(self.output_edit, 1)
        output_row.addWidget(self.btn_pick_output)
        output_row.addWidget(self.btn_clear_output)
        layout.addLayout(output_row)

        # 文件操作栏
        button_row = QHBoxLayout()
        button_row.setSpacing(10)

        self.btn_add = QPushButton("➕ 添加文件")
        self.btn_add.clicked.connect(self._pick_files)

        self.btn_clear = QPushButton("🗑 清空列表")
        self.btn_clear.setObjectName("secondaryBtn")
        self.btn_clear.clicked.connect(self._clear_files)

        self.btn_convert = QPushButton("🚀 开始转换")
        self.btn_convert.clicked.connect(self._start_conversion)

        button_row.addWidget(self.btn_add)
        button_row.addWidget(self.btn_clear)
        button_row.addStretch(1)
        button_row.addWidget(self.btn_convert)
        layout.addLayout(button_row)

        # 文件列表
        self.file_list = QListWidget()
        layout.addWidget(self.file_list, 1)

        # 进度与状态
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel("")
        self.status_label.setObjectName("hintLabel")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        # 结果区
        result_title = QLabel("📋 转换结果")
        result_title.setObjectName("subtitleLabel")
        layout.addWidget(result_title)

        self.result_text = QPlainTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setPlaceholderText("转换结果会显示在这里…")
        layout.addWidget(self.result_text, 1)

    # -------- 事件处理 --------
    def _pick_files(self) -> None:
        filters = (
            "所有支持文件 (*.docx *.pdf *.txt *.xlsx);;"
            "Word 文档 (*.docx);;"
            "PDF 文档 (*.pdf);;"
            "纯文本 (*.txt);;"
            "Excel 表格 (*.xlsx);;"
            "所有文件 (*.*)"
        )
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "选择要转换的文档",
            "",
            filters,
        )
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
        self.config.add_history({
            "type": "convert",
            "file": fpath,
            "time": now,
            "status": "ok",
        })

    def _on_one_error(self, fpath: str, message: str) -> None:
        now = datetime.now().strftime("%H:%M:%S")
        self.result_text.appendPlainText(f"[{now}] {message}")

    def _on_all_done(self) -> None:
        self.status_label.setText("转换完成！")
        self.progress_bar.setVisible(False)
        self.btn_convert.setEnabled(True)
        self.btn_add.setEnabled(True)


class AITab(QWidget):
    """AI 文档助手标签页"""

    def __init__(self, config: ConfigManager):
        super().__init__()
        self.config = config
        self.worker: AIWorker | None = None
        self.selected_md: str | None = None  # 当前选中用于 AI 分析的 .md
        self._build_ui()
        self._load_ai_config()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        title = QLabel("🤖 AI 文档助手")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        subtitle = QLabel("让 AI 帮你总结文档内容、提取关键词、根据文档回答你的问题。")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        # ---- 配置区 ----
        cfg_title = QLabel("1️⃣ API 配置（首次使用请填写）")
        cfg_title.setObjectName("subtitleLabel")
        layout.addWidget(cfg_title)

        # Base URL
        url_row = QHBoxLayout()
        url_label = QLabel("Base URL:")
        url_label.setMinimumWidth(85)
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("例如：https://api.deepseek.com/v1  / https://open.bigmodel.cn/api/paas/v4")
        url_row.addWidget(url_label)
        url_row.addWidget(self.url_input, 1)
        layout.addLayout(url_row)

        # API Key
        key_row = QHBoxLayout()
        key_label = QLabel("API Key:")
        key_label.setMinimumWidth(85)
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("你的 API Key（保存在本地 config.json）")
        self.key_input.setEchoMode(QLineEdit.Password)
        key_row.addWidget(key_label)
        key_row.addWidget(self.key_input, 1)
        layout.addLayout(key_row)

        # 模型名
        model_row = QHBoxLayout()
        model_label = QLabel("模型名称:")
        model_label.setMinimumWidth(85)
        self.model_input = QLineEdit()
        self.model_input.setPlaceholderText("例如：deepseek-chat / gpt-4o-mini / glm-4-flash / qwen-plus")
        model_row.addWidget(model_label)
        model_row.addWidget(self.model_input, 1)
        layout.addLayout(model_row)

        # 配置按钮
        cfg_btn_row = QHBoxLayout()
        self.btn_save_cfg = QPushButton("💾 保存配置")
        self.btn_save_cfg.clicked.connect(self._save_ai_config)
        self.btn_test_cfg = QPushButton("🧪 测试连接")
        self.btn_test_cfg.setObjectName("secondaryBtn")
        self.btn_test_cfg.clicked.connect(self._test_connection)
        cfg_btn_row.addWidget(self.btn_save_cfg)
        cfg_btn_row.addWidget(self.btn_test_cfg)
        cfg_btn_row.addStretch(1)
        layout.addLayout(cfg_btn_row)

        self.cfg_status = QLabel("")
        self.cfg_status.setObjectName("hintLabel")
        self.cfg_status.setWordWrap(True)
        layout.addWidget(self.cfg_status)

        # ---- 文档选择区 ----
        doc_title = QLabel("2️⃣ 选择要分析的 Markdown 文档")
        doc_title.setObjectName("subtitleLabel")
        layout.addWidget(doc_title)

        doc_row = QHBoxLayout()
        self.doc_label = QLabel("未选择文档（可手动选 .md，或从转换历史里选）")
        self.doc_label.setObjectName("hintLabel")
        self.doc_label.setWordWrap(True)
        self.btn_pick_md = QPushButton("📂 选择文件…")
        self.btn_pick_md.setObjectName("secondaryBtn")
        self.btn_pick_md.clicked.connect(self._pick_md_file)
        self.btn_from_history = QPushButton("🕓 从转换历史选择…")
        self.btn_from_history.setObjectName("secondaryBtn")
        self.btn_from_history.clicked.connect(self._pick_from_history)
        self.btn_clear_doc = QPushButton("清除")
        self.btn_clear_doc.setObjectName("secondaryBtn")
        self.btn_clear_doc.clicked.connect(self._clear_doc)
        doc_row.addWidget(self.doc_label, 1)
        doc_row.addWidget(self.btn_pick_md)
        doc_row.addWidget(self.btn_from_history)
        doc_row.addWidget(self.btn_clear_doc)
        layout.addLayout(doc_row)

        # ---- 快速操作区 ----
        quick_title = QLabel("3️⃣ 一键 AI 操作")
        quick_title.setObjectName("subtitleLabel")
        layout.addWidget(quick_title)

        quick_row = QHBoxLayout()
        self.btn_summarize = QPushButton("📝 总结文档")
        self.btn_summarize.clicked.connect(lambda: self._run_ai("summarize"))
        self.btn_keywords = QPushButton("🔑 提取关键词")
        self.btn_keywords.setObjectName("secondaryBtn")
        self.btn_keywords.clicked.connect(lambda: self._run_ai("keywords"))
        quick_row.addWidget(self.btn_summarize)
        quick_row.addWidget(self.btn_keywords)
        quick_row.addStretch(1)
        layout.addLayout(quick_row)

        # ---- 对话区 ----
        chat_title = QLabel("4️⃣ 与 AI 对话/问答")
        chat_title.setObjectName("subtitleLabel")
        layout.addWidget(chat_title)

        self.chat_text = QPlainTextEdit()
        self.chat_text.setReadOnly(True)
        self.chat_text.setPlaceholderText(
            "AI 回答会显示在这里。\n"
            "• 如已选文档：问题会「基于文档内容」回答\n"
            "• 如未选文档：与模型自由对话"
        )
        layout.addWidget(self.chat_text, 1)

        query_row = QHBoxLayout()
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("输入你的问题，按回车发送…")
        self.query_input.returnPressed.connect(self._send_query)
        self.btn_send = QPushButton("发送")
        self.btn_send.setFixedWidth(80)
        self.btn_send.clicked.connect(self._send_query)
        query_row.addWidget(self.query_input, 1)
        query_row.addWidget(self.btn_send)
        layout.addLayout(query_row)

    # -------- 配置 --------
    def _load_ai_config(self) -> None:
        ai = self.config.get_ai_config()
        self.url_input.setText(ai.get("base_url", ""))
        self.key_input.setText(ai.get("api_key", ""))
        self.model_input.setText(ai.get("model", ""))

    def _save_ai_config(self) -> None:
        self.config.set_ai_config(
            base_url=self.url_input.text().strip(),
            api_key=self.key_input.text().strip(),
            model=self.model_input.text().strip(),
        )
        self._set_cfg_status("✅ 配置已保存到 config.json", success=True)

    def _set_cfg_status(self, text: str, success: bool = True) -> None:
        self.cfg_status.setText(text)
        self.cfg_status.setObjectName("successLabel" if success else "warningLabel")
        self.cfg_status.style().unpolish(self.cfg_status)
        self.cfg_status.style().polish(self.cfg_status)

    def _test_connection(self) -> None:
        ai_cfg = self._collect_ai_cfg()
        if not ai_cfg["api_key"] or not ai_cfg["base_url"]:
            QMessageBox.warning(self, "提示", "请先填写 Base URL 和 API Key！")
            return
        self._set_cfg_status("🔄 正在测试与 API 的连接…", success=False)
        self._set_buttons_enabled(False)
        self.worker = AIWorker("test", ai_cfg)
        self.worker.finished.connect(lambda msg: self._on_test_done(msg, True))
        self.worker.error.connect(lambda msg: self._on_test_done(msg, False))
        self.worker.start()

    def _collect_ai_cfg(self) -> dict:
        return {
            "base_url": self.url_input.text().strip(),
            "api_key": self.key_input.text().strip(),
            "model": self.model_input.text().strip(),
            "temperature": 0.7,
        }

    def _on_test_done(self, msg: str, success: bool) -> None:
        self._set_cfg_status(("✅ " if success else "❌ ") + msg, success=success)
        self._set_buttons_enabled(True)

    # -------- 文档选择 --------
    def _pick_md_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "选择要分析的 Markdown 文档", "", "Markdown 文件 (*.md);;所有文件 (*.*)"
        )
        if path:
            self._use_doc(path)

    def _pick_from_history(self) -> None:
        history = self.config.get_history()
        valid = [h for h in history if h.get("type") == "convert" and h.get("file")]
        if not valid:
            QMessageBox.information(self, "提示", "暂无转换历史。请先在「文档转换」页转换一份文档。")
            return
        paths = [h["file"] for h in valid]
        # 用 QInputItem 简单起见
        from PySide6.QtWidgets import QInputDialog
        choice, ok = QInputDialog.getItem(
            self, "从历史选择", "选择文档（显示的是源文件，会自动用同目录的 .md）",
            paths, 0, False,
        )
        if ok and choice:
            md_path = Path(choice).with_suffix(".md")
            if md_path.exists():
                self._use_doc(str(md_path))
            else:
                # 尝试搜索输出目录
                out_cfg = self.config.get_output_config()
                out_dir = out_cfg.get("output_dir")
                candidate = Path(out_dir) / md_path.name if out_dir else None
                if candidate and candidate.exists():
                    self._use_doc(str(candidate))
                else:
                    QMessageBox.warning(
                        self, "未找到对应的 .md",
                        f"没找到对应的 Markdown：\n{md_path}\n\n请先在「文档转换」页把它转为 .md。"
                    )

    def _use_doc(self, path: str) -> None:
        self.selected_md = path
        self.doc_label.setText(f"✅ 已选择：{path}")

    def _clear_doc(self) -> None:
        self.selected_md = None
        self.doc_label.setText("未选择文档（可手动选 .md，或从转换历史里选）")

    # -------- AI 任务入口 --------
    def _run_ai(self, mode: str) -> None:
        ai_cfg = self._collect_ai_cfg()
        if not ai_cfg["api_key"] or not ai_cfg["base_url"] or not ai_cfg["model"]:
            QMessageBox.warning(self, "提示", "请先在上方填写 Base URL、API Key 和模型名称！")
            return

        if mode in ("summarize", "keywords", "qa") and not self.selected_md:
            QMessageBox.warning(self, "提示", "请先在第 2 步选择要分析的 Markdown 文档！")
            return

        self._set_buttons_enabled(False)
        label_map = {
            "summarize": "📝 正在总结文档…",
            "keywords": "🔑 正在提取关键词…",
            "qa": "🤖 正在回答问题…",
        }
        header = label_map.get(mode, "🤖 正在调用 AI…")
        self._append_chat("系统", header)

        kwargs = {}
        if mode in ("summarize", "keywords"):
            kwargs["md_path"] = self.selected_md
            label = f"【总结】{Path(self.selected_md).name}" if mode == "summarize" else f"【关键词】{Path(self.selected_md).name}"
            self._append_chat("你", label)
        elif mode == "qa":
            kwargs["md_path"] = self.selected_md
            kwargs["question"] = self.query_input.text().strip()
            self._append_chat("你", f"（基于文档）{kwargs['question']}")

        self.worker = AIWorker(mode, ai_cfg, **kwargs)
        self.worker.finished.connect(self._on_ai_reply)
        self.worker.error.connect(self._on_ai_error)
        self.worker.start()

    # -------- 对话 / 发送问题 --------
    def _send_query(self) -> None:
        query = self.query_input.text().strip()
        if not query:
            return
        self.query_input.clear()

        ai_cfg = self._collect_ai_cfg()
        if not ai_cfg["api_key"] or not ai_cfg["base_url"] or not ai_cfg["model"]:
            QMessageBox.warning(self, "提示", "请先在上方填写 Base URL、API Key 和模型名称！")
            return

        self._set_buttons_enabled(False)

        if self.selected_md:
            # 有选文档 → 走 QA（基于文档内容回答）
            self._append_chat("你", f"（基于文档）{query}")
            self._append_chat("系统", "🤖 正在回答问题…")
            self.worker = AIWorker("qa", ai_cfg, md_path=self.selected_md, question=query)
        else:
            # 没选文档 → 走自由对话
            self._append_chat("你", query)
            self.worker = AIWorker(
                "chat", ai_cfg,
                messages=[{"role": "user", "content": query}],
            )
        self.worker.finished.connect(self._on_ai_reply)
        self.worker.error.connect(self._on_ai_error)
        self.worker.start()

    def _run_ai_no_double_clear(self, mode: str, question: str) -> None:
        """保留签名，避免调用点残留错误；实际已不再使用。"""
        pass

    # -------- UI 辅助 --------
    def _set_buttons_enabled(self, enabled: bool) -> None:
        for w in (
            self.btn_save_cfg, self.btn_test_cfg,
            self.btn_pick_md, self.btn_from_history, self.btn_clear_doc,
            self.btn_summarize, self.btn_keywords,
            self.btn_send,
        ):
            w.setEnabled(enabled)

    def _append_chat(self, who: str, content: str) -> None:
        now = datetime.now().strftime("%H:%M:%S")
        icon = {"你": "🧑", "AI": "🤖", "系统": "ℹ️"}.get(who, "•")
        self.chat_text.appendPlainText(f"{icon} [{who} · {now}]\n{content}\n")

    def _on_ai_reply(self, content: str) -> None:
        self._append_chat("AI", content)
        self._set_buttons_enabled(True)

    def _on_ai_error(self, err: str) -> None:
        self._append_chat("系统", f"❌ 出错了：{err}")
        self._set_buttons_enabled(True)


class MainWindow(QMainWindow):
    """应用主窗口"""

    def __init__(self, config: ConfigManager):
        super().__init__()
        self.config = config
        self.setWindowTitle("📚 文档转 Markdown · AI 助手")
        self.resize(900, 700)

        root = QWidget()
        root.setObjectName("rootWidget")
        self.setCentralWidget(root)

        layout = QVBoxLayout(root)
        layout.setContentsMargins(16, 16, 16, 16)

        self.tabs = QTabWidget()
        self.converter_tab = ConverterTab(config)
        self.ai_tab = AITab(config)
        self.tabs.addTab(self.converter_tab, "📄 文档转换")
        self.tabs.addTab(self.ai_tab, "🤖 AI 助手")
        self.tabs.setCurrentIndex(config.get_last_tab())
        self.tabs.currentChanged.connect(self._on_tab_changed)

        layout.addWidget(self.tabs)

        # 底部状态栏
        status_label = QLabel("✨ 文档转 Markdown + AI 助手已就绪（支持 .docx / .pdf / .txt / .xlsx）")
        status_label.setObjectName("hintLabel")
        status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(status_label)

    def _on_tab_changed(self, index: int) -> None:
        self.config.set_last_tab(index)

    def closeEvent(self, event) -> None:
        event.accept()
