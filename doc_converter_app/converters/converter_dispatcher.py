from __future__ import annotations

from pathlib import Path

from .converter_base import BaseConverter
from .docx_converter import DocxConverter
from .excel_converter import ExcelConverter
from .html_converter import HtmlConverter
from .pdf_converter import PdfConverter
from .ppt_converter import PptConverter
from .txt_converter import TxtConverter
from .url_converter import UrlConverter


ALL_CONVERTERS: list[type[BaseConverter]] = [
    DocxConverter,
    PdfConverter,
    TxtConverter,
    ExcelConverter,
    PptConverter,
    HtmlConverter,
    UrlConverter,
]


def _build_extension_map() -> dict[str, type[BaseConverter]]:
    mapping: dict[str, type[BaseConverter]] = {}
    for cls in ALL_CONVERTERS:
        for ext in cls.SUPPORTED_EXT:
            mapping.setdefault(ext, cls)
    return mapping


EXTENSION_MAP = _build_extension_map()


def get_converter(file_path: str | Path) -> BaseConverter:
    """根据文件扩展名返回合适的转换器实例"""
    ext = Path(file_path).suffix.lower()
    if ext not in EXTENSION_MAP:
        raise ValueError(f"暂不支持的文件格式: {ext or '（无扩展名）'}")
    return EXTENSION_MAP[ext]()


def convert_file(file_path: str | Path, output_dir: str | Path | None = None) -> str:
    """统一入口：把任意支持的文档转换成 Markdown，返回生成的 .md 路径"""
    converter = get_converter(file_path)
    return converter.convert(file_path, output_dir)


def supported_extensions() -> list[str]:
    return sorted(set(EXTENSION_MAP.keys()))


def convert_url(url: str, output_dir: str | Path | None = None, filename: str | None = None) -> str:
    """
    将网页链接转换为 Markdown 文件。

    :param url: 目标网页 URL
    :param output_dir: 输出目录，默认当前工作目录
    :param filename: 输出文件名（不含 .md 后缀），默认从 URL 自动生成
    :return: 生成的 .md 文件的绝对路径
    """
    converter = UrlConverter()
    return converter.convert_url(url, output_dir, filename)

