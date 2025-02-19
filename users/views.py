from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from .serializers import UserSignupSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny


class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to access

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)  # Logs the user in
            token, _ = Token.objects.get_or_create(user=user)  # Creates token for API authentication
            return Response({"token": token.key, "message": "Login successful!"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


User = get_user_model()


class SignupView(CreateAPIView):
    serializer_class = UserSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def welcome(request):
    return render(request, "welcome.html")


def signup(request):
    return render(request, "signup.html")


def login_view(request):
    return render(request, "login.html")
