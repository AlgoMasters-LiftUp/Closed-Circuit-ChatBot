from django.urls import path
from . import views


urlpatterns = [
	path("", views.index), #herhangi bir sayfaya geçmeden kaynaktan gönderim 
	path("index", views.index),
	path("Login", views.login, name="Login"),
	path("Register", views.register, name="Register"), 
]

