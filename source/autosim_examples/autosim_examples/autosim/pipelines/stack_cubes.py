"""Stack Cubes Pipeline - 多物体堆叠任务示例.

这是一个比 FrankaCubeLift 更复杂的任务，需要：
1. 识别多个立方体（cube_1, cube_2, cube_3）
2. 按顺序拾取每个立方体
3. 将它们精确堆叠在一起
4. 涉及多步推理和空间规划

任务难度：⭐⭐⭐⭐ (4/5)
"""

import torch
from isaaclab.envs import ManagerBasedEnv
from isaaclab.utils import configclass

from autosim.core.pipeline import AutoSimPipeline, AutoSimPipelineCfg
from autosim.core.types import EnvExtraInfo
from autosim.decomposers import LLMDecomposerCfg

from ..action_adapters.franka_adapter_cfg import FrankaAbsAdapterCfg


@configclass
class StackCubesPipelineCfg(AutoSimPipelineCfg):
    """Configuration for the stack cubes pipeline.

    这个配置定义了多物体堆叠任务，需要将3个立方体堆叠成塔。
    """

    decomposer: LLMDecomposerCfg = LLMDecomposerCfg(
        base_url="https://llm-8poxt62sisjmdx2n.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
        model="qwen3.6-35b-a3b",
        max_tokens=8000,  # 更复杂的任务需要更多 tokens
    )

    action_adapter: FrankaAbsAdapterCfg = FrankaAbsAdapterCfg()

    def __post_init__(self):
        # 堆叠任务的特殊配置
        self.skills.lift.extra_cfg.move_axis = "-z"
        self.skills.lift.extra_cfg.lift_offset = 0.30  # 抬起高度

        # 碰撞检测配置 - 堆叠时需要更精确的避障
        self.occupancy_map.floor_prim_suffix = "Table"
        self.occupancy_map.inflation_radius = 0.15  # 更小的膨胀半径，允许更精确的放置

        # 运动规划配置
        self.motion_planner.robot_config_file = "franka.yml"
        self.motion_planner.world_ignore_subffixes = []
        self.motion_planner.world_only_subffixes = []
        self.motion_planner.env_scene_prefix = None

        # 堆叠目标高度配置（相对于桌面）
        self.stack_height_offset = 0.05  # 每个立方体的高度偏移


class StackCubesPipeline(AutoSimPipeline):
    """Stack Cubes Pipeline - 多物体堆叠任务.

    这个 pipeline 演示了如何处理更复杂的多物体交互任务：
    - 需要识别和跟踪多个物体
    - 需要按特定顺序执行操作
    - 需要精确的空间放置
    - 涉及复杂的状态管理
    """

    def __init__(self, cfg: AutoSimPipelineCfg):
        self._task_name = "Isaac-Stack-Cube-Franka-v0"
        super().__init__(cfg)

    def load_env(self) -> ManagerBasedEnv:
        """加载堆叠任务环境."""
        import gymnasium as gym
        from isaaclab_tasks.utils import parse_env_cfg

        # 解析环境配置
        env_cfg = parse_env_cfg(
            self._task_name,
            device="cuda:0",
            num_envs=1,
            use_fabric=True,
        )

        # 堆叠任务的特殊配置
        env_cfg.terminations = None  # 禁用自动终止，允许完整执行

        # 关闭重力，便于精确控制
        env_cfg.scene.robot.spawn.rigid_props.disable_gravity = True

        # 创建环境
        env = gym.make(self._task_name, cfg=env_cfg).unwrapped
        return env

    def get_env_extra_info(self) -> EnvExtraInfo:
        """获取环境额外信息，包括堆叠任务的特殊配置."""
        available_objects = self._env.scene.keys()

        return EnvExtraInfo(
            task_name=self._task_name,
            objects=available_objects,
            additional_prompt_contents="""
## 堆叠任务特殊说明

这是一个多物体堆叠任务，需要将3个立方体堆叠成塔。

### 关键约束：
1. **堆叠顺序**：必须从大到小堆叠（如果立方体大小不同）
2. **放置精度**：每个立方体必须精确放置在前一个立方体的中心
3. **高度计算**：需要考虑已堆叠立方体的总高度
4. **稳定性**：确保堆叠后的塔不会倒塌

### 成功条件：
- 所有3个立方体都成功堆叠
- 堆叠塔保持稳定（不倒塌）
- 最终高度符合预期

### 技能序列示例：
对于3个立方体的堆叠，典型的技能序列是：
1. 拾取 cube_1 → 堆叠到目标位置
2. 拾取 cube_2 → 堆叠到 cube_1 上
3. 拾取 cube_3 → 堆叠到 cube_2 上

每个堆叠步骤包含：
- reach(object) - 运动到物体
- grasp(object) - 抓取物体
- lift(object) - 抬起物体
- reach(target) - 运动到放置位置
- ungrasp(object) - 释放物体
- retract(none) - 收回机械臂
""",
            robot_name="robot",
            robot_base_link_name="panda_link0",
            ee_link_name="panda_hand",
            # 堆叠目标位姿 - 需要根据实际立方体位置计算
            object_reach_target_poses={
                "cube_1": [
                    # 第一个立方体放置位置（桌面中心）
                    torch.tensor([0.5, 0.0, 0.10, 1.0, 0.0, 0.0, 0.0]),
                ],
                "cube_2": [
                    # 第二个立方体放置位置（cube_1 上方）
                    torch.tensor([0.5, 0.0, 0.15, 1.0, 0.0, 0.0, 0.0]),
                ],
                "cube_3": [
                    # 第三个立方体放置位置（cube_2 上方）
                    torch.tensor([0.5, 0.0, 0.20, 1.0, 0.0, 0.0, 0.0]),
                ],
            },
        )
