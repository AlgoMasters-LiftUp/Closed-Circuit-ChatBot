from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from . import authentication
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

def Login(request):
    if request.method == 'POST':  

        form_type = request.POST.get('form_type', None)

        if form_type == 'Login':
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            # Call the EmailAuthBackend class and its authenticate method
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                home_url = reverse('chatbot_app:home')
                return redirect(home_url)
            else:
                return render(request, 'deneme.html', {"error":"user is none"})
        
        return render(request, 'deneme.html', {"error":"form type is not login"})
    return render(request, 'deneme.html', {"error":"it is not post"})
    
#  if user is not None:
#         login(request,user)
#         return Response({'ok':'True'},status=status.HTTP_200_OK)
#     else:
#         return Response({'ok':'False'},status=status.HTTP_401_UNAUTHORIZED)

def Register(request):
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

