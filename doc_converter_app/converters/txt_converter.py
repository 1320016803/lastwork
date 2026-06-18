from __future__ import annotations

from pathlib import Path

from .converter_base import BaseConverter


class TxtConverter(BaseConverter):
    SUPPORTED_EXT = (".txt", ".md")

    def _to_markdown(self, src: Path) -> str:
        # 尝试多种常见编码
        for enc in ("utf-8", "utf-8-sig", "gbk", "gb18030", "big5"):
            try:
                text = src.read_text(encoding=enc)
                break
            except UnicodeDecodeError:
                continue
        else:
            # 最后一招：忽略错误
            text = src.read_text(encoding="utf-8", errors="ignore")

        lines = text.splitlines()
        cleaned: list[str] = []
        for ln in lines:
            cleaned.append(ln.rstrip())

        return "\n".join(cleaned).strip() + "\n"
