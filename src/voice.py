import asyncio, os

def generate_voice(text, out_path="output/voice.mp3"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    text = text.strip()[:4000]
    try:
        import edge_tts
        async def _gen(voice):
            try:
                comm = edge_tts.Communicate(text, voice)
                await comm.save(out_path)
                return os.path.getsize(out_path) > 1000
            except:
                return False
        for v in ["ar-EG-SalmaNeural", "ar-EG-ShakibNeural", "ar-SA-HamedNeural"]:
            try:
                ok = asyncio.run(_gen(v))
                if ok:
                    return out_path
            except:
                pass
    except:
        pass
    from gtts import gTTS
    gTTS(text, lang='ar').save(out_path)
    return out_path
