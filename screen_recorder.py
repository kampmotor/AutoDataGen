#!/usr/bin/env python3
"""屏幕录制器 - 使用 mss + imageio 录制屏幕."""

import sys
import time
import argparse
from pathlib import Path

try:
    import mss
    import mss.tools
except ImportError:
    print("错误: 请安装 mss: pip install mss")
    sys.exit(1)

try:
    import imageio
except ImportError:
    print("错误: 请安装 imageio: pip install imageio imageio-ffmpeg")
    sys.exit(1)


def record_screen(output_path: str, duration: int = 60, fps: int = 30, monitor: int = 0):
    """录制屏幕."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    print(f"开始录制: {output}")
    print(f"时长: {duration}秒, 帧率: {fps}fps")

    writer = imageio.get_writer(str(output), fps=fps, codec="libx264", quality=8)

    try:
        with mss.mss() as sct:
            monitor_info = sct.monitors[monitor]
            print(f"录制区域: {monitor_info['width']}x{monitor_info['height']}")

            frame_interval = 1.0 / fps
            start_time = time.time()
            frame_count = 0

            while time.time() - start_time < duration:
                frame_start = time.time()

                # 截图
                img = sct.grab(monitor_info)
                # mss 返回 BGRA raw bytes, 转换为 RGB numpy array
                import numpy as np
                raw = np.frombuffer(img.raw, dtype=np.uint8).reshape(img.height, img.width, 4)
                rgb = raw[:, :, :3][:, :, ::-1]  # BGRA -> RGB
                writer.append_data(rgb)
                frame_count += 1

                # 控制帧率
                elapsed = time.time() - frame_start
                sleep_time = frame_interval - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)

                # 每10秒打印一次状态
                if frame_count % (fps * 10) == 0:
                    elapsed_total = time.time() - start_time
                    print(f"  已录制 {elapsed_total:.0f}/{duration}秒, {frame_count} 帧")

    except KeyboardInterrupt:
        print("\n录制被中断")
    finally:
        writer.close()

    file_size = output.stat().st_size / (1024 * 1024)
    print(f"录制完成: {output}")
    print(f"  总帧数: {frame_count}")
    print(f"  文件大小: {file_size:.1f} MB")
    return str(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="屏幕录制器")
    parser.add_argument("--output", "-o", required=True, help="输出视频路径")
    parser.add_argument("--duration", "-d", type=int, default=60, help="录制时长(秒)")
    parser.add_argument("--fps", type=int, default=30, help="帧率")
    parser.add_argument("--monitor", type=int, default=0, help="显示器编号 (0=全部)")
    args = parser.parse_args()

    record_screen(args.output, args.duration, args.fps, args.monitor)
