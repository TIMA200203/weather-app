from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def login(request: HttpRequest) -> HttpResponse:
    return render(request, "users/login.html")


def register(request: HttpRequest) -> HttpResponse:
    return render(request, "users/register.html")
