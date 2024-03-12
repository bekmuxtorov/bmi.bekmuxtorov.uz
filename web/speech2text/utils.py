import requests
import os

from django.conf import settings

STT_API_KEY = settings.STT_API_KEY
MEDIA_ROOT = settings.MEDIA_ROOT

url = "https://mohir.ai/api/v1/stt"
headers = {'Authorization': f'{STT_API_KEY}'}


def to_text(audio_url: str) -> dict:
    file = os.path.join(MEDIA_ROOT, str(audio_url))
    files = {'file': open(file, 'rb')}
    params = {
        'return_offsets': 'false',
        'run_diarization': 'false',
        'blocking': 'false',
    }
    # response = requests.post(url, headers=headers, files=files, params=params)
    # data = response.json()
    data = {'id': 'stt/8b3ac67a-7297-4fe3-a62b-fff3bcd10ad4/5d2eb5b4-5dde-4ab2-a46f-5177e83c7bec',
            'progress': 1.0, 'result': {'range': [
                0, 8281], 'text': 'bu tekshirish uchun kiritilgan matn hisoblanadi asadbek muxtorov tomonidan shunday dastur ustida ishlar boshlab yuborilgan'}, 'status': 'SUCCESS'}
    return {"status": data.get("status"), "text": data.get("result").get("text")} if data else None
