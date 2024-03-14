from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from random import randrange

from .forms import AttemptRecordForm
from .utils import to_text, send_text_to_telegram_bot
from .models import Attempt

MAX_FILE_SIZE = 1000000


def generate_audio_code():
    return randrange(100000, 999999)


@login_required(login_url='login')
def speech_to_text(request):
    first_audio_code = generate_audio_code()
    if request.method == 'POST':
        attempt_audio_code = request.POST.get("attempt_audio_code")
        if attempt_audio_code:
            instance = Attempt.objects.filter(
                audio_code=int(attempt_audio_code)).first()
            instance.remove_audio_file()

        # FOR send_text_to_telegram_bot BUTTON
        audio_code_for_send_text = request.POST.get("audio_code_for_send_text")
        if audio_code_for_send_text:
            instance = Attempt.objects.filter(
                audio_code=int(audio_code_for_send_text)).first()
            if not instance:
                return render(request, 'stt.html', {"form": AttemptRecordForm(), "status_code": 407, "audio_code": first_audio_code})

            status_ok = send_text_to_telegram_bot(instance)
            if not status_ok:
                return render(request, 'stt.html', {"form": AttemptRecordForm(), "status_code": 406, "audio_code": instance.audio_code, "result_data": {"text": instance.text}, "audio": instance.audio})
            return render(request, 'stt.html', {"form": AttemptRecordForm(), "status_code": 405, "audio_code": instance.audio_code, "result_data": {"text": instance.text}, "audio": instance.audio})

        if request.POST.get("audio_code"):
            audio_code = request.POST.get("audio_code")
            audio_data = Attempt.objects.filter(
                audio_code=int(audio_code)).first()
            if not audio_data:
                return render(request, 'stt.html', {"form": AttemptRecordForm(), "status_code": 400, 'audio_code': audio_code})

            audio_url = audio_data.audio
            result_data = to_text(audio_url)
            audio_data.set_text(result_text=result_data.get("text"))
            return render(request, 'stt.html', {"form": AttemptRecordForm(), "audio": audio_url, "result_data": result_data, 'audio_code': audio_code})

        form = AttemptRecordForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.audio_code = first_audio_code
            audio_size = form.instance.audio.size
            if audio_size >= MAX_FILE_SIZE:
                return render(request, "stt.html", context={"status_code": 401, "form": AttemptRecordForm(), 'audio_code': first_audio_code})
            attempt_instance = form.save()
            result_data = to_text(attempt_instance.audio.name)
            attempt_instance.set_text(result_data.get("text"))

            return render(request, 'stt.html', {'audio': form.instance.audio, "form": AttemptRecordForm(), "result_data": result_data, 'audio_code': first_audio_code})
        else:
            print(form.errors)
    else:
        form = AttemptRecordForm()
    return render(request, 'stt.html', {'form': form, 'audio_code': first_audio_code})
