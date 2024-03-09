from django.urls import path
from . import views

app_name = 'chatbot_app'

urlpatterns = [
    path("", views.home, name="home"), 
	path("home", views.home, name="home"), 
]

