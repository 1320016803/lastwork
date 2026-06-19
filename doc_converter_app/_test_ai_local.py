"""不依赖网络的 AI 客户端测试：使用本地 http.server 模拟 API 响应。"""
import io
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

# Windows cmd 下强制用 UTF-8 输出，避免 emoji 等字符引发 UnicodeEncodeError
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

APP_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(APP_DIR))

from core.ai_client import AIConfig, AIClient  # noqa: E402

MOCK_RESPONSE = {
    "id": "mock-id",
    "choices": [
        {"message": {"role": "assistant", "content": "✅ 这是来自 mock API 的回答！内容已正确解析。"}}
    ],
}


class MockHandler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8")
        data = json.loads(body)
        msg = f"[收到请求] model={data.get('model')}, messages_n={len(data.get('messages', []))}"
        print("  " + msg)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        body_bytes = json.dumps(MOCK_RESPONSE).encode("utf-8")
        self.send_header("Content-Length", str(len(body_bytes)))
        self.end_headers()
        self.wfile.write(body_bytes)

    def log_message(self, *args, **kwargs) -> None:
        pass  # 禁用默认日志，避免刷屏


def main() -> int:
    print(">>> 启动本地 mock API 服务器…")
    server = HTTPServer(("127.0.0.1", 0), MockHandler)
    port = server.server_port
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()

    cfg = AIConfig(
        base_url=f"http://127.0.0.1:{port}",
        api_key="sk-test-123",
        model="mock-model",
    )
    client = AIClient(cfg)

    print(">>> 测试 chat()…")
    resp = client.chat([{"role": "user", "content": "你好"}])
    assert "mock API" in resp.content, f"响应内容异常：{resp.content!r}"
    print("    ✅ chat() OK →", resp.content[:60])

    print(">>> 测试 summarize_markdown()（准备一个小的 md 文件）…")
    tmp_md = APP_DIR / "_sample_outputs" / "示例文档.md"
    if not tmp_md.exists():
        tmp_md.parent.mkdir(parents=True, exist_ok=True)
        tmp_md.write_text(
            "# 示例文档\n\n这是一个示例文档，包含一些普通的中文内容。\n\n用来测试 AI 总结功能。\n",
            encoding="utf-8",
        )
    resp2 = client.summarize_markdown(str(tmp_md))
    assert resp2, "总结不应为空"
    print("    ✅ summarize_markdown() OK →", resp2[:60])

    print(">>> 测试 extract_keywords()…")
    resp3 = client.extract_keywords(str(tmp_md))
    assert resp3, "关键词提取不应为空"
    print("    ✅ extract_keywords() OK →", resp3[:60])

    print(">>> 测试 keyword_qa()…")
    resp4 = client.keyword_qa(str(tmp_md), "这篇文档是干什么的？")
    assert resp4, "QA 不应为空"
    print("    ✅ keyword_qa() OK →", resp4[:60])

    print("\n=== 全部通过 ✅ ===")
    server.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
