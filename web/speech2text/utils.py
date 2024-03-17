import requests
import os

from django.conf import settings
from django.utils import timezone

from accounts.models import User
from .models import Attempt

STT_API_KEY = settings.STT_API_KEY
MEDIA_ROOT = settings.MEDIA_ROOT
BOT_TOKEN = settings.BOT_TOKEN

url = "https://mohir.ai/api/v1/stt"
headers = {'Authorization': f'{STT_API_KEY}'}


def can_use(user: User) -> bool:
    attempt_count = Attempt.objects.filter(
        user=user,
        created_at__day=timezone.now().day
    ).count()

    return attempt_count <= user.daily_use


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


def send_text_to_telegram_bot(attempt: Attempt):
    chat_id = attempt.user.telegram_id
    message = f"✅ Audio code: {attempt.audio_code}\n\n"
    message += attempt.text
    message += "\n\n👉speechtotext.bekmuxtorov.uz "
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    data = requests.get(url).json()
    return data.get("ok")
