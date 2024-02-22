from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from django.http import HttpResponse

from .models import User


def login_view(request):
    if request.method == 'POST':
        confirm_code = request.POST["confirm_code"]

        if not confirm_code.isdigit():
            return render(request, "login.html", context={"status_code": 401})

        is_exists_confirm_code = User.objects.filter(
            confirm_code=confirm_code).exists()
        if not is_exists_confirm_code:
            return render(request, "login.html", context={"status_code": 401})

        user_data = User.objects.filter(confirm_code=confirm_code).first()
        if user_data:
            login(request, user_data)
            return redirect('stt')
        else:
            redirect('login')
    return render(request, 'login.html')
