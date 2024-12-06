from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('search_app.urls')),

    path('accounts/', include('allauth.urls')),  # allauthのURL設定を追加

    # path('accounts/', include('accounts.urls')),  # accountsアプリのURLをインクルード
]
