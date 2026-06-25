#!/bin/bash
# 同步启动 Isaac Sim + 屏幕录制
source /home/zj/miniconda3/etc/profile.d/conda.sh
conda activate AutoDataGen

export AUTOSIM_LLM_API_KEY="sk-62c8818800304bd98f98373bd3491cdf"
export AUTOSIM_LLM_BASE_URL="https://llm-8poxt62sisjmdx2n.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
export AUTOSIM_LLM_MODEL="qwen3.6-35b-a3b"
export DISPLAY=:0

VIDEO_DIR="/home/zj/PycharmProjects/AutoDataGen/videos"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
VIDEO_FILE="${VIDEO_DIR}/demo_${TIMESTAMP}.mp4"
RECORD_SCRIPT="/home/zj/PycharmProjects/AutoDataGen/screen_recorder.py"

echo "=========================================="
echo "AutoDataGen 录制"
echo "视频: $VIDEO_FILE"
echo "=========================================="

cd /home/zj/PycharmProjects/AutoDataGen/source/autosim

# 先等 GUI 窗口出现
echo "[1/3] 启动 Isaac Sim..."
/home/zj/PycharmProjects/AutoDataGen/dependencies/IsaacLab/isaaclab.sh -p \
  examples/run_autosim_example.py \
  --pipeline_id AutoSimPipeline-FrankaCubeLift-v0 \
  --num_runs 2 \
  --viz kit &
SIM_PID=$!
echo "  Isaac Sim PID: $SIM_PID"

# 等待窗口加载
echo "  等待 GUI 窗口..."
sleep 30

echo "[2/3] 启动屏幕录制..."
python "$RECORD_SCRIPT" --output "$VIDEO_FILE" --duration 120 --fps 20 &
REC_PID=$!
echo "  录制 PID: $REC_PID"

# 等待 Isaac Sim 完成
echo "[3/3] 等待 Isaac Sim 完成..."
wait $SIM_PID
echo "  Isaac Sim 已退出"

# 停止录制
kill $REC_PID 2>/dev/null
wait $REC_PID 2>/dev/null
echo "  录制已停止"

echo ""
echo "=========================================="
echo "完成!"
ls -lh "$VIDEO_FILE" 2>/dev/null || echo "视频文件未生成"
echo "=========================================="
