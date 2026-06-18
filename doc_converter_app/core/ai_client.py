"""AI 客户端：封装 OpenAI 兼容接口（DeepSeek / 智谱 / 通义千问 / SiliconFlow 等都可用）。

只依赖标准库 json + urllib + ssl，不引入第三方库，避免版本冲突。
"""
from __future__ import annotations

import json
import ssl
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class AIConfig:
    base_url: str          # 例如 https://api.deepseek.com/v1
    api_key: str           # 你的 API Key
    model: str = "deepseek-chat"
    temperature: float = 0.7
    timeout: int = 120     # 秒

    def validate(self) -> str | None:
        """如果配置不完整，返回错误说明字符串；否则返回 None"""
        if not self.base_url.strip():
            return "请先填写 Base URL"
        if not self.api_key.strip():
            return "请先填写 API Key"
        if not self.model.strip():
            return "请先填写模型名称"
        return None


@dataclass
class AIResponse:
    content: str
    raw: str = ""


class AIClient:
    """通用的 OpenAI Chat Completions 客户端"""

    def __init__(self, config: AIConfig):
        self.config = config
        self._base_url = config.base_url.strip().rstrip("/")

    # ---------- 内部工具 ----------
    def _build_url(self, path: str) -> str:
        if path.startswith("/"):
            return f"{self._base_url}{path}"
        return f"{self._base_url}/{path}"

    def _post(self, path: str, payload: dict) -> dict:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            self._build_url(path),
            data=data,
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        # 创建一个允许 TLS 的上下文；对自签名证书 fallback 更宽松
        ctx = ssl.create_default_context()
        try:
            with urllib.request.urlopen(req, timeout=self.config.timeout, context=ctx) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                return json.loads(body)
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"HTTP {e.code}: {err_body[:500]}"
            ) from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"网络错误：{e.reason}") from e

    # ---------- 公开 API ----------
    def chat(self, messages: list[dict[str, str]], stream: bool = False) -> AIResponse:
        """
        发起一次聊天完成请求。

        messages 格式示例：
        [
            {"role": "system", "content": "你是一个有帮助的助手"},
            {"role": "user", "content": "你好"},
        ]
        """
        payload = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature,
            "stream": stream,
        }
        resp = self._post("/chat/completions", payload)
        try:
            content = resp["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as e:
            raise RuntimeError(f"API 返回格式异常：{resp!r}") from e
        return AIResponse(content=content, raw=json.dumps(resp, ensure_ascii=False)[:2000])

    def test_connection(self) -> tuple[bool, str]:
        """快速测试 API 是否可用。发送一条极短的消息。返回 (是否成功, 信息)"""
        try:
            self.chat([{"role": "user", "content": "Hi, 回复一句话。"}])
        except Exception as exc:  # noqa: BLE001
            return False, str(exc)
        return True, "连接成功！API 与模型正常工作。"

    # ---------- 业务层面的便捷方法 ----------
    def summarize_markdown(self, md_path: str | Path, max_chars: int = 12000) -> str:
        """读取一个 markdown 文件，生成中文摘要。"""
        text = Path(md_path).read_text(encoding="utf-8", errors="ignore").strip()
        if not text:
            return "（文档内容为空）"
        # 简单的"前后截断"策略：长文档取前 + 后各一半，确保 token 不爆
        if len(text) > max_chars:
            half = max_chars // 2
            snippet = text[:half] + "\n...[中间已省略]...\n" + text[-half:]
        else:
            snippet = text
        messages = [
            {"role": "system", "content": "你是一个严谨的中文文档助手。请用简洁、结构化的中文总结下面的文档。"},
            {"role": "user", "content": f"请总结以下文档（约 300-500 字，使用要点分点，保留关键信息）：\n\n{snippet}"},
        ]
        return self.chat(messages).content

    def keyword_qa(self, md_path: str | Path, question: str, max_chars: int = 12000) -> str:
        """根据文档内容回答用户的关键词/问题。"""
        text = Path(md_path).read_text(encoding="utf-8", errors="ignore").strip()
        if not text:
            return "（文档内容为空，无法回答。请先在「文档转换」页面转换一份文档。）"
        if len(text) > max_chars:
            half = max_chars // 2
            snippet = text[:half] + "\n...[中间已省略]...\n" + text[-half:]
        else:
            snippet = text
        messages = [
            {"role": "system", "content": "你是一个中文文档问答助手。只能根据用户提供的文档内容回答问题。如果答案不在文档中，请明确说明。"},
            {"role": "user", "content": f"文档内容如下：\n\n{snippet}\n\n——请根据上面的文档，回答下面的问题：\n\n{question}"},
        ]
        return self.chat(messages).content

    def extract_keywords(self, md_path: str | Path, top_k: int = 8, max_chars: int = 12000) -> str:
        """从文档里提取关键主题/关键词。"""
        text = Path(md_path).read_text(encoding="utf-8", errors="ignore").strip()
        if not text:
            return "（文档内容为空）"
        if len(text) > max_chars:
            half = max_chars // 2
            snippet = text[:half] + "\n...[中间已省略]...\n" + text[-half:]
        else:
            snippet = text
        messages = [
            {"role": "system", "content": "你是一个中文文档分析员。请列出文档中的关键主题词与关键词。"},
            {"role": "user", "content": f"请从以下文档中提取 {top_k} 个最重要的关键词，并简要说明每个关键词的含义。用中文、以要点形式输出：\n\n{snippet}"},
        ]
        return self.chat(messages).content


def read_text_with_limit(
    paths: Iterable[str | Path],
    max_chars_per_file: int = 8000,
) -> str:
    """读取多个文档并拼接（可选），为 AI 调用准备内容。"""
    parts: list[str] = []
    for p in paths:
        content = Path(p).read_text(encoding="utf-8", errors="ignore").strip()
        if len(content) > max_chars_per_file:
            half = max_chars_per_file // 2
            content = content[:half] + "\n...[中间已省略]...\n" + content[-half:]
        parts.append(f"=== {Path(p).name} ===\n{content}\n")
    return "\n".join(parts)
