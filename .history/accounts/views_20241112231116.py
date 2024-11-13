# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import SignUpForm

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')  # 登録後にログイン画面にリダイレクト
    template_name = 'templates/signup.html'

