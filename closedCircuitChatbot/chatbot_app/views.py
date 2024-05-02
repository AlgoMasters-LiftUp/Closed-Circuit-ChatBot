from django.shortcuts import render, redirect

# Create your views here.


def home(request):
    # if request.user.is_authenticated and request.user.groups.filter(name="ClientUserGroup").exists():
        
    #     return render(request, 'home.html') 
    # else:
    #     return render(request, 'login_register.html')
    return render(request, 'home.html') 


def handlePrompt(request):
    if request.method == 'POST':  

        form_type = request.POST.get('user_prompt_form', None)

        if form_type == 'user_prompt_ready':
            prompt = request.POST.get('user_prompt', None)
            context = {}
            if prompt:
                context.update({"prompt": prompt})
            else:
                context.update({"prompt": "prompt yok"})
            context.update({"bidi":"bidi"})
        
            return render(request, 'deneme.html', context) 
        else:
            return redirect("home")
    else:
        return redirect("home")
    