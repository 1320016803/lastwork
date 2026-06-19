from __future__ import annotations

from pathlib import Path

from markdownify import markdownify as md

from .converter_base import BaseConverter


class HtmlConverter(BaseConverter):
    SUPPORTED_EXT = (".html", ".htm")

    def _to_markdown(self, src: Path) -> str:
        for enc in ("utf-8", "utf-8-sig", "gbk", "gb18030", "big5"):
            try:
                html_text = src.read_text(encoding=enc)
                break
            except UnicodeDecodeError:
                continue
        else:
            html_text = src.read_text(encoding="utf-8", errors="ignore")

        md_text = md(
            html_text,
            heading_style="ATX",
            bullets="-",
            strong_em_symbol="*",
            sub_symbol="",
            sup_symbol="",
        )

        cleaned_lines: list[str] = []
        for line in md_text.splitlines():
            cleaned_lines.append(line.rstrip())

        result = "\n".join(self._collapse_blank_lines(cleaned_lines)).strip() + "\n"
        return result

    def _collapse_blank_lines(self, lines: list[str]) -> list[str]:
        result: list[str] = []
        blank_count = 0
        for line in lines:
            if line.strip() == "":
                blank_count += 1
                if blank_count <= 2:
                    result.append("")
            else:
                blank_count = 0
                result.append(line)
        return result
