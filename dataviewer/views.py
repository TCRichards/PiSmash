from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("<h2>Welcome to Pi Smash Dot Com!</h2>")