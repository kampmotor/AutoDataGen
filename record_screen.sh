#!/bin/bash
# AutoDataGen 屏幕录制脚本
# 使用 ffmpeg 录制 Isaac Sim GUI 窗口

set -e

# 配置
VIDEO_DIR="/home/zj/PycharmProjects/AutoDataGen/videos"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
VIDEO_FILE="${VIDEO_DIR}/demo_${TIMESTAMP}.mp4"
DURATION="${1:-120}"  # 录制时长（秒），默认 120 秒

# 创建视频目录
mkdir -p "$VIDEO_DIR"

echo "=========================================="
echo "AutoDataGen - 屏幕录制"
echo "=========================================="
echo "视频文件: $VIDEO_FILE"
echo "录制时长: ${DURATION} 秒"
echo "=========================================="

# 检查 ffmpeg 是否安装
if ! command -v ffmpeg &> /dev/null; then
    echo "错误: ffmpeg 未安装"
    echo "请运行: sudo apt install ffmpeg"
    exit 1
fi

# 获取 Isaac Sim 窗口 ID
WINDOW_ID=$(xdotool search --name "Isaac Sim" | head -1)
if [ -z "$WINDOW_ID" ]; then
    echo "警告: 未找到 Isaac Sim 窗口，将录制整个屏幕"
    RECORD_TARGET=":0.0"
else
    echo "找到 Isaac Sim 窗口: $WINDOW_ID"
    RECORD_TARGET="window=$WINDOW_ID"
fi

# 启动 ffmpeg 录制（后台运行）
echo "开始录制..."
ffmpeg -f x11grab -r 30 -video_size 1920x1080 -i "$RECORD_TARGET" \
  -vcodec libx264 -preset fast -crf 23 \
  -t "$DURATION" \
  "$VIDEO_FILE" &
FFMPEG_PID=$!

echo "ffmpeg 进程 ID: $FFMPEG_PID"
echo "录制中... 按 Ctrl+C 停止"

# 等待 ffmpeg 完成或用户中断
trap "kill $FFMPEG_PID 2>/dev/null; echo '录制已停止'" INT TERM

# 等待指定时长
sleep "$DURATION"

# 停止录制
kill $FFMPEG_PID 2>/dev/null || true
wait $FFMPEG_PID 2>/dev/null || true

echo ""
echo "=========================================="
echo "录制完成！"
echo "视频文件: $VIDEO_FILE"
echo "文件大小: $(du -h "$VIDEO_FILE" | cut -f1)"
echo "=========================================="
