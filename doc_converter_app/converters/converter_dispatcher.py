from __future__ import annotations

from pathlib import Path

from .converter_base import BaseConverter
from .docx_converter import DocxConverter
from .excel_converter import ExcelConverter
from .html_converter import HtmlConverter
from .pdf_converter import PdfConverter
from .ppt_converter import PptConverter
from .txt_converter import TxtConverter


ALL_CONVERTERS: list[type[BaseConverter]] = [
    DocxConverter,
    PdfConverter,
    TxtConverter,
    ExcelConverter,
    PptConverter,
    HtmlConverter,
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
