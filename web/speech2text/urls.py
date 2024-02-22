from django.urls import path
from .views import speech_to_text


urlpatterns = [
    path('', speech_to_text, name='stt')
]
