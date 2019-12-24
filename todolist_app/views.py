from django.shortcuts import render, redirect
from django.http import HttpResponse
from todolist_app.models import TaskList
from todolist_app.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        form.save(commit=False).manager = request.user
        form.save()
        messages.success(request, ('New task Added!'))
        return redirect('todolist')
    else:        
        all_tasks = TaskList.objects.filter(manager=request.user)
        paginator = Paginator(all_tasks, 5)
        page = request.GET.get('pg')
        all_tasks = paginator.get_page(page)

        return render(request, 'app.html', {'all_tasks': all_tasks, 'title_of_page': "TodoList"})

@login_required
def delete_task(request, task_id):
    task = TaskList.objects.get(pk = task_id)

    if task.manager==request.user:
        task.delete()
        return redirect('todolist')
    else:
        messages.error(request, ('Access Denied'))

@login_required
def edit_task(request, task_id):
    if request.method == "POST":
        task = TaskList.objects.get(pk = task_id)
        form = TaskForm(request.POST or None, instance= task)
        form.save()

        messages.success(request, ('Task Edited!'))
        return redirect('todolist')
    else:        
        task_obj = TaskList.objects.get(pk = task_id)   
        return render(request, 'edit.html', {'task_obj': task_obj, 'title_of_page':"Edit Task"})

@login_required
def complete_task(request, task_id):
    task = TaskList.objects.get(pk = task_id)
    if task.manager==request.user:
        if task.done == True:
            task.done = False
        else:
            task.done = True
        task.save()
    else:
        messages.error(request, ('Access Denied'))

    return redirect ('todolist')

def contact(request):
    context = {
        'welcome_text':"Welcome to Contact us",
        'title_of_page':"Contact Us",
    }
    return render(request, 'contact.html', context)

def about(request):
    context = {
        'welcome_text':"Welcome to About us",
        'title_of_page':"About Us",
    }
    return render(request, 'about.html', context)

def homepage(request):
    return render(request, 'homepage.html')