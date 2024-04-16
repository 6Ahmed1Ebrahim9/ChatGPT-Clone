from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone
import openai

openai_api_key = 'sk-proj-fwJ2fJWURjqaFE9BaB6fT3BlbkFJokkcipCVNr9EUD0WTTmC'
openai.api_key = openai_api_key


class getRoutes(APIView):
    def get(self, request):
        routes = [
            '/api/chats/',
            '/api/login/',
            '/api/register/',
            '/api/logout/',
        ]
        return Response({'routes': routes})

class ChatbotAPIView(APIView):
    def get(self, request):
        chats = Chat.objects.filter(user=request.user)
        return Response({'chats': [{'message': chat.message, 'response': chat.response} for chat in chats]})

    def post(self, request):
        message = request.data.get('message')
        response = ask_openai(message)
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return Response({'message': message, 'response': response}, status=status.HTTP_201_CREATED)

def ask_openai(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    answer = response.choices[0].message.content.strip()
    return answer


