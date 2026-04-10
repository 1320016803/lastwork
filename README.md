<div align="center">

<img src="assets/readme-mascot.png" width="200" alt="应用图标占位图（可替换）"/>

## ⏰ hh计时器 ⏰

**cute-timer** · Python · PySide6

超可爱的桌面小计时器，支持25分钟专注计时，可快速调整时长，界面圆润可爱，适合学习工作时使用。

**克隆地址**：`https://gitee.com/mengmengdongdong/cute-timer`

</div>

### 界面预览

运行 `python main.py` 后，可将窗口截图保存为 `assets/readme-screenshot.png`，并在此处增加一行：  
`<img src="assets/readme-screenshot.png" width="480" alt="界面截图"/>`

---

## 简介与克隆说明

本仓库设计为在 Gitee 上 **公开**：公开仓库下 `git clone` **不需要** Gitee 账号或密码。若克隆时仍被要求登录，多半是仓库被设成了私有，请维护者在 Gitee 改为公开（见文末「维护者」一句）。

**路径说明**：下文中的 **`cute-timer`** 表示「克隆到本机后的项目文件夹名」，通常与 **仓库名** 一致。若你的仓库名不同，请把所有路径里的 `cute-timer` 换成你的实际文件夹名。

---

## 人类读者：怎么运行

### 第一次使用：先把项目下载到电脑

1. 安装 **Python 3.10+**（安装时勾选 *pip*），并安装 **Git**（Windows 可从 <https://git-scm.com/download/win> 获取；也可用 `winget install Git.Git` 等，以用户环境为准）。
2. 打开 **终端**（Windows 可搜「PowerShell」）。
3. 进入你想存放项目的目录（例如用户主目录），执行：

```bash
git clone https://gitee.com/mengmengdongdong/cute-timer.git
cd cute-timer
```

4. 再继续下面「安装依赖」步骤。

### 安装依赖与启动

1. **确认当前在项目文件夹里**（终端里 `pwd` 或看路径末尾是否是项目名）。
2. 在本目录安装依赖：  
   - **推荐**：`python3 -m venv .venv`，再执行  
     - Windows：`.venv\Scripts\activate`  
     - macOS / Linux：`source .venv/bin/activate`  
     然后：`python -m pip install -r requirements.txt`  
   - 若系统未限制全局 pip，也可直接：`python -m pip install -r requirements.txt`  
   - **在中国大陆且下载很慢时**，可临时加清华镜像：  
     `python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`
3. 启动：`python main.py`（macOS / Linux 或 Windows 调试）  
   窗口与任务栏图标来自 `assets/app.ico`（随仓库提供，可替换）。  
4. Windows 想减少黑窗：可用 `pythonw main.py`、`pyw -3 main.py`，或双击 `main.pyw`（依赖系统 `.pyw` 关联）。也可双击同目录下的 `run_app.bat`（优先 `pyw` / `pythonw`）。

---

## 复制给 WorkBuddy / OpenClaw 的一句话

下面这段是给人类**直接复制粘贴**用的「指挥句」；具体命令在下一节 **「给智能体的安装剧本」** 里。

**安装时请发送：**

```text
请打开（或克隆）公开仓库 https://gitee.com/mengmengdongdong/cute-timer ，阅读 README 里的「给智能体的安装剧本」，根据我当前操作系统逐步执行。克隆公开仓库时不要向用户索要 Gitee 账号或密码。若某一步失败，按 README 里的说明降级处理（尤其是桌面快捷方式）。最后请明确告诉我：项目目录路径、用哪条命令启动（若用了 venv，要写全 venv 里的 python/pythonw 路径）。
```

**卸载时请发送：**

```text
请阅读仓库 https://gitee.com/mengmengdongdong/cute-timer 的 README 中「给智能体的卸载剧本」，在我当前操作系统下按步骤执行，并在完成后告诉我删除了哪些路径。若本地文件夹名与仓库名不一致，请按实际文件夹名删除。
```

若智能体已经打开你本机的克隆目录，可把「打开（或克隆）公开仓库 …」改成：「请阅读本仓库 README 中的「给智能体的安装剧本」……」。

---

## 给智能体的安装剧本

> **受众**：OpenClaw、WorkBuddy、Cursor Agent 等自动化助手。请根据**当前操作系统**选择对应分支，在用户同意的前提下执行命令。  
> **固定目录名（默认）**：项目克隆到用户主目录下的 **`cute-timer`**（与卸载剧本一致）。  
> **克隆与凭据（重要）**：本仓库以 **Gitee 公开仓库** 方式提供。**只读克隆 `git clone https://gitee.com/mengmengdongdong/cute-timer.git` 在仓库为公开时不需要、也不应要求用户提供 Gitee 用户名或密码。**  
> - **禁止**向用户索取 Gitee 登录密码或私人令牌来完成克隆。  
> - 若 `git clone` 失败并提示需要认证，说明远程可能仍为**私有**或 URL 错误：请明确告知用户「需由维护者将仓库改为公开」，**不要**让用户把密码发给你。  
> - 为避免交互式卡住，克隆命令建议使用非交互环境变量（见下方示例中的 `GIT_TERMINAL_PROMPT=0`；Windows PowerShell 用 `$env:GIT_TERMINAL_PROMPT = '0'`）。  
> **快捷方式**：部分环境无法在用户桌面创建 `.lnk` / `.desktop`；若失败，完成克隆与 `pip install` 即可，并告知用户如何运行 `main.py`。  
> **中国大陆网络**：若 `pip` 明显缓慢或失败，再按下文「可选」为国内 PyPI 镜像；勿对境外网络默认改源。

