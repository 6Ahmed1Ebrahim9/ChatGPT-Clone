from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes.as_view(), name='Routes'),
    path('api/chats/', views.ChatbotAPIView.as_view(), name='chatbot-api'),
    path('api/login/', views.LoginAPIView.as_view(), name='login-api'),
    path('api/register/', views.RegisterAPIView.as_view(), name='register-api'),
    path('api/logout/', views.LogoutAPIView.as_view(), name='logout-api'),
]