from django.conf import settings
from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.api.v1.serializers import UserSerializer
from users.models import User


class Register(APIView):
    def post(self, request: HttpRequest) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class Login(APIView):
    def post(self, request: HttpRequest) -> Response:
        email = request.data["email"]
        password = request.data["password"]

        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({"error": "Invalid email or password"}, status=400)

        if not user.check_password(password):
            return Response({"error": "Invalid email or password"}, status=400)

        login(request, user)

        refresh_token = RefreshToken.for_user(user)

        response = Response({"message": "Login successful"}, status=200)
        response.set_cookie(
            key="refresh_token",
            value=str(refresh_token),
            expires=settings.REFRESH_TOKEN_EXPIRE_TIME,
        )
        response.set_cookie(
            key="access_token",
            value=str(refresh_token.access_token),
            expires=settings.ACCESS_TOKEN_EXPIRE_TIME,
        )
        return response


class Logout(APIView):
    def post(self, request: HttpRequest) -> Response:
        logout(request)

        response = Response({"message": "Logout successful"}, status=200)
        response.delete_cookie("refresh_token")
        response.delete_cookie("access_token")

        return response
