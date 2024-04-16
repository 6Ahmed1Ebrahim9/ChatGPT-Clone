from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes.as_view(), name='chatbot'),
    path('api/chats/', views.ChatbotAPIView.as_view(), name='chatbot-api'),
]