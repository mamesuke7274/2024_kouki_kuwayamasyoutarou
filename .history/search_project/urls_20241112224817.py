from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', include('search_app.urls')),
    path('', include('django.contrib.auth.urls')),  # 修正済み
]
