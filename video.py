import os
from PIL import Image

try:
    RESAMPLE = Image.Resampling.LANCZOS
except AttributeError:
    RESAMPLE = Image.LANCZOS

def create_video(image_paths, audio_path, output_path="output/final/final_video.mp4"):
    from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    if not image_paths:
        raise ValueError("No images")
    
    audio = AudioFileClip(audio_path)
    total_duration = audio.duration
    per_image = total_duration / len(image_paths) if image_paths else 5
    
    clips = []
    for img_path in image_paths:
        try:
            with Image.open(img_path) as im:
                im = im.convert("RGB")
                im = im.resize((1080, 1920), RESAMPLE)
                fixed = img_path + "_fixed.jpg"
                im.save(fixed, "JPEG")
                clip = ImageClip(fixed).set_duration(per_image)
                clips.append(clip)
        except Exception as e:
            print(f"Img err {img_path}: {e}")
            continue
    
    if not clips:
        raise ValueError("No valid clips")
    
    final = concatenate_videoclips(clips, method="compose")
    final = final.set_audio(audio)
    final.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac', threads=2)
    print(f"Saved {output_path}")
    return output_path
