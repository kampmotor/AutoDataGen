# core/ — AutoSim 核心抽象

## 概述

AutoSim 管线的基础类和类型系统：`AutoSimPipeline`、`Skill`、`Decomposer`、`ActionAdapterBase` 以及所有共享 dataclass。

## 快速定位

| 类 | 文件 | 作用 |
|-------|------|------|
| `AutoSimPipeline` | `pipeline.py` | 编排器 —— `run()` → 分解 → 逐技能执行 |
| `AutoSimPipelineCfg` | `pipeline.py` | 配置：decomposer、motion_planner、occupancy_map、action_adapter、max_steps |
| `Skill` (ABC) | `skill.py` | `plan()` → `step()` 生命周期；`extract_goal_from_info()` |
| `Decomposer` (ABC) | `decomposer.py` | 任务分解，带 JSON 缓存（`~/.cache/autosim/decomposer_cache/`） |
| `ActionAdapterBase` | `action_adapter.py` | 技能输出 → 环境动作张量，通过 `register_apply_method()` 注册 |
| `register_pipeline()` / `make_pipeline()` | `registration.py` | 插件式管线注册中心 |
| `SkillRegistry` | `registration.py` | 技能注册单例；`create(name, extra_cfg)` |
| 所有数据类 | `types.py` | `PipelineOutput`、`SkillGoal/Output`、`WorldState`、`EnvExtraInfo`、`DecomposeResult`、`OccupancyMap` |

## 约定

- **`@configclass`** 用于所有配置类（IsaacLab 模式）
- **`class_type: type = MISSING`** 在配置中用于插件分发
- **`register_skill` 装饰器** 优先于手动 `SkillRegistry.register()`
- 抽象方法抛出 `NotImplementedError`
- 日志通过 `AutoSimLogger(name)` —— 格式：`[name] LEVEL: message`

## 反模式

- **禁止**将技能实现导入 `core/` —— core 仅包含抽象层
- **禁止**使用 `typing.Optional` 或 `typing.Union` —— 使用 `x | None` 语法
- **Decomposer 缓存** 通过 `dataclasses.asdict` 序列化为 JSON；确保所有字段类型可 JSON 序列化
