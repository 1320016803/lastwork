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

            text = page.get_text("text") or ""
            lines = [ln.rstrip() for ln in text.splitlines()]

            # 先按空行切成「段落」
            paragraphs: list[list[str]] = []
            current: list[str] = []
            for ln in lines:
                if ln.strip() == "":
                    if current:
                        paragraphs.append(current)
                        current = []
                else:
                    current.append(ln)
            if current:
                paragraphs.append(current)

            page_lines: list[str] = []
            for para in paragraphs:
                stripped = " ".join(ln.strip() for ln in para)
                # 单行（< 40 字符且不以标点结尾）视作标题；其余视作正文并合并断行
                if len(para) == 1 and len(para[0].strip()) < 40 and not para[0].rstrip().endswith(
                    (".", "。", "，", ",", "；", ";", "！", "!", "？", "?", ":", "：")
                ):
                    page_lines.append(f"### {para[0].strip()}")
                else:
                    page_lines.append(stripped)
                page_lines.append("")

            blocks.append("\n".join(self._cleanup_lines(page_lines)))

        doc.close()

        md = "\n\n".join(blocks).strip() + "\n"
        return md

    def _cleanup_lines(self, lines: list[str]) -> list[str]:
        """去除连续空行，保持段落间只有一个空行"""
        result: list[str] = []
        prev_blank = False
        for ln in lines:
            is_blank = ln.strip() == ""
            if is_blank:
                if not prev_blank:
                    result.append("")
                prev_blank = True
            else:
                result.append(ln)
                prev_blank = False
        return result
