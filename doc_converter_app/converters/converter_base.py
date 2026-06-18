from __future__ import annotations

from pathlib import Path


class BaseConverter:
    """所有文件格式转换器的基类"""

    # 支持的文件扩展名（小写，带点）
    SUPPORTED_EXT: tuple[str, ...] = ()

    def convert(self, input_path: str | Path, output_dir: str | Path | None = None) -> str:
        """
        将文档转换为 Markdown。

        :param input_path: 源文件路径
        :param output_dir: 输出目录。为 None 时保存到源文件同目录。
        :return: 生成的 .md 文件的绝对路径
        """
        src = Path(input_path).resolve()
        if not src.exists():
            raise FileNotFoundError(f"文件不存在: {src}")
        ext = src.suffix.lower()
        if ext not in self.SUPPORTED_EXT:
            raise ValueError(f"本转换器不支持 {ext} 格式")

        if output_dir is None:
            target_dir = src.parent
        else:
            target_dir = Path(output_dir)
            target_dir.mkdir(parents=True, exist_ok=True)

        out_path = target_dir / (src.stem + ".md")
        md_content = self._to_markdown(src)

        out_path.write_text(md_content, encoding="utf-8")
        return str(out_path)

    def _to_markdown(self, src: Path) -> str:
        """子类必须实现：读取 src 并返回 Markdown 字符串"""
        raise NotImplementedError
