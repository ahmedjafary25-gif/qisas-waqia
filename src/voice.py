
import asyncio, os
VOICES = {"shakib": "ar-EG-ShakibNeural", "salma": "ar-EG-SalmaNeural"}

async def generate_voice_free(text, output_path="output/audio/voice.mp3", voice="shakib"):
    os.makedirs("output/audio", exist_ok=True)
    try:
        import edge_tts
        voice_name = VOICES.get(voice, VOICES["shakib"])
        print(f"Generating voice {voice_name}")
        comm = edge_tts.Communicate(text, voice_name)
        await comm.save(output_path)
        return output_path
    except Exception as e:
        print(f"edge-tts error {e}, creating silent fallback")
        from pydub import AudioSegment
        AudioSegment.silent(duration=15000).export(output_path, format="mp3")
        return output_path

def generate_voice_sync(text, output_path="output/audio/voice.mp3", voice="shakib"):
    return asyncio.run(generate_voice_free(text, output_path, voice))
