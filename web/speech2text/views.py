from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import AttemptRecordForm
from .utils import to_text


@login_required(login_url='login')
def speech_to_text(request):
    if request.method == 'POST':
        form = AttemptRecordForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            audio_size = form.instance.audio.size
            if audio_size >= 1000000:
                return render(request, "stt.html", context={"status_code": 401, "form": AttemptRecordForm()})
            attempt_instance = form.save()
            result_data = to_text(attempt_instance.audio.name)
            
            return render(request, 'stt.html', {'audio': form.instance.audio, "form": AttemptRecordForm(), "result_data": result_data})
        else:
            print(form.errors)
    else:
        form = AttemptRecordForm()
    return render(request, 'stt.html', {'form': form})
