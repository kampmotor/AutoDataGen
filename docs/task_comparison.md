# AutoDataGen 任务对比快速参考

## 📋 任务难度等级

| 等级 | 任务类型 | 示例 |
|------|----------|------|
| ⭐ | 简单移动 | 机械臂移动到目标位置 |
| ⭐⭐ | 基础抓取 | FrankaCubeLift |
| ⭐⭐⭐ | 多步操作 | Pick-and-Place |
| ⭐⭐⭐⭐ | 复杂任务 | StackCubes |
| ⭐⭐⭐⭐⭐ | 高级任务 | 装配、烹饪 |

---

## 🎯 FrankaCubeLift vs StackCubes

### FrankaCubeLift (基础任务)

```
任务: 拾取单个立方体并抬起
难度: ⭐⭐
步骤: 4 步 (reach → grasp → lift)
物体: 1 个立方体
时间: ~30 秒
成功率: ~95%
```

**适用场景**:
- 学习基础抓取
- 验证环境配置
- 测试 LLM 分解

### StackCubes (复杂任务)

```
任务: 将3个立方体堆叠成塔
难度: ⭐⭐⭐⭐
步骤: 18+ 步 (多轮 reach → grasp → lift → place)
物体: 3 个立方体
时间: ~150 秒
成功率: ~80%
```

**适用场景**:
- 测试多物体处理
- 验证复杂 LLM 推理
- 演示精确放置

---

## 🔧 运行命令速查

### FrankaCubeLift

```bash
export AUTOSIM_LLM_API_KEY="sk-62c8818800304bd98f98373bd3491cdf"
export AUTOSIM_LLM_BASE_URL="https://llm-8poxt62sisjmdx2n.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
export AUTOSIM_LLM_MODEL="qwen3.6-35b-a3b"

cd /home/zj/PycharmProjects/AutoDataGen/source/autosim
/home/zj/PycharmProjects/AutoDataGen/dependencies/IsaacLab/isaaclab.sh -p \
  examples/run_autosim_example.py \
  --pipeline_id AutoSimPipeline-FrankaCubeLift-v0 \
  --viz kit
```

### StackCubes

```bash
export AUTOSIM_LLM_API_KEY="sk-62c8818800304bd98f98373bd3491cdf"
export AUTOSIM_LLM_BASE_URL="https://llm-8poxt62sisjmdx2n.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
export AUTOSIM_LLM_MODEL="qwen3.6-35b-a3b"

cd /home/zj/PycharmProjects/AutoDataGen/source/autosim
/home/zj/PycharmProjects/AutoDataGen/dependencies/IsaacLab/isaaclab.sh -p \
  examples/run_autosim_example.py \
  --pipeline_id AutoSimPipeline-StackCubes-v0 \
  --viz kit
```

---

## 📊 关键指标对比

| 指标 | FrankaCubeLift | StackCubes | 增幅 |
|------|----------------|------------|------|
| LLM tokens | ~2000 | ~6000 | 3x |
| 总步数 | ~120 | ~582 | 4.8x |
| 执行时间 | ~30s | ~150s | 5x |
| 物体数量 | 1 | 3 | 3x |
| 成功率 | ~95% | ~80% | -15% |

---

## 🧠 LLM 推理复杂度

### FrankaCubeLift

```json
{
  "task": "Pick up the cube and lift it",
  "objects": ["cube"],
  "skills": ["reach", "grasp", "lift"],
  "reasoning": "简单线性序列"
}
```

### StackCubes

```json
{
  "task": "Stack 3 cubes into a tower",
  "objects": ["cube_1", "cube_2", "cube_3"],
  "skills": ["reach", "grasp", "lift", "reach", "ungrasp", "retract"] × 3,
  "reasoning": "多步推理 + 空间计算 + 顺序约束"
}
```

---

## ⚠️ 常见问题

### FrankaCubeLift

1. **LLM API Key 未设置** → 设置 `AUTOSIM_LLM_API_KEY`
2. **simulation_app 找不到** → 安装 `isaacsim-app`
3. **PYTHONPATH 错误** → 使用 `isaaclab.sh -p`

### StackCubes

1. **放置位置不精确** → 调整 `placement_tolerance`
2. **堆叠顺序错误** → 在 prompt 中明确顺序
3. **高度计算错误** → 预计算目标位置
4. **堆叠塔倒塌** → 增加稳定性检查

---

## 🎓 学习路径

```
第1周: FrankaCubeLift
  - 理解基础抓取流程
  - 熟悉 LLM 分解机制
  - 验证环境配置

第2周: StackCubes
  - 学习多物体处理
  - 理解空间推理
  - 优化 LLM prompt

第3周+: 自定义任务
  - 设计新的复杂任务
  - 优化技能组合
  - 提高成功率
```

---

**快速参考版本**: v1.0  
**最后更新**: 2026-06-24
