from django.shortcuts import render, redirect
from django.contrib import messages
from .RAGconfig import RAG

rag = RAG()


def home(request):
    # if request.user.is_authenticated and request.user.groups.filter(name="ClientUserGroup").exists():
        
    #     return render(request, 'home.html') 
    # else:
    #     return render(request, 'login_register.html')
    return render(request, 'home.html') 


def deneme(request):
    context = {}
    return render(request, 'deneme.html', context) 

def handlePrompt(request):    
    if request.method == 'POST':  

        form_type = request.POST.get('user_prompt_form', None)

        if form_type == 'user_prompt_ready':
            prompt = request.POST.get('user_prompt', None)

            rag_rsp = rag.ragQA(prompt)
            response = rag_rsp["answer"]
            index = response.find("Assistant:")
            if index != -1:
                human_part = response[index:]
            else:
                human_part=  "Cevap bulunamadı."
            
            if prompt:
                messages.success(request=request,message=f"prompt: {prompt}")
                messages.success(request=request,message=f"response: {human_part}")
            else:
                messages.error(request=request,message=f"prompt yok")
        
            return redirect("chatbot_app:home")
        else:
            return redirect("chatbot_app:home")
    else:
        return render(request, 'login_register.html')
    

    