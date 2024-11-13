# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView、
from .forms import SignUpForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import 
from django.contrib import messages


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')  # 登録後にログイン画面にリダイレクト
    template_name = 'signup.html'

class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)  # ユーザーをログアウト
        messages.success(request, 'ログアウトしました')  # ログアウト後のメッセージ
        return redirect('signup')  # リダイレクト先（URL名を指定）