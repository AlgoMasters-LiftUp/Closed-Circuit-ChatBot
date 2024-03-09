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

from django.contrib import messages
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
            
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                home_url = reverse('chatbot_app:home')
                return redirect(home_url)
            else:
                messages.add_message(message = "Email or password is wrong. Try again...")
                return render(request, 'login_register.html')
        else:
            messages.add_message("Form type is not as expected.")
            return render(request, 'login_register.html')
        
    form = SignupForm()
    return render(request, 'login_register.html', {'form': form})


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
                messages.add_message(message = form_error)
                return render(request, 'login_register.html', {'form': form})
                
        else:
            form = SignupForm()  
            messages.add_message(message = 'form type is not as expected')
            return render(request, 'deneme.html', {'form': form})
        
    form = SignupForm()
    return render(request, 'login_register.html', {'form': form} )




#  if user is not None:
#         login(request,user)
#         return Response({'ok':'True'},status=status.HTTP_200_OK)
#     else:
#         return Response({'ok':'False'},status=status.HTTP_401_UNAUTHORIZED)