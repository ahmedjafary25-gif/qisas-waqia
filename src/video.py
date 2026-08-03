
import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip

def create_video_from_assets(image_paths, audio_path, hook_text, output_path="output/final/video.mp4"):
    os.makedirs("output/final", exist_ok=True)
    if not os.path.exists(audio_path) or not image_paths:
        print("Missing assets")
        return None
    try:
        audio = AudioFileClip(audio_path)
        dur = audio.duration / len(image_paths)
        clips = []
        for p in image_paths:
            if not os.path.exists(p): continue
            c = ImageClip(p).set_duration(dur).resize(height=720).set_position("center")
            c = c.resize(lambda t: 1 + 0.05*t)
            clips.append(c)
        if not clips: return None
        video = concatenate_videoclips(clips, method="compose").set_audio(audio)
        try:
            txt = TextClip(hook_text, fontsize=40, color='white', stroke_color='black', stroke_width=2, method='caption', size=(1000, None))
            txt = txt.set_position('center').set_duration(3)
            video = CompositeVideoClip([video, txt])
        except Exception as e:
            print(f"text overlay skip {e}")
        video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
        return output_path
    except Exception as e:
        print(f"video error {e}")
        import traceback; traceback.print_exc()
        return None
