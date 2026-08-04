1. افتح: https://modal.com/signup وسجل بجوجل (هتاخد 30$ مجانا = 15 ساعة GPU)

2. على جهازك افتح CMD واكتب:
pip install modal
modal token new
# هيفتح لينك دوس Allow

3. اعمل Secret فيه مفاتيحك:
modal secret create qisas-secrets --from-dotenv .env

# ملف .env لازم يكون فيه:
FISH_API_KEY=xxx
FISH_VOICE_ID=98c1f6dca0614f679046c5a67eb1a27d
GROQ_API_KEY=xxx
PEXELS_API_KEY=xxx
YT_TOKEN_JSON={"...":"..."}

4. شغل البوت:
modal deploy modal_app.py
# هيقولك اشتغل كل 6 ساعات تلقائي على T4 ببلاش

5. عشان تشغله حالا:
modal run modal_app.py

6. هيعمل فيديو 15 دقيقة في دقيقة ونص بـ h264_nvenc GPU ويرفعه يوتيوب

# التكلفة:
# كل فيديو = 0.02$ على T4
# 4 فيديوهات يوميا = 0.08$ يوميا = 2.4$ شهريا
# وانت معاك 30$ مجانا يعني 12 شهر ببلاش!
