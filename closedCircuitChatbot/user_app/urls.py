from django.urls import path
from . import views


urlpatterns = [
	path("", views.index), #herhangi bir sayfaya geçmeden kaynaktan gönderim 
	path("index", views.index),
	path("login", views.login, name="login"),
	path("register", views.register, name="register"), 
]

