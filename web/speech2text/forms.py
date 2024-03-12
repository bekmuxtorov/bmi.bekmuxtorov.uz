from django import forms
from .models import Attempt


class AttemptRecordForm(forms.ModelForm):
    class Meta:
        model = Attempt
        fields = ('user', 'audio', 'audio_code')
    audio = forms.FileField(
        widget=forms.FileInput(attrs={'accept': "audio/*"}))
