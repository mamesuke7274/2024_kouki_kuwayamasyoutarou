# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import SignUpForm



class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')  # 登録後にログイン画面にリダイレクト
    template_name = 'signup.html'

class CustomLogoutView(View):
    def get(self, request):
        logout(request)  # ユーザーをログアウトさせる
        return redirect('login')  # ログアウト後のリダイレクト先