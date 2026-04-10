#!/usr/bin/env bash
# 从正方形 PNG 生成 Windows 用多尺寸 app.ico（需已安装 ImageMagick：magick）
set -euo pipefail
SRC="${1:?用法: $0 你的图标.png}"
OUT_DIR="$(cd "$(dirname "$0")/.." && pwd)/assets"
mkdir -p "$OUT"
magick "$SRC" -define icon:auto-resize=256,128,96,64,48,32,16 "$OUT/app.ico"
echo "已写入 $OUT/app.ico"
