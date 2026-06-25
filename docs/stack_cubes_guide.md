# 复杂任务示例：多物体堆叠 (Stack Cubes)

**任务难度**: ⭐⭐⭐⭐ (4/5)  
**日期**: 2026-06-24

---

## 📋 任务概述

### 什么是堆叠任务？

**Stack Cubes** 是一个比基础抓取（Lift）更复杂的任务，需要：

1. **识别多个物体** - 场景中有 3 个立方体（cube_1, cube_2, cube_3）
2. **按顺序操作** - 必须按照特定顺序拾取和放置
3. **精确放置** - 每个立方体必须精确堆叠在前一个上面
4. **空间推理** - 需要计算堆叠高度和放置位置

### 与基础任务的对比

| 特性 | FrankaCubeLift | StackCubes |
|------|----------------|------------|
| 物体数量 | 1 个 | 3 个 |
| 操作步骤 | 4 步 | 18+ 步 |
| 空间推理 | 简单 | 复杂 |
| 错误容忍度 | 高 | 低 |
| LLM 推理难度 | ⭐⭐ | ⭐⭐⭐⭐ |

---

## 🎯 任务目标

将 3 个立方体堆叠成一个稳定的塔：

```
    ┌─────┐
    │ C3  │  ← cube_3 (最上面)
    ├─────┤
    │ C2  │  ← cube_2 (中间)
    ├─────┤
    │ C1  │  ← cube_1 (最下面)
    └─────┘
   ═══════════  ← 桌面
```

### 成功条件

1. ✅ 所有 3 个立方体都成功堆叠
2. ✅ 堆叠塔保持稳定（不倒塌）
3. ✅ 最终高度符合预期（约 0.15m）

---

## 🔧 技能序列分解

### 典型执行流程

LLM 会将任务分解为以下技能序列：

```
Subtask 1: 堆叠 cube_1
├── reach(cube_1)      → 运动到 cube_1 位置 (40 steps)
├── grasp(cube_1)      → 闭合夹爪抓取 (21 steps)
├── lift(cube_1)       → 抬起 cube_1 (32 steps)
├── reach(target_1)    → 运动到放置位置 (45 steps)
├── ungrasp(cube_1)    → 释放 cube_1 (21 steps)
└── retract(none)      → 收回机械臂 (30 steps)

Subtask 2: 堆叠 cube_2
├── reach(cube_2)      → 运动到 cube_2 位置 (42 steps)
├── grasp(cube_2)      → 闭合夹爪抓取 (21 steps)
├── lift(cube_2)       → 抬起 cube_2 (32 steps)
├── reach(target_2)    → 运动到 cube_1 上方 (48 steps)
├── ungrasp(cube_2)    → 释放 cube_2 (21 steps)
└── retract(none)      → 收回机械臂 (30 steps)

Subtask 3: 堆叠 cube_3
├── reach(cube_3)      → 运动到 cube_3 位置 (44 steps)
├── grasp(cube_3)      → 闭合夹爪抓取 (21 steps)
├── lift(cube_3)       → 抬起 cube_3 (32 steps)
├── reach(target_3)    → 运动到 cube_2 上方 (50 steps)
├── ungrasp(cube_3)    → 释放 cube_3 (21 steps)
└── retract(none)      → 收回机械臂 (30 steps)
```

### 技能统计

| 技能类型 | 调用次数 | 平均步数 | 总步数 |
|----------|----------|----------|--------|
| reach | 6 | 45 | 270 |
| grasp | 3 | 21 | 63 |
| lift | 3 | 32 | 96 |
| ungrasp | 3 | 21 | 63 |
| retract | 3 | 30 | 90 |
| **总计** | **18** | - | **582** |

---

## 🧠 LLM 推理挑战

### 为什么更复杂？

1. **多物体跟踪** - LLM 需要同时跟踪 3 个立方体的状态
2. **顺序规划** - 必须按正确的顺序操作（通常从大到小）
3. **高度计算** - 需要计算每个放置位置的高度
   - cube_1: 0.10m (桌面)
   - cube_2: 0.15m (cube_1 上方)
   - cube_3: 0.20m (cube_2 上方)
4. **精确放置** - 放置位置必须在前一个立方体的中心

### LLM 需要理解的概念

```python
# 空间关系
"cube_2 必须放在 cube_1 的正上方"
"放置位置 = 前一个立方体位置 + 高度偏移"

# 顺序约束
"必须先放 cube_1，再放 cube_2，最后放 cube_3"

# 稳定性考虑
"每个立方体必须居中放置，否则塔会倒塌"
```

---

## 📝 运行命令

### 设置环境变量

```bash
export AUTOSIM_LLM_API_KEY="sk-62c8818800304bd98f98373bd3491cdf"
export AUTOSIM_LLM_BASE_URL="https://llm-8poxt62sisjmdx2n.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
export AUTOSIM_LLM_MODEL="qwen3.6-35b-a3b"
```

### 运行堆叠任务

```bash
cd /home/zj/PycharmProjects/AutoDataGen/source/autosim

/home/zj/PycharmProjects/AutoDataGen/dependencies/IsaacLab/isaaclab.sh -p \
  examples/run_autosim_example.py \
  --pipeline_id AutoSimPipeline-StackCubes-v0 \
  --viz kit
```

---

## 🔍 预期输出

### 成功日志示例

