from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


@login_required(login_url="users:login")
def subscription_list(request: HttpRequest) -> HttpResponse:
    return render(request, "subscription/subscriptions.html")


@login_required(login_url="users:login")
def create_subscription(request: HttpRequest) -> HttpResponse:
    return render(request, "subscription/create_subscription.html")
