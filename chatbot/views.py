from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone
import openai

# Secret key for OpenAI API
openai_api_key = 'api-key-here' # Replace 'api-key-here' with your OpenAI API key
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
        try:
            chats = Chat.objects.filter(user=request.user)
            return Response({'chats': [{'message': chat.message, 'response': chat.response} for chat in chats]})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            message = request.data.get('message')
            if not message:
                raise ValidationError("Message field is required")
            
            response = ask_openai(message)
            chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
            chat.save()
            return Response({'message': message, 'response': response}, status=status.HTTP_201_CREATED)
        except ValidationError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

class LoginAPIView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            if not username or not password:
                raise ValidationError("Username and password are required")

            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('chatbot-api')
            else:
                error_message = 'Invalid username or password'
                return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RegisterAPIView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            email = request.data.get('email')
            password1 = request.data.get('password1')
            password2 = request.data.get('password2')

            if not (username and email and password1 and password2):
                raise ValidationError("All fields are required")

            if password1 != password2:
                raise ValidationError("Passwords do not match")

            user = User.objects.create_user(username, email, password1)
            user.save()
            auth.login(request, user)
            return redirect('chatbot-api')
        except ValidationError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutAPIView(APIView):
    def post(self, request):
        try:
            auth.logout(request)
            return redirect('login-api')
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
