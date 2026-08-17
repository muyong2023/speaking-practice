#!/usr/bin/env python3
"""
为「对话跟读」生成示范音频。

用法：
    pip install edge-tts
    python3 gen_audio.py

输出：
    audio/meet-1.mp3, audio/meet-2.mp3, ... audio/road-8.mp3

把 audio/ 目录和 duihua-genudu.html 放在同一层，页面会自动优先播 mp3，
找不到文件才回落到浏览器自带的语音合成。

音色（微软神经语音，一男一女）：
    女  zh-CN-XiaoxiaoNeural   自然、偏年轻，适合学生角色
    男  zh-CN-YunxiNeural      清亮男声，适合同龄男生
    男  zh-CN-YunjianNeural    更成熟的男声，适合服务员/路人
换音色直接改下面的 VOICE_F / VOICE_M。
可用音色列表：edge-tts --list-voices | grep zh-CN
"""

import asyncio
import os
import sys

VOICE_F = "zh-CN-XiaoxiaoNeural"
VOICE_M = "zh-CN-YunxiNeural"
RATE = "-10%"          # 教学用稍慢一点；不想放慢就设成 "+0%"
OUT_DIR = "audio"

# 和 HTML 里的 DIALOGS 保持一致：id、每个角色的性别、每句的说话人和文本
DIALOGS = [
    ("meet", {"A": "m", "B": "f"}, [
        ("A", "你好！我叫李明。"),
        ("B", "你好，李明！我是王小美。"),
        ("A", "认识你很高兴。"),
        ("B", "我也很高兴。你是哪国人？"),
        ("A", "我是美国人。你呢？"),
        ("B", "我是中国人，我住在北京。"),
        ("A", "太好了！我们做朋友吧。"),
        ("B", "好啊！这是我的电话号码。"),
    ]),
    ("food", {"A": "f", "B": "m"}, [
        ("A", "欢迎光临！你想吃什么？"),
        ("B", "我想吃一碗牛肉面。"),
        ("A", "你要喝什么饮料？"),
        ("B", "请给我一杯热茶。"),
        ("A", "好的，请稍等。"),
        ("B", "谢谢！一共多少钱？"),
        ("A", "一共二十五块。"),
        ("B", "给你钱。再见！"),
    ]),
    ("road", {"A": "m", "B": "f"}, [
        ("A", "请问，地铁站在哪里？"),
        ("B", "一直往前走，然后向右拐。"),
        ("A", "离这里远吗？"),
        ("B", "不远，走路十分钟就到。"),
        ("A", "我可以坐公共汽车吗？"),
        ("B", "可以，你坐三路车。"),
        ("A", "太谢谢你了！"),
        ("B", "不客气，祝你好运！"),
    ]),
]


async def main():
    try:
        import edge_tts
    except ImportError:
        sys.exit("缺少依赖，先跑：pip install edge-tts")

    os.makedirs(OUT_DIR, exist_ok=True)
    total = 0

    for dlg_id, roles, lines in DIALOGS:
        for i, (speaker, text) in enumerate(lines, start=1):
            voice = VOICE_M if roles.get(speaker) == "m" else VOICE_F
            path = os.path.join(OUT_DIR, f"{dlg_id}-{i}.mp3")
            await edge_tts.Communicate(text, voice, rate=RATE).save(path)
            total += 1
            print(f"  {path}  [{voice}]  {text}")

    print(f"\n完成，共 {total} 个文件，输出在 {OUT_DIR}/")
    print("把 audio/ 和 html 放同一目录，起个本地服务器就能听："
          "\n    python3 -m http.server 8000")


if __name__ == "__main__":
    asyncio.run(main())
