
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views 
from django.conf import settings
from django.conf.urls.static import static
from user_app import views as user_app
from chatbot_app import views as chatbot_app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_app.urls'), name="user_app"),
    path("user/", include('user_app.urls'), name="user_app"),
    path("botai/", include('chatbot_app.urls'), name="chatbot_app"),
]
