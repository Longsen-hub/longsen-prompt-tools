#!/bin/bash
# video-prompt-reverse 一键执行：视频 → 提示词 → 分镜脚本
# 用法：./run_all.sh <video.mp4> [输出目录]
set -e
VIDEO="$1"
OUT="${2:-/tmp/vpr_out}"
DIR="$(cd "$(dirname "$0")" && pwd)"

if [ -z "$VIDEO" ] || [ ! -f "$VIDEO" ]; then
  echo "用法: ./run_all.sh <video.mp4> [输出目录]"
  exit 1
fi

echo "========== Step1 解析（镜头切分+抽帧+转写） =========="
python3 "$DIR/step1_parse.py" "$VIDEO" "$OUT"

echo "========== Step2 视觉理解（智谱 GLM-4V） =========="
python3 "$DIR/step2_vision.py" "$OUT/parse.json" "$OUT"

echo "========== Step3 提示词逆向（DeepSeek 10段式） =========="
python3 "$DIR/step3_reverse.py" "$OUT/parse.json" "$OUT/vision.json" "$OUT"

echo "========== Step4 分镜脚本（12字段 + 自检） =========="
python3 "$DIR/step4_storyboard.py" "$OUT/parse.json" "$OUT/vision.json" "$OUT/reverse.json" "$OUT"

echo ""
echo "✅ 全链路完成，交付物："
ls -la "$OUT"/parse.json "$OUT"/vision.json "$OUT"/reverse.json "$OUT"/storyboard.md "$OUT"/selfcheck.json 2>/dev/null
