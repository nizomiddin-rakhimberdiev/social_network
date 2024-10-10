from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('verify_email/', views.verify_email, name='verify_email'),
    path('', views.home, name='home'),  # Home sahifasi
]