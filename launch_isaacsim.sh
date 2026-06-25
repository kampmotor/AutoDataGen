#!/bin/bash
# 启动 Isaac Sim 进行视频录制
source /home/zj/miniconda3/etc/profile.d/conda.sh
conda activate AutoDataGen

export AUTOSIM_LLM_API_KEY="sk-62c8818800304bd98f98373bd3491cdf"
export AUTOSIM_LLM_BASE_URL="https://llm-8poxt62sisjmdx2n.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
export AUTOSIM_LLM_MODEL="qwen3.6-35b-a3b"
export DISPLAY=:0

cd /home/zj/PycharmProjects/AutoDataGen/source/autosim
exec /home/zj/PycharmProjects/AutoDataGen/dependencies/IsaacLab/isaaclab.sh -p examples/run_autosim_example.py --pipeline_id AutoSimPipeline-FrankaCubeLift-v0 --viz kit
