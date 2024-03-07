from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token  
from django.contrib.auth.models import User  
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage  
from django.apps import apps

from django.contrib.auth.models import Group 
# Create your views here.

def index(request):
    form = SignupForm()  
    return render(request, 'login_register.html', {'form': form} )

def login(request):
    return render(request, 'chatbot/home.html') 

# email verification 
# sending email to the user
def register(request):
    if request.method == 'POST':  

        form_type = request.POST.get('form_type', None)

        if form_type == 'Register': # buttons name is checking
            username = request.POST.get('first_name', None) + "_" + request.POST.get('last_name', None)
            data = {
                'username': username,
                'first_name': request.POST.get('first_name', None),
                'last_name': request.POST.get('last_name', None),
                'email': request.POST.get('email', None),
                'password1': request.POST.get('password1', None),
                'password2': request.POST.get('password2', None)
            }
            form = SignupForm(data)  
            if form.is_valid():  

                user = form.save(commit=False)  
                # user.is_active = False  
                user.username = username 
                user.save()
            else:
                form_error = form.errors
                form = SignupForm()
                return render(request, 'deneme.html', {'form': form, 'error':form_error})
                
        else:
            form = SignupForm()  
            return render(request, 'deneme.html', {'form': form, 'error':'form type is not as expected'})
    form = SignupForm()
    return render(request, 'login_register.html')

