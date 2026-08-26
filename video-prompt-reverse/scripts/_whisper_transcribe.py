#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_whisper_transcribe.py — faster-whisper 转写（在 /tmp/whisper_env venv 中运行）
被 step1_parse.py 以 subprocess 调用。输出最后一行 |||JSON
"""
import json, sys

def main():
    video = sys.argv[1]
    from faster_whisper import WhisperModel
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, info = model.transcribe(video, language="zh", beam_size=5)
    text = "".join(s.text for s in segments)
    print("|||" + json.dumps({"text": text}, ensure_ascii=False))

if __name__ == "__main__":
    main()
