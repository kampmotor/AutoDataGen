#!/bin/bash
# 同步启动 Isaac Sim + 屏幕录制 (修复版 v2)
set -e

source /home/zj/miniconda3/etc/profile.d/conda.sh
conda activate AutoDataGen

export AUTOSIM_LLM_API_KEY="sk-62c8818800304bd98f98373bd3491cdf"
export AUTOSIM_LLM_BASE_URL="https://llm-8poxt62sisjmdx2n.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
export AUTOSIM_LLM_MODEL="qwen3.6-35b-a3b"
export DISPLAY=:1

VIDEO_DIR="/home/zj/PycharmProjects/AutoDataGen/videos"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
VIDEO_FILE="${VIDEO_DIR}/demo_${TIMESTAMP}.mp4"
PYTHON="/home/zj/miniconda3/envs/AutoDataGen/bin/python"
RECORD_SCRIPT="/home/zj/PycharmProjects/AutoDataGen/screen_recorder.py"

mkdir -p "$VIDEO_DIR"

echo "=========================================="
echo "AutoDataGen 录制 (v2)"
echo "Python: $PYTHON"
echo "Display: $DISPLAY"
echo "CONDA_PREFIX: $CONDA_PREFIX"
echo "视频: $VIDEO_FILE"
echo "=========================================="

cd /home/zj/PycharmProjects/AutoDataGen/source/autosim

# 1. 启动屏幕录制 (后台)
echo "[1/3] 启动屏幕录制..."
$PYTHON "$RECORD_SCRIPT" --output "$VIDEO_FILE" --duration 120 --fps 20 &
REC_PID=$!
echo "  录制 PID: $REC_PID"
sleep 2

# 2. 启动 Isaac Sim (直接用正确的 python，绕过 isaaclab.sh 的检测)
echo "[2/3] 启动 Isaac Sim..."
export ISAACLAB_PATH="/home/zj/PycharmProjects/AutoDataGen/dependencies/IsaacLab"
export PYTHONPATH="$ISAACLAB_PATH/source/isaaclab:$PYTHONPATH"
$PYTHON -c "from isaaclab.cli import cli; cli()" -- examples/run_autosim_example.py \
  --pipeline_id AutoSimPipeline-FrankaCubeLift-v0 \
  --num_runs 2 \
  --viz kit &
SIM_PID=$!
echo "  Isaac Sim PID: $SIM_PID"

# 3. 等待 Isaac Sim 完成
echo "[3/3] 等待 Isaac Sim 完成..."
wait $SIM_PID
echo "  Isaac Sim 已退出"

sleep 3

echo "停止录制..."
kill $REC_PID 2>/dev/null || true
wait $REC_PID 2>/dev/null || true

echo ""
echo "=========================================="
echo "完成!"
ls -lh "$VIDEO_FILE" 2>/dev/null || echo "视频文件未生成"
echo "=========================================="
