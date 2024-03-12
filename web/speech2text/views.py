from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from random import randrange

from .forms import AttemptRecordForm
from .utils import to_text
from .models import Attempt

MAX_FILE_SIZE = 1000000


def generate_audio_code():
    return randrange(100000, 999999)


@login_required(login_url='login')
def speech_to_text(request):
    first_audio_code = generate_audio_code()
    if request.method == 'POST':
        if request.POST.get("audio_code"):
            audio_code = request.POST.get("audio_code")
            audio_data = Attempt.objects.filter(
                audio_code=int(audio_code)).first()
            if not audio_data:
                return render(request, 'stt.html', {"form": AttemptRecordForm(), "status_code": 400, 'audio_code': first_audio_code})

            audio_url = audio_data.audio
            result_data = to_text(audio_url)
            return render(request, 'stt.html', {"form": AttemptRecordForm(), "audio": audio_url, "result_data": result_data, 'audio_code': first_audio_code})

        form = AttemptRecordForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            audio_size = form.instance.audio.size
            if audio_size >= MAX_FILE_SIZE:
                return render(request, "stt.html", context={"status_code": 401, "form": AttemptRecordForm(), 'audio_code': first_audio_code})
            attempt_instance = form.save()
            result_data = to_text(attempt_instance.audio.name)

            return render(request, 'stt.html', {'audio': form.instance.audio, "form": AttemptRecordForm(), "result_data": result_data, 'audio_code': first_audio_code})
        else:
            print(form.errors)
    else:
        form = AttemptRecordForm()
    return render(request, 'stt.html', {'form': form, 'audio_code': first_audio_code})
