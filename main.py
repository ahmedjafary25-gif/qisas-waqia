import os, glob, json
from src.story import generate_story
from src.voice import generate_voice
from src.video import create_video

def main():
    os.makedirs("output/images", exist_ok=True)
    os.makedirs("output/final", exist_ok=True)
    
    print("1. Story...")
        result = generate_story()     if isinstance(result, dict):         title = result.get('title', 'قصة واقعية')         script = result.get('script', result.get('story', ''))         desc = result.get('description', script[:100])     else:         # لو بيرجع tuple         try:             title, script, desc = result[0], result[1], result[2] if len(result) > 2 else result[1][:100]         except:             title = "قصة واقعية"             script = str(result)             desc = script[:100]
    print(f"Title: {title}")
    with open("output/story.json","w",encoding="utf-8") as f:
        json.dump({"title":title,"script":script,"description":desc},f,ensure_ascii=False,indent=2)
    
    print("2. Voice...")
    audio = generate_voice(script, "output/voice.mp3")
    
    print("3. Images...")
    imgs = sorted(glob.glob("output/images/*.jpg"))
    if not imgs:
        print("Creating placeholders")
        from PIL import Image
        try: RESAMPLE = Image.Resampling.LANCZOS
        except: RESAMPLE = Image.LANCZOS
        for i in range(3):
            im = Image.new('RGB',(1080,1920),color=(20,20,40))
            p=f"output/images/scene_{i}.jpg"
            im.save(p)
            imgs.append(p)
    
    print("4. Video...")
    final = create_video(imgs, audio, "output/final/final_video.mp4")
    
    print("5. YouTube...")
    try:
        from src.youtube import upload_to_youtube
        upload_to_youtube(final, title, desc)
    except Exception as e:
        print(f"YT fail: {e}")
    
    print(f"Done: {final}")

if __name__ == "__main__":
    main()
