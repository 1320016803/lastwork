from __future__ import annotations

import re
import urllib.parse
from html.parser import HTMLParser

import requests

from pathlib import Path
from .converter_base import BaseConverter


class _HtmlToMarkdown(HTMLParser):
    """将 HTML 内容转换为 Markdown 格式的解析器"""

    def __init__(self) -> None:
        super().__init__()
        self._result: list[str] = []
        self._tag_stack: list[str] = []
        self._in_pre = False
        self._in_code = False
        self._current_href: str | None = None
        self._list_stack: list[tuple[str, int]] = []  # (type, index)
        self._ignore_data = False
        self._buffer: str = ""
        self._table_rows: list[list[str]] = []
        self._current_row: list[str] = []
        self._in_cell = False
        self._is_header_row = False
        self._first_table = True

    # ---------- 公共接口 ----------

    def get_markdown(self) -> str:
        """返回转换后的 Markdown 文本"""
        self._flush()
        return "\n".join(self._result).strip() + "\n" if self._result else ""

    # ---------- 标签处理 ----------

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attr_dict = {k: v for k, v in attrs if v is not None}

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._flush()
            level = int(tag[1])
            self._buffer = "#" * level + " "
            self._tag_stack.append(tag)

        elif tag == "p":
            self._flush()
            self._tag_stack.append(tag)

        elif tag == "br":
            self._flush()
            self._result.append("")

        elif tag in ("strong", "b"):
            self._buffer += "**"

        elif tag in ("em", "i"):
            self._buffer += "*"

        elif tag == "code":
            self._in_code = True
            if not self._in_pre:
                self._buffer += "`"

        elif tag == "pre":
            self._flush()
            self._in_pre = True
            self._result.append("```")

        elif tag == "blockquote":
            self._flush()
            self._tag_stack.append(tag)
            self._buffer = "> "

        elif tag in ("ul", "ol"):
            self._flush()
            list_type = "ol" if tag == "ol" else "ul"
            self._list_stack.append((list_type, 0))

        elif tag == "li":
            self._flush()
            if self._list_stack:
                list_type, idx = self._list_stack[-1]
                idx += 1
                self._list_stack[-1] = (list_type, idx)
                indent = "  " * (len(self._list_stack) - 1)
                if list_type == "ol":
                    self._buffer = f"{indent}{idx}. "
                else:
                    self._buffer = f"{indent}- "

        elif tag == "a":
            href = attr_dict.get("href", "")
            self._current_href = href
            self._tag_stack.append(tag)

        elif tag == "img":
            alt = attr_dict.get("alt", "")
            src = attr_dict.get("src", "")
            self._buffer += f"![{alt}]({src})"

        elif tag == "hr":
            self._flush()
            self._result.append("---")

        elif tag == "table":
            self._flush()
            self._table_rows = []
            self._first_table = True

        elif tag == "thead":
            self._is_header_row = True

        elif tag == "tr":
            self._current_row = []

        elif tag in ("td", "th"):
            self._in_cell = True
            self._buffer = ""

        elif tag in ("div", "section", "article", "main", "header", "footer", "nav", "aside"):
            # 块级容器标签，换行但不额外处理
            self._flush()

        elif tag in ("script", "style"):
            self._ignore_data = True

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._flush()
            self._tag_stack = [t for t in self._tag_stack if t != tag]

        elif tag == "p":
            self._flush()
            self._result.append("")
            self._tag_stack = [t for t in self._tag_stack if t != tag]

        elif tag in ("strong", "b"):
            self._buffer += "**"

        elif tag in ("em", "i"):
            self._buffer += "*"

        elif tag == "code":
            self._in_code = False
            if not self._in_pre:
                self._buffer += "`"

        elif tag == "pre":
            self._flush()
            self._in_pre = False
            self._result.append("```")
            self._result.append("")

        elif tag == "blockquote":
            self._flush()
            self._tag_stack = [t for t in self._tag_stack if t != tag]
            self._result.append("")

        elif tag in ("ul", "ol"):
            self._flush()
            if self._list_stack:
                self._list_stack.pop()

        elif tag == "li":
            self._flush()

        elif tag == "a":
            self._flush()
            href = self._current_href or ""
            if self._current_href and self._last_flushed_text:
                # 如果链接文本和href相同，简化显示
                last_idx = len(self._result) - 1
                if last_idx >= 0:
                    text = self._result[last_idx].strip()
                    if text and text != href:
                        self._result[last_idx] = f"[{text}]({href})"
                    elif text == href:
                        self._result[last_idx] = f"<{href}>"
            self._current_href = None
            self._tag_stack = [t for t in self._tag_stack if t != tag]

        elif tag in ("td", "th"):
            self._flush()
            cell_text = (self._last_flushed_text or "").strip()
            self._current_row.append(cell_text)
            self._in_cell = False

        elif tag == "tr":
            if self._current_row:
                self._table_rows.append(self._current_row[:])
                self._current_row = []
            if self._is_header_row:
                self._is_header_row = False

        elif tag == "table":
            self._render_table()
            self._table_rows = []

        elif tag in ("script", "style"):
            self._ignore_data = False

    def handle_data(self, data: str) -> None:
        if self._ignore_data:
            return
        if self._in_cell:
            self._buffer += data
        else:
            self._buffer += data

    def handle_entityref(self, name: str) -> None:
        entities = {
            "amp": "&", "lt": "<", "gt": ">", "quot": '"',
            "apos": "'", "nbsp": " ", "mdash": "—",
            "ndash": "–", "hellip": "…",
        }
        self._buffer += entities.get(name, f"&{name};")

    def handle_charref(self, name: str) -> None:
        try:
            if name.startswith("x"):
                codepoint = int(name[1:], 16)
            else:
                codepoint = int(name)
            self._buffer += chr(codepoint)
        except (ValueError, OverflowError):
            self._buffer += f"&#{name};"

    # ---------- 内部方法 ----------

    _last_flushed_text: str = ""

    def _flush(self) -> None:
        text = self._buffer.strip("\r\n")
        if text:
            self._last_flushed_text = text
            if self._in_pre or self._in_code:
                self._result.append(text)
            else:
                # 清理多余空白
                cleaned = re.sub(r"[ \t]+", " ", text).strip()
                if cleaned:
                    self._result.append(cleaned)
        self._buffer = ""

    def _render_table(self) -> None:
        """将解析到的表格行渲染为 Markdown 表格"""
        if not self._table_rows:
            return

        rows = self._table_rows
        max_cols = max((len(r) for r in rows), default=0)
        # 规范化每行列数
        for row in rows:
            while len(row) < max_cols:
                row.append("")

        if len(rows) < 1:
            return

        # 第一行作为表头
        header = rows[0]
        sep = ["---"] * max_cols

        lines = [
            "| " + " | ".join(header) + " |",
            "| " + " | ".join(sep) + " |",
        ]
        for data_row in rows[1:]:
            lines.append("| " + " | ".join(data_row) + " |")

        self._result.extend(lines)
        self._result.append("")


