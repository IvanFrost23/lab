from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('validate_username/', views.validate_username, name='validate_username'),
    path('profile/', views.profile, name='profile')
]
