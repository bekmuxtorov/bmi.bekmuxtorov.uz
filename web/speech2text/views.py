from django.shortcuts import render
from .models import Attempt

from django.core.files.storage import FileSystemStorage

from django.shortcuts import render, redirect
from .models import Attempt
from .forms import AttemptRecordForm


def speech_to_text(request):
    if request.method == 'POST':
        form = AttemptRecordForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            print(form.instance.audio)
            return render(request, 'stt.html', {'audio': form.instance.audio})
        else:
            print(form.errors)
    else:
        form = AttemptRecordForm()
    return render(request, 'stt.html', {'form': form})
