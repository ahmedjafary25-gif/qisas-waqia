import os, json
from groq import Groq

def generate_story():
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    prompt = """اكتب قصة واقعية مشوقة جدا باللهجة المصرية العامية، قصيرة ومؤثرة، تنفع فيديو شورتس 60 ثانية.
    رجع JSON فقط:
    {"title": "عنوان", "script": "القصة 150 كلمة", "description": "وصف يوتيوب"}"""
    comp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        response_format={"type": "json_object"}
    )
    data = json.loads(comp.choices[0].message.content)
    return data['title'], data['script'], data.get('description', '')
