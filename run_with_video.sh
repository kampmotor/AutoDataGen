#!/bin/bash
# AutoDataGen 运行脚本 - 带录像功能
# 用法: ./run_with_video.sh [pipeline_id] [num_runs]

set -e

# 默认参数
PIPELINE_ID="${1:-AutoSimPipeline-StackCubes-v0}"
NUM_RUNS="${2:-1}"
VIDEO_DIR="/home/zj/PycharmProjects/AutoDataGen/videos"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
VIDEO_FILE="${VIDEO_DIR}/${PIPELINE_ID}_${TIMESTAMP}.mp4"

# 创建视频目录
mkdir -p "$VIDEO_DIR"

echo "=========================================="
echo "AutoDataGen - 带录像运行"
echo "=========================================="
echo "Pipeline: $PIPELINE_ID"
echo "运行次数: $NUM_RUNS"
echo "视频文件: $VIDEO_FILE"
echo "=========================================="

# 设置环境变量
export AUTOSIM_LLM_API_KEY="sk-62c8818800304bd98f98373bd3491cdf"
export AUTOSIM_LLM_BASE_URL="https://llm-8poxt62sisjmdx2n.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
export AUTOSIM_LLM_MODEL="qwen3.6-35b-a3b"

# 切换到工作目录
cd /home/zj/PycharmProjects/AutoDataGen/source/autosim

# 运行带录像的 pipeline
/home/zj/PycharmProjects/AutoDataGen/dependencies/IsaacLab/isaaclab.sh -p \
  examples/run_autosim_example.py \
  --pipeline_id "$PIPELINE_ID" \
  --num_runs "$NUM_RUNS" \
  --video "$VIDEO_FILE" \
  --headless \
  2>&1 | tee "${VIDEO_DIR}/run_${TIMESTAMP}.log"

echo ""
echo "=========================================="
echo "运行完成！"
echo "视频文件: $VIDEO_FILE"
echo "日志文件: ${VIDEO_DIR}/run_${TIMESTAMP}.log"
echo "=========================================="
