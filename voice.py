import asyncio, os

def generate_voice(text, out_path="output/voice.mp3"):
    """Wrapper that GitHub can import - name fixed"""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    text = text.strip()[:4000]
    
    # Try edge-tts first
    try:
        import edge_tts
        async def _gen(voice):
            try:
                comm = edge_tts.Communicate(text, voice)
                await comm.save(out_path)
                return os.path.getsize(out_path) > 1000
            except Exception as e:
                print(f"edge fail {voice}: {e}")
                return False
        
        for v in ["ar-EG-SalmaNeural", "ar-EG-ShakibNeural", "ar-SA-HamedNeural"]:
            print(f"Trying {v}")
            try:
                ok = asyncio.run(_gen(v))
                if ok:
                    print(f"OK {v}")
                    return out_path
            except Exception as e:
                print(e)
    except Exception as e:
        print(f"edge import fail: {e}")
    
    # Fallback gTTS
    print("Fallback gTTS")
    try:
        from gtts import gTTS
        gTTS(text, lang='ar').save(out_path)
        return out_path
    except Exception as e:
        print(f"gTTS fail {e}")
        from pydub import AudioSegment
        AudioSegment.silent(duration=10000).export(out_path, format="mp3")
        return out_path
