from django.urls import path 
from . import views 

# 画像追加のためのインポート
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [  
    path('', views.product_list, name='product_list'),
    path('product/new/', views.product_create, name='product_create'), 
    path('product/<int:pk>/', views.product_detail, name='product_detail'), 
    path('product/<int:pk>/edit/',  views.product_update, name='product_update'), 
    path('product/<int:pk>/delete',  views.product_delete, name='product_delete'), 
    path('product/<int:pk>/detail-api/', views.product_detail_api, name='product_detail_api'),

    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),

    path('product/<int:pk>/detail-api/', views.product_detail_api, name='product_detail_api'),
    path('product/<int:product_id>/add-review/', views.add_review, name='add_review'),
    path('product/<int:pk>/reviews-api/', views.product_reviews_api, name='product_reviews_api'),

    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
]

# urlの結びつけ
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

