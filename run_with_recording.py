#!/usr/bin/env python3
"""AutoDataGen 录像运行脚本.

使用 Isaac Sim 的内置截图功能录制视频帧。
"""

import os
import sys
import time
import argparse
from pathlib import Path

# 添加项目路径
sys.path.insert(0, "/home/zj/PycharmProjects/AutoDataGen/source/autosim")
sys.path.insert(0, "/home/zj/PycharmProjects/AutoDataGen/source/autosim_examples")

from isaaclab.app import AppLauncher


def main():
    parser = argparse.ArgumentParser(description="AutoDataGen with video recording")
    parser.add_argument(
        "--pipeline_id",
        type=str,
        default="AutoSimPipeline-FrankaCubeLift-v0",
        help="Pipeline ID to run",
    )
    parser.add_argument("--num_runs", type=int, default=2, help="Number of runs")
    parser.add_argument(
        "--output_dir",
        type=str,
        default="/home/zj/PycharmProjects/AutoDataGen/videos",
        help="Output directory for frames",
    )
    parser.add_argument("--fps", type=int, default=30, help="Frames per second")

    AppLauncher.add_app_launcher_args(parser)
    args = parser.parse_args()

    # 创建输出目录
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    frames_dir = output_dir / "frames"
    frames_dir.mkdir(exist_ok=True)

    # 启动应用
    app_launcher = AppLauncher(vars(args))
    simulation_app = app_launcher.app

    # 导入 autosim
    import autosim_examples
    from autosim import make_pipeline

    # 截图回调
    frame_count = [0]
    capture_interval = 1.0 / args.fps  # 每帧间隔

    def capture_frame():
        """捕获当前帧."""
        try:
            from omni.isaac.core.utils.viewports import set_camera_view

            # 获取当前时间戳
            timestamp = time.time()

            # 截图文件名
            frame_file = frames_dir / f"frame_{frame_count[0]:06d}.png"

            # 使用 Isaac Sim 的截图功能
            import omni.kit.app

            app = omni.kit.app.get_app()
            if app:
                # 获取渲染窗口
                viewport = app.get_viewport()
                if viewport:
                    viewport.schedule_capture(str(frame_file))
                    frame_count[0] += 1
                    return True
        except Exception as e:
            print(f"截图失败: {e}")
        return False

    # 主函数
    def run_with_recording():
        pipeline = make_pipeline(args.pipeline_id)

        for run_idx in range(args.num_runs):
            print(f"\n{'='*50}")
            print(f"Run {run_idx + 1}/{args.num_runs}")
            print(f"{'='*50}")

            # 开始录制
            print("开始录制...")
            start_time = time.time()

            # 运行 pipeline
            pipeline.run()

            # 停止录制
            end_time = time.time()
            print(f"录制完成，耗时: {end_time - start_time:.2f} 秒")

        # 生成视频
        print(f"\n{'='*50}")
        print("生成视频文件...")
        print(f"{'='*50}")

        # 使用 ffmpeg 从帧生成视频
        video_file = output_dir / "output.mp4"
        cmd = (
            f"ffmpeg -y -framerate {args.fps} "
            f"-i {frames_dir}/frame_%06d.png "
            f"-c:v libx264 -pix_fmt yuv420p "
            f"{video_file}"
        )

        print(f"执行命令: {cmd}")
        os.system(cmd)

        print(f"\n视频已保存到: {video_file}")
        print(f"总帧数: {frame_count[0]}")

    # 运行
    run_with_recording()

    # 关闭应用
    simulation_app.close()


if __name__ == "__main__":
    main()
