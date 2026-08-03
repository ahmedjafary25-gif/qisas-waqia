
import os, requests, time
from urllib.parse import quote

def generate_images_for_scenes(scenes, character_prompt, num_variants=4):
    os.makedirs("output/images", exist_ok=True)
    meta_key = os.getenv("META_API_KEY")
    all_images = []
    for scene_idx, scene_desc in enumerate(scenes, 1):
        full_prompt = f"{character_prompt}, {scene_desc}, cinematic, volumetric lighting, ultra detailed, 8k"
        print(f"\nScene {scene_idx}: {scene_desc[:80]}")
        scene_images = []
        for variant in range(num_variants):
            seed = 1996 + scene_idx*100 + variant
            out_path = f"output/images/scene_{scene_idx}_variant_{variant+1}.jpg"
            try:
                url = f"https://image.pollinations.ai/prompt/{quote(full_prompt)}?width=1280&height=720&seed={seed}&nologo=true&enhance=true"
                r = requests.get(url, timeout=90)
                if r.status_code == 200:
                    open(out_path, "wb").write(r.content)
                    print(f"  OK {out_path}")
                    scene_images.append(out_path)
            except Exception as e:
                print(f"  Error {e}")
            time.sleep(2)
        all_images.append(scene_images)
    return all_images
