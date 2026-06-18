# 📚 文档转 Markdown · AI 助手

> 在 Windows 上一键将 **Word / PDF / TXT / Excel** 转换为 Markdown，并通过大模型做总结、关键词提取、基于文档问答。

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PySide6](https://img.shields.io/badge/GUI-PySide6-green)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

---

## ✨ 功能

### 📄 文档转换

- ✅ `.docx` → Markdown（保留标题层级、粗体/斜体、表格）
- ✅ `.pdf` → Markdown（基于 PyMuPDF，自动合并断句段落）
- ✅ `.txt` → Markdown（自动识别 UTF-8 / GBK 编码）
- ✅ `.xlsx` → Markdown（多工作表自动转为多张 Markdown 表格）
- 📂 批量转换：一次可选多个文件同时处理
- 💾 可选输出目录；默认与源文件同目录

### 🤖 AI 文档助手

- 🔑 统一的 **OpenAI 兼容接口**（DeepSeek / 智谱 GLM / 通义千问 / SiliconFlow 等皆可）
- 📝 **总结文档**：一句话提炼文档核心内容
- 🔑 **关键词提取**：自动列出文档主题词并附简短说明
- 💬 **基于文档问答**：把你的问题结合文档内容回答
- 💬 **自由对话**：没选文档时也可直接跟大模型聊天

### 🛠 其他

- 🎨 清新的白绿色 PySide6 界面
- 🔐 API Key 保存在本地 `config.json`（**不会被提交到 Git** — 已在 `.gitignore` 中忽略）
- 📜 自动记录转换历史

---

## ⚙ 环境要求

| 项目 | 最低版本 |
|------|----------|
| **Python** | 3.8 或更高 |
| **操作系统** | Windows 10 / 11（其他系统也可，只是未在 Linux/Mac 上专门测试） |

> 💡 检查你的 Python 版本：
> ```bash
> python --version
> ```

---

## 🚀 一键安装与运行

### 步骤 1：进入项目目录

```bash
cd doc_converter_app
```

### 步骤 2：创建虚拟环境（推荐，不强制）

```bash
python -m venv .venv
.venv\Scripts\activate
```

> 不创建虚拟环境也能直接装依赖，只是会把包装到全局 Python。

### 步骤 3：安装依赖

```bash
pip install -r requirements.txt
```

`requirements.txt` 中包含：

| 包 | 作用 |
|----|------|
| `PySide6` | 图形界面框架 |
| `python-docx` | 读取 `.docx` |
| `PyMuPDF` | 读取 `.pdf` |
| `openpyxl` | 读取 `.xlsx` |
| `requests` | 调用 AI API （已内置，不必额外装） |

### 步骤 4：启动程序

```bash
python main.py
```

启动后会出现主界面，里面有两个标签页：

1. **📄 文档转换** —— 选择文件 → 点击「开始转换」
2. **🤖 AI 助手** —— 填写配置 → 选择文档 → 让大模型帮你读

---

## 🧠 AI 配置说明

程序使用 **OpenAI 兼容的 Chat Completions 接口**，所以任何提供了兼容接口的平台都能用（DeepSeek、智谱 GLM、通义千问、SiliconFlow 等）。

### 三种典型平台的填写方式

| 平台 | Base URL | 模型名示例 | API Key 获取 |
|------|----------|-----------|--------------|
| **DeepSeek** | `https://api.deepseek.com/v1` | `deepseek-chat` | https://platform.deepseek.com/api_keys |
| **智谱 GLM** | `https://open.bigmodel.cn/api/paas/v4` | `glm-4-flash` | https://open.bigmodel.cn/usercenter/apikeys |
| **通义千问（兼容版）** | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-plus` | https://bailian.console.aliyun.com/ |
| **SiliconFlow** | `https://api.siliconflow.cn/v1` | `Qwen/Qwen2.5-7B-Instruct` | https://cloud.siliconflow.cn/account/ak |

### 在程序中如何配置

1. 打开程序 → 切换到「🤖 AI 助手」标签页
2. 在顶部的三个输入框里分别填入上面的 **Base URL**、**API Key**、**模型名称**
3. 点击 **💾 保存配置** → 再点 **🧪 测试连接**，提示「连接成功」即为配置完成
4. 在「2️⃣ 选择文档」处选一个 `.md`（可以是刚转换出来的，或手动选择）
5. 点 **📝 总结文档** / **🔑 提取关键词**，或在底部输入框直接提问

### ⚠ 安全提示

- **API Key 只保存在本机** `core/config.json`，不会上传到 Git
- `.gitignore` 中已经把 `config.json` 排除，放心提交项目

---

## 📖 使用示例

### 例子 1：把一份作业 Word 文档转成 Markdown

1. 打开程序 → 「📄 文档转换」
2. 点 **➕ 添加文件**，选 `我的作业.docx`
3. 点 **🚀 开始转换**
4. 几秒后在源文件同目录下得到 `我的作业.md`

### 例子 2：让 AI 总结一篇 PDF 论文

1. 先用「文档转换」把 `论文.pdf` 转成 `论文.md`
2. 切到「🤖 AI 助手」，填好 API 配置（见上表）
3. 点 **🕓 从转换历史选择**，选中刚才的论文
4. 点 **📝 总结文档**，几秒后即可看到 AI 提炼的要点

### 例子 3：基于一份 Excel 表格的内容问答

1. 先把 `数据.xlsx` 转成 Markdown
2. 在 AI 助手页选中它
3. 在底部输入框输入：「这张表里总分最高的学生是谁？」回车 → AI 会基于表格内容回答

---

## 📂 项目结构

```
doc_converter_app/
├── main.py                       # 入口：运行这个文件即可启动 GUI
├── requirements.txt              # 依赖清单
├── converters/
│   ├── converter_base.py         # 转换器基类（自定义新格式可继承）
│   ├── converter_dispatcher.py   # 根据扩展名自动选择转换器
│   ├── docx_converter.py         # docx → md
│   ├── pdf_converter.py          # pdf → md
│   ├── txt_converter.py          # txt → md
│   └── excel_converter.py        # xlsx → md
├── core/
│   ├── config_manager.py         # 配置与历史记录持久化
│   └── ai_client.py              # OpenAI 兼容接口封装
└── ui/
    ├── style_manager.py          # 白绿色主题样式
    └── main_window.py            # 主窗口（转换页 + AI 页）
```

> 运行后会自动生成：
> - `core/config.json` —— 保存的 API 配置
> - `core/history.json` —— 转换历史

---

## 🛠 常见问题 FAQ

### Q1：启动程序时提示「ModuleNotFoundError: No module named 'PySide6'」

> 没装依赖，执行：
> ```bash
> pip install -r requirements.txt
> ```

### Q2：测试连接失败 / 报错 HTTP 401 / Invalid authentication

检查以下三点：

1. **API Key 是否正确**（注意前后不要有空格）
2. **Base URL 是否带 `/v1` 后缀**，不同平台要求不一样（详见上表）
3. 模型名是否对应平台支持的模型（例如 DeepSeek 的模型名必须是 `deepseek-chat`）

### Q3：中文显示乱码？

请确认终端为 UTF-8（推荐 Windows Terminal / PowerShell 7）。程序内部写入 `.md` 文件时统一使用 UTF-8，不会乱码。

### Q4：PDF 里的图片 / 复杂公式能识别吗？

目前的 PDF 转换器只做 **文本提取**，无法识别图片和复杂公式。想让 AI 理解图片可以后续扩展 OCR（例如百度 OCR、CNOCR）。

### Q5：生成的 `.md` 文件在哪里？

默认与源文件**同目录**。想集中保存，可以在「文档转换」页顶部指定**输出目录**。

### Q6：想清理 API Key？

直接删除 `core/config.json` 文件即可，下次打开程序会重新生成空配置。或者在输入框里把内容清空，再点「保存配置」。

---

## 📜 License

MIT License —— 随便用，随便改。

---

## 🙋 反馈与扩展

如果你想进一步扩展，以下是几个方向：

- [ ] 支持更多格式：`.html` / `.rtf` / `.epub`
- [ ] 长文档分段：用「向量索引 + 片段检索」做真正的 RAG
- [ ] 支持 OCR 识别图片 PDF
- [ ] 用 PyInstaller 打包成 `.exe`，免安装双击运行
- [ ] 增加暗黑主题

欢迎把你的文档转换 / AI 心得分享到 README 里！
