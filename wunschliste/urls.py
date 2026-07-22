from django.urls import path
from . import views

urlpatterns = [
    path('', views.public_view_login, name='public_view_login'),
    path('wunschliste/', views.public_wishes, name='public_wishes'),
    path('schenken/<int:wish_id>/', views.gift_wish, name='gift_wish'),
    
    path('create-wish/', views.create_wish, name='create_wish'),
    path('create-wish/login/', views.create_wish_login, name='create_wish_login'),
    path('create-wish/edit/<int:wish_id>/', views.edit_wish, name='edit_wish'),
    path('create-wish/delete/<int:wish_id>/', views.delete_wish, name='delete_wish'),

    path('gift-history/', views.gift_history, name='gift_history'),
    path('gift-history/login/', views.gift_history_login, name='gift_history_login'),
]