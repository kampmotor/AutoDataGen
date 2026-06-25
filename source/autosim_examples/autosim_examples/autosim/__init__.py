from autosim import register_pipeline

# Franka Cube Lift - 基础抓取任务
register_pipeline(
    id="AutoSimPipeline-FrankaCubeLift-v0",
    entry_point=f"{__name__}.pipelines.franka_lift_cube:FrankaCubeLiftPipeline",
    cfg_entry_point=f"{__name__}.pipelines.franka_lift_cube:FrankaCubeLiftPipelineCfg",
)

# Stack Cubes - 多物体堆叠任务（更复杂）
register_pipeline(
    id="AutoSimPipeline-StackCubes-v0",
    entry_point=f"{__name__}.pipelines.stack_cubes:StackCubesPipeline",
    cfg_entry_point=f"{__name__}.pipelines.stack_cubes:StackCubesPipelineCfg",
)
