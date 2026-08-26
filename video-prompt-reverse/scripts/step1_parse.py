#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Step1 视频解析：PySceneDetect 镜头切分 + ffmpeg 抽帧 + faster-whisper 转写
底座：Breakthrough/PySceneDetect (5122★ BSD-3) + ffmpeg + faster-whisper(本地)
用法：python3 step1_parse.py <video.mp4> [输出目录]
输出：<输出目录>/parse.json {duration, scenes:[{idx,start,end,frame}], transcript}
零成本：全程本地工具，无付费 API 依赖
"""
import json, os, subprocess, sys

FFMPEG = "/usr/local/bin/ffmpeg"  # launchd PATH 无 ffmpeg，必须绝对路径（08-23 踩坑）
WHISPER_PY = os.environ.get("WHISPER_PY", "python3")  # faster-whisper 环境，可配置
WHISPER_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_whisper_transcribe.py")

def main():
    video = sys.argv[1]
    outdir = sys.argv[2] if len(sys.argv) > 2 else "/tmp/vpr_out"
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(os.path.join(outdir, "frames"), exist_ok=True)

    # 1. 视频时长
    probe = subprocess.run([FFMPEG, "-i", video], capture_output=True, text=True)
    duration = 0.0
    for line in probe.stderr.splitlines():
        if "Duration:" in line:
            try:
                h, m, s = line.split("Duration:")[1].split(",")[0].strip().split(":")
                duration = int(h)*3600 + int(m)*60 + float(s)
            except Exception:
                pass
            break
    if duration <= 0:
        print("❌ 无法读取视频时长"); sys.exit(1)

    # 2. 镜头切分（三级：PySceneDetect → ffmpeg scene → 均匀切段）
    # ⚠️ 环境坑（2026-08-26）：本机 OpenCV 4.13 + PySceneDetect 0.7.1 decode thread 兼容 bug，自动降级
    scenes = []
    try:
        from scenedetect import SceneManager, open_video, ContentDetector
        video_stream = open_video(video)
        sm = SceneManager()
        sm.add_detector(ContentDetector(threshold=27.0))
        sm.detect_scenes(video_stream, show_progress=False)
        scene_list = sm.get_scene_list()
        video_stream.release()
        for i, sc in enumerate(scene_list):
            start = sc[0].get_seconds()
            end = sc[1].get_seconds()
            scenes.append({"idx": i+1, "start": round(start, 2), "end": round(end, 2), "frame": ""})
    except Exception:
        try:
            import re
            r = subprocess.run([FFMPEG, "-i", video, "-vf", "select='gt(scene,0.3)',showinfo", "-f", "null", "-"], capture_output=True, text=True)
            times = sorted(set(round(float(m.group(1)), 2) for m in re.finditer(r"pts_time:([0-9.]+)", r.stderr) if float(m.group(1)) > 0.5))
            bounds = [0.0] + times + [duration]
            for i in range(len(bounds) - 1):
                scenes.append({"idx": i+1, "start": bounds[i], "end": bounds[i+1], "frame": ""})
            print(f"ℹ️ PySceneDetect 不可用，已用 ffmpeg scene 检测切分（{len(scenes)} 段，阈值 0.3）")
        except Exception as e2:
            print(f"⚠️ ffmpeg scene 也失败({e2})，降级为按 3 秒均匀切段")
            t = 0.0
            i = 1
            while t < duration:
                scenes.append({"idx": i, "start": round(t, 2), "end": round(min(t+3, duration), 2), "frame": ""})
                t += 3; i += 1
    if not scenes:
        scenes = [{"idx": 1, "start": 0.0, "end": round(duration, 2), "frame": ""}]

    # 3. 每镜头抽 1 帧关键帧
    for sc in scenes:
        mid = (sc["start"] + sc["end"]) / 2
        fp = os.path.join(outdir, "frames", f"frame_{sc['idx']:03d}.jpg")
        r = subprocess.run(
            [FFMPEG, "-ss", f"{mid:.2f}", "-i", video, "-frames:v", "1", "-q:v", "3", "-y", fp],
            capture_output=True)
        if os.path.exists(fp) and os.path.getsize(fp) > 0:
            sc["frame"] = fp
        else:
            print(f"⚠️ 镜头{sc['idx']} 抽帧失败")

    # 4. faster-whisper 完整转写（本地 venv）
    transcript = ""
    if os.path.exists(WHISPER_PY) and os.path.exists(WHISPER_SCRIPT):
        r = subprocess.run([WHISPER_PY, WHISPER_SCRIPT, video], capture_output=True, text=True, timeout=1800)
        if r.returncode == 0:
            try:
                transcript = json.loads(r.stdout.strip().split("|||")[-1])["text"]
            except Exception:
                transcript = r.stdout.strip()
        else:
            print(f"⚠️ 转写失败：{r.stderr[-200:]}")
    else:
        print("⚠️ whisper venv 不存在，跳过转写（需 /tmp/whisper_env）")

    out = {"duration": round(duration, 2), "scene_count": len(scenes), "scenes": scenes, "transcript": transcript}
    with open(os.path.join(outdir, "parse.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"✅ Step1 完成：时长 {duration:.1f}s / {len(scenes)} 镜头 / 转写 {len(transcript)} 字")
    print(f"   输出：{outdir}/parse.json")

if __name__ == "__main__":
    main()