### 0. 识别平台

- 若在 **Windows**（`os.name == 'nt'` 或存在 `WINDIR` 环境变量），执行 **「Windows」** 小节。
- 若在 **macOS**，执行 **「macOS」** 小节。
- 若在 **Linux** 或其它 Unix，执行 **「Linux」** 小节。

### 1. 检查 Git

执行 `git --version`。若失败：提示用户安装 Git（Windows 可从 <https://git-scm.com/download/win> 获取；也可用 `winget install Git.Git` 等，以用户环境为准），安装完成后重新执行本剧本。

### 2. 检查 Python 与 pip

执行 `python3 --version` 或 `python --version`（Windows 上可再试 `py -3 --version`）。需 **Python 3.10+**。  
执行 `python3 -m pip --version` 或 `python -m pip --version`（Windows 若 `python` 不可用，再试 `py -3 -m pip --version`）。若失败，引导用户修复 Python 安装（勾选 pip）或使用 `python -m ensurepip`。  
后续安装依赖时，**与通过版本检查的解释器保持一致**（例如 Windows 上若只用 `py -3` 能通过检查，则使用 `py -3 -m pip install -r requirements.txt`）。

### 3. 克隆仓库（公开仓库、无需 Gitee 密码）

**HTTPS 克隆地址**：`https://gitee.com/mengmengdongdong/cute-timer.git`

**Windows（PowerShell 示例）** — 将 `$Repo` 设为实际文件夹名（默认 `cute-timer`）：

```powershell
$env:GIT_TERMINAL_PROMPT = '0'
$Repo = "cute-timer"
$dest = Join-Path $env:USERPROFILE $Repo
if (Test-Path $dest) {
  Set-Location $dest
  if (Test-Path .git) { git pull } else { Set-Location ..; Remove-Item -Recurse -Force $dest; git -c credential.helper= clone "https://gitee.com/mengmengdongdong/cute-timer.git" $dest; Set-Location $dest }
} else {
  git -c credential.helper= clone "https://gitee.com/mengmengdongdong/cute-timer.git" $dest
  Set-Location $dest
}
python -m pip install -r requirements.txt
```

**macOS / Linux（bash 示例）** — 将 `REPO` 设为实际文件夹名：

```bash
export GIT_TERMINAL_PROMPT=0
REPO="cute-timer"
DEST="$HOME/$REPO"
if [ -d "$DEST" ]; then
  cd "$DEST" || exit 1
  if [ -d .git ]; then git pull; else cd .. && rm -rf "$DEST" && git -c credential.helper= clone "https://gitee.com/mengmengdongdong/cute-timer.git" "$DEST" && cd "$DEST" || exit 1; fi
else
  git -c credential.helper= clone "https://gitee.com/mengmengdongdong/cute-timer.git" "$DEST"
  cd "$DEST"
fi
python3 -m pip install -r requirements.txt
```

（若系统只有 `python` 无 `python3`，请改用 `python -m pip`。）

**（可选）中国大陆网络：为 pip 使用国内 PyPI 镜像**  
- **何时加**：用户或网络明显在中国大陆，且 `pip install` **很慢、反复超时或失败**时再使用；**不要**默认给境外网络改源。  
- **做法（仅本次安装生效，不改全局配置）**：在原有 `pip install` 命令末尾增加 `-i` 与镜像地址，例如清华源：  
  `python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`  
  其它常用镜像（任选其一即可）：阿里云 `https://mirrors.aliyun.com/pypi/simple/`、中科大 `https://pypi.mirrors.ustc.edu.cn/simple/`。  
- Windows / macOS / Linux 命令相同；若在 **venv** 里安装，请用该 venv 下的 `python -m pip … -i …`。  
- 若用户明确要求**长期**默认走国内源，可再执行 `pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple`（需用户知情同意）。

**若 `pip install` 报错 externally-managed-environment（常见于 Homebrew Python）**：在项目目录执行 `python3 -m venv .venv`（Windows 可用 `py -3 -m venv .venv`），再使用 `.venv/bin/python -m pip install -r requirements.txt`（Windows 为 `.venv\Scripts\python.exe -m pip ...`）。**此后启动程序必须用同一 venv 里的解释器**，例如：  
- Windows：`"%USERPROFILE%\cute-timer\.venv\Scripts\pythonw.exe"` + 工作目录为项目根，参数填 `main.py` 的绝对路径；或在项目目录执行 `.venv\Scripts\pythonw.exe main.py`。  
- macOS / Linux：`"$HOME/cute-timer/.venv/bin/python" main.py`。  
桌面快捷方式若已创建，应将 **`TargetPath` 改为上述 venv 内的 `pythonw.exe` / `python`**，不要仍指向系统全局 `pythonw`。