class UrlConverter(BaseConverter):
    """
    网页链接 → Markdown 转换器
    
    支持以 URL 作为输入（传入 .url 后缀的虚拟路径），
    或通过 convert_url() 方法直接传入网址。
    
    使用 requests 抓取网页 HTML，再用内置 HTML 解析器转换为 Markdown。
    """

    SUPPORTED_EXT = (".url",)

    # 默认请求超时（秒）
    REQUEST_TIMEOUT = 30

    # 用户代理
    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    @staticmethod
    def fetch_html(url: str, timeout: int | None = None) -> str:
        """
        抓取指定 URL 的网页 HTML 内容。
        
        :param url: 目标网址
        :param timeout: 请求超时秒数，默认使用 REQUEST_TIMEOUT
        :return: 网页 HTML 源码
        :raise ValueError: URL 格式无效
        :raise requests.RequestException: 请求失败
        """
        url = url.strip()
        if not url:
            raise ValueError("URL 不能为空")
        
        # 补全协议前缀
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        headers = {
            "User-Agent": UrlConverter.USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }

        resp = requests.get(url, headers=headers, timeout=timeout or UrlConverter.REQUEST_TIMEOUT, allow_redirects=True)
        resp.raise_for_status()
        
        # 尝试检测编码
        resp.encoding = resp.apparent_encoding or "utf-8"
        return resp.text

    @staticmethod
    def html_to_markdown(html_content: str) -> str:
        """将 HTML 字符串转换为 Markdown 格式"""
        parser = _HtmlToMarkdown()
        parser.feed(html_content)
        return parser.get_markdown()

    def _to_markdown(self, src: Path) -> str:
        """
        当输入路径是 .url 文件时，读取其中的 URL 并转换。
        也支持直接传入包含 URL 的文件。
        """
        content = src.read_text(encoding="utf-8").strip()
        
        # 判断内容是纯URL还是可能是一个HTML/文本文件
        url = content.splitlines()[0].strip() if content else ""
        
        if not url.startswith(("http://", "https://")):
            # 可能是本地文件或非URL内容
            raise ValueError(f"无效的网页链接: {url[:50]}...")

        html_content = self.fetch_html(url)
        markdown = self.html_to_markdown(html_content)
        
        # 在开头添加来源信息
        source_info = f"> 来源: {url}\n>\n"
        return source_info + markdown

    def convert_url(self, url: str, output_dir: str | Path | None = None, filename: str | None = None) -> str:
        """
        直接将网页 URL 转换为 Markdown 文件。
        
        :param url: 要转换的网页链接
        :param output_dir: 输出目录，默认当前工作目录
        :param filename: 输出文件名（不含扩展名），默认从URL生成
        :return: 生成的 .md 文件的绝对路径
        """
        from urllib.parse import urlparse
        
        parsed = urlparse(url)
        domain = parsed.netloc.replace(":", "_")
        path = parsed.path.rstrip("/").replace("/", "_") or "index"
        
        if filename is None:
            safe_name = (domain + path).strip("_") or "webpage"
            # 清理非法字符
            safe_name = re.sub(r'[<>:"/\\|?*]', '_', safe_name)[:100]
        else:
            safe_name = filename

        if output_dir is None:
            target_dir = Path.cwd()
        else:
            target_dir = Path(output_dir)
            target_dir.mkdir(parents=True, exist_ok=True)

        out_path = target_dir / f"{safe_name}.md"

        html_content = self.fetch_html(url)
        markdown = self.html_to_markdown(html_content)

        # 添加来源信息
        source_info = f"> **来源**: [{url}]({url})\n>\n> **抓取时间**: 自动\n>\n"
        final_md = source_info + markdown

        out_path.write_text(final_md, encoding="utf-8")
        return str(out_path.resolve())
