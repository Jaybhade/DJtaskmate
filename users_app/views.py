from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomRegisterForm

# Create your views here.
def register(request):
    if request.method=='POST':
        register_form = CustomRegisterForm(request.POST)
        register_form.save()
        messages.success(request, ('Successfully Registered!'))
        return redirect('todolist')
    else:
        register_form = CustomRegisterForm()
        return render (request, 'register.html', {'register_form': register_form, 'title_of_page': 'Register'})