### 4. （可选）桌面快捷方式 — 成功则做，失败则跳过

**Windows**：在能使用 PowerShell 且能访问用户桌面的环境中，可尝试用 `WScript.Shell` 创建 `.lnk`：

1. 解析 `pythonw.exe` 路径：可执行 `where.exe pythonw` 或 `Get-Command pythonw`；若无，试 `pyw` 与 `where.exe pyw`。
2. `TargetPath` = 上一步得到的 `pythonw.exe`（或 `pyw.exe`）；**若依赖装在项目内 `.venv` 里**，则改为 `"%USERPROFILE%\cute-timer\.venv\Scripts\pythonw.exe"`。  
3. `Arguments` = `"<USERPROFILE>\cute-timer\main.py"`（请展开为绝对路径并保留引号）。  
4. `WorkingDirectory` = `<USERPROFILE>\cute-timer`。  
5. `IconLocation` = `<USERPROFILE>\cute-timer\assets\app.ico`（仓库内已带多尺寸 Windows 图标）。  
6. 快捷方式文件名建议：`hh计时器.lnk`，放在 `[Environment]::GetFolderPath('Desktop')` 对应目录。

PowerShell 模板（需自行替换 `$PythonW`）：

```powershell
$WshShell = New-Object -ComObject WScript.Shell
$Desktop = [Environment]::GetFolderPath('Desktop')
$Repo = "cute-timer"
$Shortcut = $WshShell.CreateShortcut("$Desktop\hh计时器.lnk")
$Shortcut.TargetPath = $PythonW
$Shortcut.Arguments = "`"$env:USERPROFILE\$Repo\main.py`""
$Shortcut.WorkingDirectory = "$env:USERPROFILE\$Repo"
$Shortcut.IconLocation = "$env:USERPROFILE\$Repo\assets\app.ico"
$Shortcut.Save()
```

**macOS**：可向 `~/Desktop` 写入一个可执行的小脚本，调用 `python3 "$HOME/cute-timer/main.py"`，并 `chmod +x`；或提示用户在访达中手动拖放创建别名。

**Linux**：可在 `~/Desktop` 创建 `.desktop` 文件，`Exec` 指向 `python3 /home/<用户>/cute-timer/main.py`，并赋予可执行权限（具体路径按实际用户主目录填写）。

若任一步报错或与沙箱/权限冲突，**跳过本节**，并明确告知用户：已进入项目目录后运行 `pythonw main.py`（Windows）或 `python3 main.py` 即可。

### 5. 安装完成检查

在**项目根目录**执行一次 `python main.py`（或 Windows 无控制台用 `pythonw main.py` / `pyw -3 main.py`）。**若第 3 步使用了 venv**，此处应改为 `.venv\Scripts\python.exe main.py`（Windows）或 `.venv/bin/python main.py`（Unix）。应弹出图形窗口。若失败，根据报错检查 PySide6 是否安装成功、显示环境是否可用。

---

## 给智能体的卸载剧本

> **受众**：同上。按平台删除**项目目录**与**固定名称的快捷方式**（若曾创建成功）。操作前请确认路径属于当前用户且用户授权删除。

### 固定约定

- 项目目录：**`%USERPROFILE%\cute-timer`**（Windows）或 **`$HOME/cute-timer`**（macOS / Linux）。  
- Windows 桌面快捷方式文件名：**`hh计时器.lnk`**（若安装时用了其它名称，应与当时保持一致）。

### Windows（PowerShell 示例）

```powershell
$Repo = "cute-timer"
$proj = Join-Path $env:USERPROFILE $Repo
if (Test-Path $proj) { Remove-Item -Recurse -Force $proj }

$desk = [Environment]::GetFolderPath('Desktop')
$lnk = Join-Path $desk "hh计时器.lnk"
if (Test-Path $lnk) { Remove-Item -Force $lnk }
```

### macOS / Linux（bash 示例）

```bash
REPO="cute-timer"
rm -rf "$HOME/$REPO"
```

若安装剧本曾在桌面创建过启动脚本或 `.desktop` 文件，请删除**当时写入的同一文件名**。若无法确定，至少删除项目目录并告知用户自行移除桌面上的相关入口。

### 说明

- 一般不卸载全局/用户级已安装的 `PySide6`，以免影响其它项目；若用户要求彻底清理，可再执行 `python -m pip uninstall PySide6`（谨慎）。

---

## 维护者（仅此一句）

请在本仓库的 Gitee 页面：**管理 → 基本设置 → 是否开源**，将仓库设为 **公开**，这样学生与其它电脑用 `git clone` 时**不会**被系统要求输入 Gitee 账号密码。若保持私有，则 HTTPS 克隆必然需要有权账号登录，智能体无法代你绕过这一点。

---

## 相关示例

完整示例应用（含加密小工具）可参考：[caesar-desktop-lab](https://gitee.com/thiswind/caesar-desktop-lab)（结构与 README 写法与本模板对齐，便于对照修改）。
