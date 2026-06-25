#!/bin/bash
# 简化版录制脚本 - 录制整个屏幕
# 无需 xdotool，直接录制 :0.0

set -e

VIDEO_DIR="/home/zj/PycharmProjects/AutoDataGen/videos"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
VIDEO_FILE="${VIDEO_DIR}/demo_${TIMESTAMP}.mp4"
DURATION="${1:-120}"
FPS=30

mkdir -p "$VIDEO_DIR"

echo "=========================================="
echo "录制配置"
echo "=========================================="
echo "视频文件: $VIDEO_FILE"
echo "录制时长: ${DURATION} 秒"
echo "帧率: ${FPS} FPS"
echo "=========================================="

export DISPLAY=:0

echo "开始录制... (按 Ctrl+C 停止)"

# 使用 ffmpeg 录制整个屏幕
ffmpeg -y -f x11grab -r $FPS -video_size 1920x1080 -i :0.0 \
  -vcodec libx264 -preset fast -crf 23 \
  -t $DURATION \
  "$VIDEO_FILE" 2>/dev/null &

FFMPEG_PID=$!
echo "ffmpeg PID: $FFMPEG_PID"

# 等待
sleep $DURATION

# 结束
kill $FFMPEG_PID 2>/dev/null || true
wait $FFMPEG_PID 2>/dev/null || true

echo ""
echo "=========================================="
echo "录制完成!"
echo "文件: $VIDEO_FILE"
ls -lh "$VIDEO_FILE" 2>/dev/null || echo "录制可能失败"
echo "=========================================="
