import modal

# صورة فيها ffmpeg + python + cuda
image = (
    modal.Image.from_registry("nvidia/cuda:12.1.0-runtime-ubuntu22.04", add_python="3.10")
    .apt_install("ffmpeg", "git")
    .pip_install(
        "groq",
        "fish-audio-sdk",
        "edge-tts",
        "moviepy==1.0.3",
        "Pillow",
        "requests",
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        "pexels_api",
    )
    .add_local_dir(".", remote_path="/root")
)

app = modal.App("qisas-gpu-worker", image=image)

# Secrets اللي هتحطها في Modal
@app.function(
    gpu="T4",
    timeout=1800,
    secrets=[
        modal.Secret.from_name("qisas-secrets"),  # هنعمله تحت
    ],
)
def generate_video():
    import subprocess
    import os
    os.chdir("/root")
    print("🎬 Starting 15min video on T4 GPU...")
    # يحاول GPU ولو مفيش يرجع CPU
    result = subprocess.run(["python3", "main.py"], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    return "Done"

# يشتغل كل 6 ساعات تلقائي ببلاش
@app.function(schedule=modal.Period(hours=6), secrets=[modal.Secret.from_name("qisas-secrets")])
def scheduled():
    generate_video.local()

@app.function()
@modal.web_endpoint(method="POST")
def trigger():
    generate_video.spawn()
    return {"status": "started on T4 GPU"}

if __name__ == "__main__":
    generate_video.local()
