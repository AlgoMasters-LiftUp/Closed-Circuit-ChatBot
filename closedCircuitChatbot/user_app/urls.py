from django.urls import path
from . import views
from chatbot_app import views as chatbot_views


urlpatterns = [
	path("", views.index), #herhangi bir sayfaya geçmeden kaynaktan gönderim 
	path("index", views.index),
	path("Login", views.Login, name="Login"),
	path("Register", views.Register, name="Register"), 
]

