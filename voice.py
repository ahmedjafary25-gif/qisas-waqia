import asyncio, os
import edge_tts

def generate_voice(text, out_path="output/voice.mp3"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    text = text.strip()[:4000]
    
    async def _gen():
        comm = edge_tts.Communicate(text, "ar-EG-ShakibNeural")
        await comm.save(out_path)
    
    # حاول 3 مرات بصوتك انت بس
    for i in range(3):
        try:
            asyncio.run(_gen())
            if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
                print("OK ShakibNeural")
                return out_path
        except Exception as e:
            print(f"محاولة {i+1} فشلت: {e}")
    
    raise Exception("Shakib فشل بعد 3 محاولات")
