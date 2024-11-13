# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import SignUpForm
from django.contrib.auth import logout,render
from django.shortcuts import redirect
from django.views import View


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')  # 登録後にログイン画面にリダイレクト
    template_name = 'signup.html'

class CustomLogoutView(View):
    def get(self, request):
        logout(request)  # ユーザーをログアウトさせる
        return render('signup.html')  # ログアウト後のリダイレクト先