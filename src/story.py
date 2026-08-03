
import os, json
from groq import Groq

def generate_story():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {
            "title": "الورقة اللي في جيبي",
            "best_hook": "الورقة اللي في جيبي دي بقالها مية سنة وكل اللي مسكها اختفى",
            "story": "لقيت الورقة دي في درج المكتب الخشبي بتاع جدي. مكتوب عليها لا تفتح قبل 50 سنة. لما فتحتها لقيت خريطة لقصر في الواحات. دوست REC وبدأت اقرا.",
            "scenes": [
                "wide shot, sitting at wooden desk in traditional library studio, holding old yellow letter, vintage microphone and mixer visible, warm amber light",
                "close up, hands holding torn old paper with arabic handwriting, patterned shawl edge visible",
                "medium shot, putting folded old paper into shirt pocket, serious expression"
            ],
            "hooks": ["الصدمة", "اللغز", "الوثيقة"]
        }
    client = Groq(api_key=api_key)
    prompt = "اكتب قصة واقعية قصيرة 180 كلمة عامية مصرية عن ورقة قديمة في استوديو تسجيل. رجع JSON فقط: {title, best_hook, story, scenes: [3 English prompts], hooks}"
    completion = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "system", "content": "ترجع JSON فقط."},{"role": "user", "content": prompt}], temperature=0.9)
    content = completion.choices[0].message.content
    try:
        s = content.find("{"); e = content.rfind("}")+1
        return json.loads(content[s:e])
    except:
        return {"title": "قصة من الارشيف", "best_hook": content[:100], "story": content, "scenes": ["wide shot in library", "close up old paper", "putting paper in pocket"], "hooks": []}
