from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .views import CustomLogoutView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),

]
