# 项目知识库

**生成时间：** 2026-06-24
**提交：** 5f158d2
**分支：** main

## 概述

AutoDataGen —— 基于 NVIDIA Isaac Lab 的自动化仿真数据生成管线。通过 LLM 将高层任务指令分解为原子机器人技能，由 cuRobo 运动规划和 A*/DWA 导航执行。

## 目录结构

```
./
├── source/autosim/autosim/    # 主包（core、skills、capabilities、decomposers）
├── source/autosim_examples/   # 示例管线（Franka 提立方体）
├── examples/                  # 独立运行脚本
├── dependencies/              # IsaacLab + cuRobo 子模块
├── pyproject.toml             # Black（120字符）、isort
├── .pre-commit-config.yaml    # Black、flake8、isort、pyupgrade、codespell
├── .flake8                    # max-complexity=30、Google 风格文档字符串
└── docs/
```

## 快速定位

| 任务 | 位置 | 说明 |
|------|------|------|
| 核心抽象 | [`source/autosim/autosim/core/`](source/autosim/autosim/core/) | Pipeline、Skill、Decomposer、类型定义 |
| 原子技能 | [`source/autosim/autosim/skills/`](source/autosim/autosim/skills/) | Reach、Grasp、Navigate、Rotate 等 |
| 能力层 | [`source/autosim/autosim/capabilities/`](source/autosim/autosim/capabilities/) | cuRobo 规划器、A*/DWA 导航 |
| LLM 分解器 | [`source/autosim/autosim/decomposers/`](source/autosim/autosim/decomposers/) | LLMDecomposer + prompt 模板 |
| 示例管线 | [`source/autosim_examples/`](source/autosim_examples/) | FrankaCubeLiftPipeline |
| 运行入口 | [`examples/run_autosim_example.py`](source/autosim/examples/run_autosim_example.py) | CLI 入口点 |
| 抓取编辑器 | [`examples/grasp_authoring/`](source/autosim/examples/grasp_authoring/) | 独立抓取位姿编辑器 |

## 代码映射

| 符号 | 类型 | 位置 | 作用 |
|------|------|------|------|
| `AutoSimPipeline` | 抽象类 | `core/pipeline.py` | 管线编排器。子类需实现 `load_env()`、`get_env_extra_info()` |
| `AutoSimPipelineCfg` | 配置 | `core/pipeline.py` | 配置：decomposer、motion_planner、occupancy_map、skills、action_adapter |
| `Skill` | 抽象类 | `core/skill.py` | 技能基类：`plan()` → `step()` 生命周期 |
| `SkillCfg` / `SkillExtraCfg` | 配置 | `core/skill.py` | 技能配置 + 各技能专属扩展配置 |
| `Decomposer` | 抽象类 | `core/decomposer.py` | 任务分解，带 JSON 缓存 |
| `ActionAdapterBase` | 类 | `core/action_adapter.py` | 技能输出 → 环境动作映射 |
| `SkillRegistry` | 单例 | `core/registration.py` | 插件式技能注册中心 + 管线注册 |
| `PipelineOutput` | dataclass | `core/types.py` | `success` + `generated_actions` |
| `WorldState` | dataclass | `core/types.py` | 机器人关节状态、末端位姿、物体状态 |
| `DecomposeResult` | dataclass | `core/types.py` | 子任务、技能序列、物体、条件 |
| `EnvExtraInfo` | dataclass | `core/types.py` | 任务名、机器人链接、到达目标位姿 |
| `OccupancyMap` | dataclass | `core/types.py` | 导航规划用栅格地图 |
| `SkillGoal` / `SkillOutput` | dataclass | `core/types.py` | 目标（target_pose [K,7]）、输出（action） |
| `CuroboPlanner` | 类 | `capabilities/motion_planning/curobo/` | GPU 加速运动规划 |
| `LLMDecomposer` | 类 | `decomposers/llm_decomposer/` | 基于 LLM 的任务分解 |
| `ReachSkill` | 类 | `skills/reach.py` | 运动规划到目标位姿 |
| `GraspSkill` | 类 | `skills/gripper.py` | 夹爪开/合 |
| `NavigateSkill` | 类 | `skills/navigate.py` | A* + DWA 导航 |
| `FrankaCubeLiftPipeline` | 类 | `autosim_examples/autosim/pipelines/` | 示例：Franka 提立方体 |

## 约定

- **Python 3.11+**，使用现代类型注解（PEP 604：`x | None`，禁止 `Optional`/`Union`）
- 所有配置类使用 **Isaac Lab `@configclass`**；`class_type: type = MISSING` 用于插件分发
- **注册模式**：`register_pipeline(id, entry_point, cfg_entry_point)` / `register_skill(name, desc, cfg)` 装饰器
- **ABC 基类**，抽象方法抛出 `NotImplementedError`
- **`as_torch()` 工具函数** 用于 warp→torch 张量转换（位于 `utils/data_util.py`）
- **技能配置容器** 通过 `AutoSimSkillsExtraCfg` + `.get(skill_name)` 访问

## 反模式（本项目禁止）

- **不要直接从仿真缓冲区构造 `torch.Tensor`** —— 使用 `as_torch()` 包装器
- **不要裸用 `python3`** —— 在 IsaacLab 依赖环境下使用 `./isaaclab.sh -p`
- **`extra_target_link_names` 不能有重复项** —— 由 `CuroboSkillExtraCfg.__post_init__` 强制校验
- **不要无充分理由添加新依赖** —— IsaacLab 自身规则

## 常用命令

```bash
# 安装 autosim
uv pip install -e source/autosim

# 安装示例
uv pip install -e source/autosim_examples

# 运行 Franka 提立方体示例
python examples/run_autosim_example.py --pipeline_id AutoSimPipeline-FrankaCubeLift-v0 --viz kit

# 运行 pre-commit 检查
pre-commit run --all-files
```

## 备注

- `dependencies/IsaacLab/` 有自己的 `AGENTS.md` —— 不要重复其内容
- cuRobo 为可选依赖（仅 `CuroboSkillBase` 子类技能使用）
- LLM 分解器缓存位于 `~/.cache/autosim/decomposer_cache/`
