from django.urls import path
from . import views

app_name = 'chatbot_app'

urlpatterns = [
    path("", views.home), 
	path("home", views.home, name="home"), 
	path("home/handlePrompt", views.handlePrompt, name="handlePrompt"), 
]

