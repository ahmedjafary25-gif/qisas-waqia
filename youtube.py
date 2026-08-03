import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_youtube(video_path, title, description=""):
    try:
        print(f"Checking YT creds...")
        cid = os.getenv("YOUTUBE_CLIENT_ID")
        csecret = os.getenv("YOUTUBE_CLIENT_SECRET")
        rtoken = os.getenv("YOUTUBE_REFRESH_TOKEN")
        if not cid or not csecret or not rtoken:
            print("❌ Missing YT secrets")
            return None
        
        print("Uploading to YouTube...")
        creds = Credentials(
            None,
            refresh_token=rtoken,
            client_id=cid,
            client_secret=csecret,
            token_uri="https://oauth2.googleapis.com/token",
            scopes=["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube"]
        )
        youtube = build("youtube", "v3", credentials=creds)
        
        body = {
            "snippet": {
                "title": (title[:90] + " #Shorts"),
                "description": description + "\n\n#قصص_واقعية #قصص",
                "tags": ["قصص واقعية", "قصص"],
                "categoryId": "22"
            },
            "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}
        }
        media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)
        req = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
        res = req.execute()
        print(f"✅ Uploaded: https://youtu.be/{res['id']}")
        return res['id']
    except Exception as e:
        print(f"❌ YouTube upload failed: {e}")
        import traceback
        traceback.print_exc()
        return None