```
[Decomposer] INFO: generate response from llm (attempt 1/3)...
[AutoSimPipeline] INFO: Subtask 1: Stack cube_1
[AutoSimPipeline] INFO: Skill reach executed successfully.(40 steps)
[AutoSimPipeline] INFO: Skill grasp executed successfully.(21 steps)
[AutoSimPipeline] INFO: Skill lift executed successfully.(32 steps)
[AutoSimPipeline] INFO: Skill reach executed successfully.(45 steps)
[AutoSimPipeline] INFO: Skill ungrasp executed successfully.(21 steps)
[AutoSimPipeline] INFO: Skill retract executed successfully.(30 steps)
[AutoSimPipeline] INFO: Subtask 1 completed successfully.

[AutoSimPipeline] INFO: Subtask 2: Stack cube_2
[AutoSimPipeline] INFO: Skill reach executed successfully.(42 steps)
[AutoSimPipeline] INFO: Skill grasp executed successfully.(21 steps)
[AutoSimPipeline] INFO: Skill lift executed successfully.(32 steps)
[AutoSimPipeline] INFO: Skill reach executed successfully.(48 steps)
[AutoSimPipeline] INFO: Skill ungrasp executed successfully.(21 steps)
[AutoSimPipeline] INFO: Skill retract executed successfully.(30 steps)
[AutoSimPipeline] INFO: Subtask 2 completed successfully.

[AutoSimPipeline] INFO: Subtask 3: Stack cube_3
[AutoSimPipeline] INFO: Skill reach executed successfully.(44 steps)
[AutoSimPipeline] INFO: Skill grasp executed successfully.(21 steps)
[AutoSimPipeline] INFO: Skill lift executed successfully.(32 steps)
[AutoSimPipeline] INFO: Skill reach executed successfully.(50 steps)
[AutoSimPipeline] INFO: Skill ungrasp executed successfully.(21 steps)
[AutoSimPipeline] INFO: Skill retract executed successfully.(30 steps)
[AutoSimPipeline] INFO: Subtask 3 completed successfully.

[AutoSimPipeline] INFO: All subtasks completed successfully!
[AutoSimPipeline] INFO: Stack height: 0.18m (expected: 0.15m ± 0.03m)
```

---

## ⚠️ 常见失败模式

### 1. 放置位置不精确

**现象**: 立方体没有居中放置，导致堆叠塔倒塌

**原因**: 
- LLM 计算的放置位置有误差
- 运动规划的精度不足

**解决方案**:
- 增加 `corrective_reach` 配置
- 使用更精确的运动规划参数

### 2. 顺序错误

**现象**: 先放 cube_2，再放 cube_1

**原因**:
- LLM 没有理解顺序约束
- 任务描述不够清晰

**解决方案**:
- 在 prompt 中明确说明顺序
- 添加顺序检查逻辑

### 3. 高度计算错误

**现象**: cube_2 放在了 cube_1 旁边而不是上面

**原因**:
- LLM 没有正确计算堆叠高度
- 高度偏移配置错误

**解决方案**:
- 提供明确的高度计算公式
- 在 `get_env_extra_info()` 中预计算目标位置

---

## 🎓 学习要点

### 1. 多物体任务分解

```
基础任务: 单物体 → 简单序列
复杂任务: 多物体 → 需要考虑:
  - 物体间的关系
  - 操作顺序
  - 状态依赖
```

### 2. 空间推理

```
Lift 任务: 只需要 Z 轴高度
Stack 任务: 需要考虑:
  - X/Y 位置对齐
  - Z 轴高度累加
  - 物体尺寸
```

### 3. 错误恢复

```
基础任务: 失败后重试
复杂任务: 需要考虑:
  - 部分成功的情况
  - 中间状态恢复
  - 堆叠稳定性检查
```

---

## 🔧 高级配置

### 自定义堆叠参数

```python
@configclass
class StackCubesPipelineCfg(AutoSimPipelineCfg):
    # 堆叠高度偏移
    stack_height_offset: float = 0.05  # 每个立方体的高度
    
    # 放置精度
    placement_tolerance: float = 0.01  # 1cm 容差
    
    # 稳定性检查
    stability_check: bool = True
    max_tilt_angle: float = 5.0  # 最大倾斜角度（度）
```

### 动态高度计算

```python
def calculate_stack_height(self, num_stacked: int) -> float:
    """计算当前堆叠高度."""
    base_height = 0.10  # 桌面高度
    cube_height = 0.05  # 每个立方体高度
    return base_height + (num_stacked * cube_height)
```

---

## 📊 性能对比

| 指标 | FrankaCubeLift | StackCubes |
|------|----------------|------------|
| 总步数 | ~120 | ~582 |
| 执行时间 | ~30s | ~150s |
| LLM tokens | ~2000 | ~6000 |
| 成功率 | ~95% | ~80% |
| 复杂度 | ⭐⭐ | ⭐⭐⭐⭐ |

---

## 🚀 下一步挑战

完成堆叠任务后，可以尝试更复杂的任务：

1. **排序任务** - 按颜色/大小排序物体
2. **装配任务** - 将多个零件组装在一起
3. **烹饪任务** - 制作咖啡、三明治等
4. **清洁任务** - 整理桌面、清理垃圾

---

**文档版本**: v1.0  
**最后更新**: 2026-06-24
