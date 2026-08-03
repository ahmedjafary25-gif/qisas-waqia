import os
from PIL import Image

try:
    RESAMPLE = Image.Resampling.LANCZOS
except AttributeError:
    RESAMPLE = Image.LANCZOS

def create_video(image_paths, audio_path, output_path="output/final/final_video.mp4"):
    from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    audio = AudioFileClip(audio_path)
    total_duration = audio.duration
    per_image = total_duration / len(image_paths) if image_paths else 5
    
    clips = []
    for img_path in image_paths:
        with Image.open(img_path) as im:
            im = im.convert("RGB")
            im = im.resize((1080, 1920), RESAMPLE)
            fixed = img_path + "_fixed.jpg"
            im.save(fixed, "JPEG")
            clip = ImageClip(fixed).set_duration(per_image)
            clips.append(clip)
    
    final = concatenate_videoclips(clips, method="compose")
    final = final.set_audio(audio)
    final.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac', threads=2)
    print(f"Saved {output_path}")
    return output_path
