from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.db import IntegrityError
from .forms import TaskCreateForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm,
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error' : 'El usuario ya existe en la base de datos'
        })
        else:
            return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error' : 'Las contraseñas no coinciden'
        })

@login_required
def tasks(request):
    encabezado = 'Tareas Pendientes'
    tasks = Task.objects.filter(user=request.user, datacompleted__isnull=True)
    return render(request, 'tasks.html',{'tasks' : tasks,'encabezado':encabezado})

@login_required
def tasks_complete(request):
    encabezado = 'Tareas Completadas'
    tasks = Task.objects.filter(user=request.user, datacompleted__isnull=False)
    return render(request, 'tasks.html',{'tasks' : tasks,'encabezado':encabezado})

@login_required
def create_task(request):#otra manera de validar si la peticion es GET o POST
    #import pdb;pdb.set_trace()
    if request.method == 'POST':
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        else:
            form = TaskCreateForm()
            return render(request, 'create_task.html',{
                    'form' : form,
                    'error' : 'Datos no validos, verificar'
            })
    else:
        form = TaskCreateForm()
        return render(request, 'create_task.html',{
                'form' : form
        })

@login_required
def task_detail(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task,pk=task_id,user=request.user)
        form = TaskCreateForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')
        else:
            #task = Task.objects.get(pk=task_id)
            task = get_object_or_404(Task,pk=task_id,user=request.user)
            form = TaskCreateForm(instance=task)
            error = 'Datos no validos, Verificar'
            return render(request, 'task_detail.html',{'task':task,'form':form,'error':error})
    else:
        #task = Task.objects.get(pk=task_id)
        task = get_object_or_404(Task,pk=task_id,user=request.user)
        form = TaskCreateForm(instance=task)
        return render(request, 'task_detail.html',{'task':task,'form':form})

@login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task,pk=task_id,user=request.user)
    if request.method == 'POST':
        task.datacompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required   
def task_delete(request, task_id):
    task = get_object_or_404(Task,pk=task_id,user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method=='GET':
        return render(request, 'signin.html',{
            'form' : AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',{
            'form' : AuthenticationForm,
            'error' : 'Usuario o contraseñas incorrecto'
        })
        else:
            login(request, user)
            return redirect('tasks')