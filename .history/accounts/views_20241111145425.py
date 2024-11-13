from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')  # ログイン後にリダイレクトするURLに変更
            else:
                return HttpResponse("無効なユーザー名またはパスワードです。")
        else:
            return HttpResponse("フォームが無効です。")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# Create your views here.
