from __future__ import annotations

from pathlib import Path

import fitz  # PyMuPDF

from .converter_base import BaseConverter


class PdfConverter(BaseConverter):
    SUPPORTED_EXT = (".pdf",)

    def _to_markdown(self, src: Path) -> str:
        doc = fitz.open(str(src))
        blocks: list[str] = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            blocks.append(f"## 第 {page_num + 1} 页\n")

            # 先用简单的纯文本提取，按行拼接，保留原排版
            text = page.get_text("text") or ""
            lines = [ln.rstrip() for ln in text.splitlines()]

            # 如果某一行字号明显大于其他行，当作小标题
            # 这里采用简单策略：短行（<60 字符）后紧跟空行的当作 Markdown 标题
            page_lines: list[str] = []
            for ln in lines:
                stripped = ln.strip()
                if not stripped:
                    page_lines.append("")
                    continue
                is_short_title = (
                    len(stripped) < 40
                    and not stripped.endswith((".", "。", "，", ",", "；", ";", "！", "!", "？", "?"))
                )
                if is_short_title:
                    page_lines.append(f"### {stripped}")
                else:
                    page_lines.append(stripped)

            blocks.append("\n".join(self._merge_text_lines(page_lines)))

        doc.close()

        md = "\n\n".join(blocks).strip() + "\n"
        return md

    def _merge_text_lines(self, lines: list[str]) -> list[str]:
        """把被换行断开的句子合起来（PDF 经常每行自动换行）。
        策略：非空、非标题行与下一行合并，直到遇到空行或以中文句号/英文句号结束。"""
        result: list[str] = []
        buffer: list[str] = []
        for ln in lines:
            if ln.strip() == "":
                if buffer:
                    result.append(" ".join(b.strip() for b in buffer))
                    buffer = []
                result.append("")
                continue
            if ln.startswith("#"):
                if buffer:
                    result.append(" ".join(b.strip() for b in buffer))
                    buffer = []
                result.append(ln)
                continue
            buffer.append(ln)
            if ln.rstrip().endswith((".", "。", "？", "?", "！", "!", "；", ";", ":")):
                result.append(" ".join(b.strip() for b in buffer))
                buffer = []
        if buffer:
            result.append(" ".join(b.strip() for b in buffer))
        return result
