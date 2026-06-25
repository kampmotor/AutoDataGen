# AutoDataGen 录像指南

**日期**: 2026-06-25

---

## 📋 概述

本文档说明如何为 AutoDataGen 任务录制运行视频。

---

## 🎬 录像方法

### 方法 1: 使用 ffmpeg 屏幕录制（推荐）

最简单的方法是使用 ffmpeg 录制整个屏幕或 Isaac Sim 窗口。

#### 步骤

1. **安装 ffmpeg**（如果未安装）：
   ```bash
   sudo apt install ffmpeg
   ```

2. **运行录制脚本**：
   ```bash
   cd /home/zj/PycharmProjects/AutoDataGen
   ./record_screen.sh 120  # 录制 120 秒
   ```

3. **同时运行任务**（在另一个终端）：
   ```bash
   cd /home/zj/PycharmProjects/AutoDataGen/source/autosim
   export AUTOSIM_LLM_API_KEY="sk-62c8818800304bd98f98373bd3491cdf"
   export AUTOSIM_LLM_BASE_URL="https://llm-8poxt62sisjmdx2n.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
   export AUTOSIM_LLM_MODEL="qwen3.6-35b-a3b"
   
   /home/zj/PycharmProjects/AutoDataGen/dependencies/IsaacLab/isaaclab.sh -p \
     examples/run_autosim_example.py \
     --pipeline_id AutoSimPipeline-FrankaCubeLift-v0 \
     --viz kit
   ```

#### 脚本说明

`record_screen.sh` 脚本会：
- 自动查找 Isaac Sim 窗口
- 使用 x11grab 录制屏幕
- 生成 MP4 视频文件
- 保存到 `videos/` 目录

---

### 方法 2: 使用 Isaac Sim 内置截图功能

Isaac Sim 支持内置的截图和录像功能。

#### 步骤

1. **运行带截图的脚本**：
   ```bash
   cd /home/zj/PycharmProjects/AutoDataGen
   python run_with_recording.py \
     --pipeline_id AutoSimPipeline-FrankaCubeLift-v0 \
     --num_runs 2 \
     --output_dir ./videos \
     --viz kit
   ```

2. **生成视频**：
   脚本会自动使用 ffmpeg 将截图帧合成为视频。

---

### 方法 3: 使用 Isaac Sim GUI 录像

Isaac Sim GUI 内置了录像功能。

#### 步骤

1. **启动 Isaac Sim GUI**：
   ```bash
   cd /home/zj/PycharmProjects/AutoDataGen/source/autosim
   /home/zj/PycharmProjects/AutoDataGen/dependencies/IsaacLab/isaaclab.sh -p \
     examples/run_autosim_example.py \
     --pipeline_id AutoSimPipeline-FrankaCubeLift-v0 \
     --viz kit
   ```

2. **在 GUI 中录制**：
   - 点击菜单栏 `Window` → `Recording`
   - 点击 `Start Recording`
   - 运行任务
   - 点击 `Stop Recording`
   - 选择保存位置

---

## 📁 输出文件

### 文件结构

```
videos/
├── demo_20260625_103000.mp4          # 屏幕录制视频
├── frames/                           # 截图帧目录
│   ├── frame_000000.png
│   ├── frame_000001.png
│   └── ...
├── output.mp4                        # 合成的视频
└── run_20260625_103000.log           # 运行日志
```

### 视频规格

| 参数 | 默认值 |
|------|--------|
| 分辨率 | 1920x1080 |
| 帧率 | 30 FPS |
| 编码 | H.264 |
| 格式 | MP4 |

---

## 🔧 高级配置

### 自定义录制参数

修改 `record_screen.sh` 中的参数：

```bash
# 录制时长（秒）
DURATION=180

# 视频分辨率
VIDEO_SIZE=2560x1440

# 帧率
FPS=60

# 视频质量（CRF 值，越小质量越高）
CRF=18
```

### 录制特定区域

如果只想录制 Isaac Sim 窗口的一部分：

```bash
# 获取窗口位置和大小
WINDOW_INFO=$(xdotool getwindowgeometry --shell $WINDOW_ID)
X=$(echo $WINDOW_INFO | grep X | cut -d= -f2)
Y=$(echo $WINDOW_INFO | grep Y | cut -d= -f2)
WIDTH=$(echo $WINDOW_INFO | grep WIDTH | cut -d= -f2)
HEIGHT=$(echo $WINDOW_INFO | grep HEIGHT | cut -d= -f2)

# 录制指定区域
ffmpeg -f x11grab -r 30 -video_size ${WIDTH}x${HEIGHT} \
  -i "${RECORD_TARGET}+${X},${Y}" \
  -vcodec libx264 -preset fast -crf 23 \
  output.mp4
```

---

## 🎯 录像最佳实践

### 1. 录制前准备

- 关闭不必要的窗口和通知
- 确保 Isaac Sim 窗口完全加载
- 调整合适的视角

### 2. 录制过程中

- 避免移动鼠标到录制区域
- 不要最小化 Isaac Sim 窗口
- 保持系统稳定（避免高 CPU 使用）

### 3. 录制后处理

- 使用视频编辑软件剪辑
- 添加标题和说明
- 压缩视频大小（如果需要）

---

## 📊 示例输出

### FrankaCubeLift 录像

```bash
# 运行命令
./record_screen.sh 60

# 预期输出
视频文件: videos/demo_20260625_103000.mp4
文件大小: 25MB
时长: 60 秒
```

### StackCubes 录像

```bash
# 运行命令
./record_screen.sh 180

# 预期输出
视频文件: videos/demo_20260625_110000.mp4
文件大小: 75MB
时长: 180 秒
```

---

## ⚠️ 常见问题

### 1. ffmpeg 未安装

**错误**: `ffmpeg: command not found`

**解决**:
```bash
sudo apt update
sudo apt install ffmpeg
```

### 2. 无法找到 Isaac Sim 窗口

**错误**: `警告: 未找到 Isaac Sim 窗口`

**解决**:
- 确保 Isaac Sim 已启动
- 使用 `xdotool search --name "Isaac Sim"` 检查窗口

### 3. 录制卡顿

**原因**: CPU 使用率过高

**解决**:
- 关闭其他应用
- 降低录制帧率
- 使用更小的视频分辨率

### 4. 视频文件过大

**解决**:
- 增加 CRF 值（降低质量）
- 降低帧率
- 缩短录制时长

---

## 📝 快速参考

### 录制 60 秒演示

```bash
cd /home/zj/PycharmProjects/AutoDataGen
./record_screen.sh 60
```

### 录制完整任务（StackCubes）

```bash
./record_screen.sh 180
```

### 生成 GIF 动图

```bash
ffmpeg -i video.mp4 -vf "fps=10,scale=640:-1" output.gif
```

---

**指南版本**: v1.0  
**最后更新**: 2026-06-25
