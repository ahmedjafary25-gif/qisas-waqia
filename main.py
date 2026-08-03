
import os, json, glob
from src.story import generate_story
from src.images import generate_images_for_scenes
from src.voice import generate_voice_sync
from src.video import create_video_from_assets

def main():
    print("Starting Qisas free project")
    data = generate_story()
    print(json.dumps(data, ensure_ascii=False, indent=2))
    title = data.get("title","qissa")
    best_hook = data.get("best_hook","")
    full_story = f"{best_hook}. {data.get('story','')}"
    scenes = data.get("scenes",[])[:3]
    os.makedirs("output", exist_ok=True)
    open("output/story.json","w", encoding="utf-8").write(json.dumps(data, ensure_ascii=False, indent=2))
    with open("prompts/character.txt", encoding="utf-8") as f:
        char_prompt = f.read()
    all_vars = generate_images_for_scenes(scenes, char_prompt, num_variants=4)
    selected = [imgs[0] for imgs in all_vars if imgs]
    audio_path = generate_voice_sync(full_story, "output/audio/voice.mp3", voice="shakib")
    video_path = create_video_from_assets(selected, audio_path, best_hook, f"output/final/{title[:20]}.mp4")
    print(f"Done: {video_path}")

if __name__ == "__main__":
    main()
