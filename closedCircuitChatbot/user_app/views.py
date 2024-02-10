from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'login_register.html')

def login(request):
    return render(request, 'deneme.html') # chatbot/home.html

def register(request):
    return render(request, 'deneme.html')