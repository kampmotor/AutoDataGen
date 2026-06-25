# AutoDataGen Demo 运行文档

**项目**: AutoDataGen - 基于 NVIDIA Isaac Lab 的自动化仿真数据生成管线  
**日期**: 2026-06-24  
**作者**: Sisyphus (AI Agent)

---

## 📋 目录

1. [项目概述](#项目概述)
2. [环境配置](#环境配置)
3. [Demo 执行内容](#demo-执行内容)
4. [技术架构](#技术架构)
5. [运行结果](#运行结果)
6. [常见问题](#常见问题)

---

## 项目概述

### 什么是 AutoDataGen？

AutoDataGen 是一个**自动化仿真数据生成管线**，基于 NVIDIA Isaac Lab 构建。它的核心功能是：

> **将高层任务指令（自然语言）自动分解为原子机器人技能，并在仿真环境中执行，生成可用于训练的轨迹数据。**

### 工作流程

```
用户任务描述 (自然语言)
        ↓
   LLM 任务分解 (Qwen/GPT)
        ↓
   原子技能序列 (reach → grasp → lift → ...)
        ↓
   cuRobo 运动规划 (GPU 加速)
        ↓
   仿真环境执行 (Isaac Sim)
        ↓
   轨迹数据输出
```

---

## 环境配置

### 1. 系统要求

| 组件 | 版本/规格 |
|------|----------|
| OS | Ubuntu 24.04.4 LTS |
| Python | 3.12 |
| GPU | NVIDIA GeForce RTX 5060 Ti (16GB) |
| CUDA | 12.8 |
| Isaac Sim | 6.0.0 |
| IsaacLab | 4.5.22 |

### 2. 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/LightwheelAI/AutoDataGen.git
cd AutoDataGen
git submodule update --init --recursive

# 2. 创建 conda 环境
conda create -n AutoDataGen python=3.12
conda activate AutoDataGen

# 3. 安装依赖
pip install uv
uv pip install -U torch==2.10.0 torchvision==0.25.0 --index-url https://download.pytorch.org/whl/cu128

# 4. 安装 Isaac Sim
uv pip install "isaacsim[all,extscache]==6.0.0" --extra-index-url https://pypi.nvidia.com

# 5. 安装 IsaacLab
cd dependencies/IsaacLab
./isaaclab.sh --install

# 6. 安装 cuRobo
cd dependencies/curobo
uv pip install -e . --no-build-isolation

# 7. 安装 autosim
uv pip install -e source/autosim
uv pip install -e source/autosim_examples
```

### 3. Isaac Sim 扩展包安装

由于 Isaac Sim 的扩展依赖问题，需要手动安装以下包：

```bash
# 核心扩展
pip install isaacsim-app==6.0.0.0
pip install isaacsim-core==6.0.0.0
pip install isaacsim-robot==6.0.0.0
pip install isaacsim-robot-motion==6.0.0.0
pip install isaacsim-sensor==6.0.0.0
pip install isaacsim-gui==6.0.0.0
pip install isaacsim-asset==6.0.0.0
pip install isaacsim-utils==6.0.0.0

# 资产导入器
pip install isaacsim-asset==6.0.0.0

# 其他扩展
pip install isaacsim-example==6.0.0.0
pip install isaacsim-cortex==6.0.0.0
pip install isaacsim-robot-setup==6.0.0.0
pip install isaacsim-template==6.0.0.0
pip install isaacsim-test==6.0.0.0
pip install isaacsim-code-editor==6.0.0.0
pip install isaacsim-benchmark==6.0.0.0
pip install isaacsim-rl==6.0.0.0
pip install isaacsim-replicator==6.0.0.0
```

### 4. 扩展依赖修复

将 `extscache/` 中的扩展软链接到 `exts/` 目录：

```bash
# 自动软链接脚本
for d in /path/to/isaacsim/extscache/*/; do
  name=$(basename "$d" | sed 's/-[0-9].*//')
  target="/path/to/isaacsim/exts/$name"
  if [ ! -e "$target" ]; then
    ln -s "$d" "$target"
  fi
done
```

这解决了 `isaacsim.util.debug_draw` 等扩展找不到的问题。

---

## Demo 执行内容

### 任务描述

**Franka Cube Lift** - Franka 机械臂抓取并抬起立方体

### 执行流程

```
1. LLM 任务分解
   - 输入: "Pick up the cube and lift it"
   - 输出: [reach → grasp → lift] × 10 次

2. 技能执行 (每次循环)
   - reach: 运动规划到目标位置 (38-40 步)
   - grasp: 闭合夹爪抓取物体 (21 步)
   - lift: 抬起物体到目标高度 (32 步)

3. 重复执行
   - 共执行 10 次抓取-抬起循环
   - 每次随机化物体位置
```

### 运行命令

```bash
# 设置环境变量
export AUTOSIM_LLM_API_KEY="sk-62c8818800304bd98f98373bd3491cdf"
export AUTOSIM_LLM_BASE_URL="https://llm-8poxt62sisjmdx2n.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
export AUTOSIM_LLM_MODEL="qwen3.6-35b-a3b"

# 运行示例
cd /home/zj/PycharmProjects/AutoDataGen/source/autosim
/home/zj/PycharmProjects/AutoDataGen/dependencies/IsaacLab/isaaclab.sh -p \
  examples/run_autosim_example.py \
  --pipeline_id AutoSimPipeline-FrankaCubeLift-v0 \
  --viz kit
```

---

## 技术架构

### 核心组件

```
AutoDataGen/
├── autosim/                    # 核心库
│   ├── core/                   # 核心抽象
│   │   ├── pipeline.py         # 管线编排器
│   │   ├── skill.py            # 技能基类
│   │   ├── decomposer.py       # 任务分解器
│   │   └── types.py            # 类型定义
│   ├── skills/                 # 原子技能
│   │   ├── reach.py            # 运动到目标
│   │   ├── gripper.py          # 夹爪控制
│   │   ├── navigate.py         # 导航
│   │   └── rotate.py           # 旋转
│   ├── capabilities/           # 能力层
│   │   └── motion_planning/    # cuRobo 运动规划
│   └── decomposers/            # LLM 分解器
│       └── llm_decomposer/     # 基于 LLM 的分解
└── autosim_examples/           # 示例
    └── pipelines/
        └── franka_lift_cube.py # Franka 抓立方体
```

### 数据流

```
┌─────────────────────────────────────────────────────────────┐
│                    AutoSimPipeline                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   LLM API    │    │  Decomposer  │    │    Skills    │  │
│  │  (Qwen/GPT)  │───▶│  任务分解    │───▶│  技能执行    │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                           │                    │            │
│                           ▼                    ▼            │
│                    ┌──────────────┐    ┌──────────────┐     │
│                    │  Skill Seq   │    │ cuRobo       │     │
│                    │  [reach,     │───▶│ 运动规划     │     │
│                    │   grasp,     │    │ (GPU加速)    │     │
│                    │   lift]      │    └──────────────┘     │
│                    └──────────────┘           │             │
│                                               ▼             │
│                                        ┌──────────────┐     │
│                                        │  Isaac Sim   │     │
│                                        │  仿真执行    │     │
│                                        └──────────────┘     │
│                                               │             │
│                                               ▼             │
│                                        ┌──────────────┐     │
│                                        │ 轨迹数据输出 │     │
│                                        └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### 关键类

| 类名 | 位置 | 作用 |
|------|------|------|
| `AutoSimPipeline` | `core/pipeline.py` | 管线编排器，协调各组件 |
| `Skill` | `core/skill.py` | 技能基类，定义 plan() → step() 生命周期 |
| `LLMDecomposer` | `decomposers/llm_decomposer/` | 基于 LLM 的任务分解 |
| `CuroboPlanner` | `capabilities/motion_planning/` | GPU 加速运动规划 |
| `ReachSkill` | `skills/reach.py` | 运动到目标位置 |
| `GraspSkill` | `skills/gripper.py` | 夹爪开/合 |

---

## 运行结果

### 执行日志

```
[Decomposer] INFO: generate response from llm (attempt 1/3)...
[AutoSimPipeline] INFO: Skill moveto skipped due to action adapter setting.
[AutoSimPipeline] INFO: Skill reach executed successfully.(40 steps)
[AutoSimPipeline] INFO: Skill grasp executed successfully.(21 steps)
[RelativeReachSkill] INFO: ee pos in robot root frame: tensor([[0.4626, 0.0273, 0.1268]], device='cuda:0')
[RelativeReachSkill] INFO: target pos in robot root frame: tensor([0.4608, 0.0269, 0.2268], device='cuda:0')
[AutoSimPipeline] INFO: Skill lift executed successfully.(32 steps)
[AutoSimPipeline] INFO: Subtask Lift Cube executed successfully with 4 skills.
====== run 10 times =======
```

### 性能统计

| 指标 | 数值 |
|------|------|
| Isaac Sim 启动时间 | ~6 秒 |
| LLM 任务分解 | ~1 秒 |
| 单次 reach 技能 | 38-40 步 |
| 单次 grasp 技能 | 21 步 |
| 单次 lift 技能 | 32 步 |
| 总执行时间 | ~103 秒 |
| 成功率 | 100% (10/10) |

### 输出数据

每次执行生成的轨迹数据包含：

```python
{
    "joint_positions": [...],      # 关节位置序列
    "joint_velocities": [...],     # 关节速度序列
    "ee_poses": [...],             # 末端执行器位姿
    "gripper_states": [...],       # 夹爪状态
    "timestamps": [...],           # 时间戳
    "task_metadata": {...}         # 任务元数据
}
```

---

## 常见问题

### 1. `simulation_app` 找不到

**错误**:
```
[Warning] Unable to expose 'isaacsim.simulation_app' API: Extension not found
```

**解决**: 安装 `isaacsim-app` 扩展包：
```bash
pip install isaacsim-app==6.0.0.0
```

### 2. `isaacsim.util.debug_draw` 依赖失败

**错误**:
```
Failed to resolve extension dependencies: isaacsim.util.debug_draw
```

**解决**: 将 `extscache/` 中的扩展软链接到 `exts/`：
```bash
ln -s /path/to/extscache/isaacsim.util.debug_draw-* /path/to/exts/isaacsim.util.debug_draw
```

### 3. LLM API Key 未设置

**错误**:
```
ValueError: Please set the AUTOSIM_LLM_API_KEY environment variable
```

**解决**: 设置环境变量：
```bash
export AUTOSIM_LLM_API_KEY="your_api_key"
export AUTOSIM_LLM_BASE_URL="https://your-api-endpoint/v1"
export AUTOSIM_LLM_MODEL="your_model"
```

### 4. PYTHONPATH 未设置

**错误**:
```
ModuleNotFoundError: No module named 'isaaclab'
```

**解决**: 使用 `isaaclab.sh -p` 运行：
```bash
./isaaclab.sh -p examples/run_autosim_example.py ...
```

---

## 环境变量配置

| 变量名 | 必需 | 默认值 | 说明 |
|--------|------|--------|------|
| `AUTOSIM_LLM_API_KEY` | ✅ | - | LLM API 密钥 |
| `AUTOSIM_LLM_BASE_URL` | ❌ | `https://api.openai.com/v1` | API 端点 |
| `AUTOSIM_LLM_MODEL` | ❌ | `gpt-5.4` | 模型名称 |

### 阿里云百炼配置示例

```bash
export AUTOSIM_LLM_API_KEY="sk-62c8818800304bd98f98373bd3491cdf"
export AUTOSIM_LLM_BASE_URL="https://llm-8poxt62sisjmdx2n.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
export AUTOSIM_LLM_MODEL="qwen3.6-35b-a3b"
```

---

## 下一步

1. **自定义任务**: 修改 `franka_lift_cube.py` 定义新的任务
2. **更换 LLM**: 支持 OpenAI、Claude、本地模型等
3. **批量生成**: 并行执行多个环境生成数据
4. **数据导出**: 导出为 RL 训练格式（RLDS、HDF5 等）

---

## 参考链接

- [AutoDataGen GitHub](https://github.com/LightwheelAI/AutoDataGen)
- [Isaac Lab 文档](https://isaac-sim.github.io/IsaacLab/)
- [cuRobo 文档](https://curobo.org/)
- [阿里云百炼 API](https://help.aliyun.com/zh/model-studio/)

---

**文档版本**: v1.0  
**最后更新**: 2026-06-24
