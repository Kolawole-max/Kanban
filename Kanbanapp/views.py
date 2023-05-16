from asyncio import tasks
from asyncio.windows_events import NULL
import json
from unicodedata import name
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.urls import reverse
from django.db import IntegrityError
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


@login_required  
def customers_only(request):
    if request.user.role_id.name != 'Customers':
        raise PermissionDenied()
    
def admin_only(request):
    if request.user.role_id.name != 'Administrators':
        raise PermissionDenied()
    #Project Managers Developers Customer
    
def pm_admin(request):
    if request.user.role_id.name != 'Administrators' and request.user.role_id.name != 'Project Managers':
        raise PermissionDenied()
    
def devs(request):
    if request.user.role_id.name == 'Customers':
        raise PermissionDenied()


# Create your views here.

# --------------------- Landing page --------------------- #
def home(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect('login')
    
    projects = Projects.objects.all
    
    ## Control home page base on user type 
    return render(request, "Kanbanapp/home.html", {
        'projects' : projects
    }) 




# ----------------------------------- Login page ------------------- #
def login_(request):
    if request.method == "POST":
        
        # Attempt to login
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
       
        else:
            return render(request, "Kanbanapp/login.html", {
                'message' : email + password
            }) 
        
    else:
        return render(request, "Kanbanapp/login.html")
    
    
# ------------------------ Logout -----------------------#
def logout_(request):
    logout(request)
    return redirect('login');


# --------------------   CREATE USER -------------------- #
def register(request):
    if request.method == 'POST':
        
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            role = Role.objects.get(id=1)
            user = Users.objects.create_user(password=password, email=email, first_name=firstname, last_name = lastname, username=email)
            user.role_id = role
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        
        except IntegrityError: 
            return render(request, "Kanbanapp/register.html", {
                "message": 'Error in registration, please try again.'
            })
    else: 
        return render(request, "Kanbanapp/register.html")
    

# --------------------   Change Password -------------------- #
def change_password(request):
    
    if request.user.is_authenticated:
        
        username = request.user.username
        if request.method == 'POST':
            
            old_password = request.POST['old_password']
            new_password = request.POST['new_password']
            
            user = authenticate(request, username=username, password=old_password)
            
            if user is not None:
                user = Users.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                login(request, user)
                return redirect('home')
            else:
                return render(request, "Kanbanapp/change_password.html", {
                    'message' : 'Incorrect old password'
                })
        else:
            return render(request, "Kanbanapp/change_password.html")   
    else:
        return redirect('login')   


# --------------------- Create projects --------------------- #
@login_required 
def create_project(request): #### Authorise Administrator only ####
    
    admin_only(request)
    if request.method == 'POST':
        name = request.POST['name']
        slug = request.POST['slug']
        description = request.POST['description']
        end_date = request.POST['end_date']
        
        project = Projects.objects.create(name=name, slug=slug, description=description, end_date=end_date, created_at=datetime.now, updated_at=datetime.now)
        project.save()
        return redirect('home')
                    
    else:
        return render(request, 'Kanbanapp/create_project.html')


# --------------------- display tasks --------------------- #
@login_required 
def display_task(request, project_id):
    if request.user.is_authenticated:
        
        project = Projects.objects.get(id=project_id)
        tasks = Tasks.objects.filter(project_id=project.id)
        priorities = Priority.objects.all
        
        return render(request, 'Kanbanapp/task_board.html', {
            'tasks' : tasks,
            'project' : project,
            'project_id' : project_id,
            'priorities' : priorities
        })
        
    else:
        return redirect('login') 


# --------------------- Get create task page --------------------- #        

@login_required 
def create_task(request, project_id): #### Authorise PM and Administrator ####
     
    pm_admin(request=request)
    users = Users.objects.exclude(id=request.user.id)
    project = Projects.objects.get(id=project_id)
    
    return render(request, 'Kanbanapp/create_task.html', {
        'project' : project,
        'users' : users
    })
        
    
# --------------------- Post new task --------------------- #

@login_required 
def create_task_post(request, project_id):#### Authorise PM and Administrator ####
    
    pm_admin(request=request)
    if request.method == 'POST':
        
        current_user = request.user
        name = request.POST['name']
        description = request.POST['description']
        assignee_lst = request.POST.getlist('assignee')
        estimate_hours = request.POST['estimate_time']
        
        project_id = Projects.objects.get(id=project_id)
        status_id = Statues.objects.get(id=1)

        task = Tasks.objects.create (project_id=project_id, name=name, description=description,
                                    status_id=status_id, estimate_hours=estimate_hours, progress_hours=0)
        task.save
        task.assignee_id.add(current_user)
        task.save
        for assignee in assignee_lst:
            user = Users.objects.get(id=assignee)
            task.assignee_id.add(user)
            task.save
            
        return redirect('home')
    
    

# --------------------- edit task --------------------- #

@login_required 
def edittask(request, task_id):#### Authorise PM and Administrator ####
    
    pm_admin(request=request)
    task = Tasks.objects.get(id=task_id)
    
    if request.method == 'GET':
        
        users = Users.objects.exclude(id=request.user.id)
        return render(request, 'Kanbanapp/edittask.html', {
        'task' : task,
        'users' : users
    })
    
    name = request.POST['name']
    description = request.POST['description']
    assignee_lst = request.POST.getlist('assignee')
    estimate_hours = request.POST['estimate_time']
    
    task.name = name
    task.description = description
    task.estimate_hours = estimate_hours
    task.save
    
    for assignee in assignee_lst:
            user = Users.objects.get(id=assignee)
            task.assignee_id.add(user)
            task.save
            
    return redirect('home')
    
    
# --------------------- Task page --------------------- #

def task_page(request, task_id):
    
    if request.user.is_authenticated: #### Authorise every type of user ####
        task = Tasks.objects.get(id=task_id)
        comments = Comments.objects.filter(task_id=task)
        
        return render(request, 'Kanbanapp/task_page.html', {
            'task' : task,
            'comments' : comments,
            'estimate' : task.estimate_hours - task.progress_hours
        })
    else:
        return redirect('login')    
    
    
# ----------------- API ------------------------#

# --------------------- Add comments --------------------- #

@csrf_exempt
@login_required

def comment(request, task_id): #### Authorise every except customer ####
    
    pm_admin(request=request)
    task = Tasks.objects.get(id=task_id)
    
    data = json.loads(request.body)
    description = data.get('description', '')
    
    if request.method == 'POST':
        
        comments = Comments.objects.create(task_id=task, user_id=request.user, description=description)
        comments.save()
        
        return JsonResponse({"message": "Email sent successfully."}, status=201)
    
    elif request.method == 'DELETE':
        
        comment_id = data.get('comment_id', '')
        comment = Comments.objects.get(id=comment_id, task_id=task_id).delete()
        
        return JsonResponse({"message": "Email sent successfully."}, status=201)
    else:
        
        comment_id = data.get('comment_id', '')
        comment = Comments.objects.get(id=comment_id, task_id=task_id)
        comment.description = description
        comment.save()
        
        return JsonResponse({"message": "Email sent successfully."}, status=201)
            
            
            
            
# --------------------- change usertype --------------------- #
            
@csrf_exempt
@login_required

def xUserType(request):
    
    admin_only(request)
    if request.method == "GET":
        
        users = Users.objects.exclude(id=request.user.id)
        roles = Role.objects.all
        return render(request, 'Kanbanapp/xrole.html', {
            'users' : users,
            'roles' : roles
        })
    
    
    data = json.loads(request.body)
    role_id = data['role']
    user_id = data['user']
    
    role = Role.objects.get(id=role_id)
    user = Users.objects.get(id=user_id)
    
    user.role_id = role
    user.save()
    
    return JsonResponse({"message": "Email sent successfully."}, status=201)
    
    
@csrf_exempt
@login_required

def priority(request, task_id):
    
    customers_only(request=request)
    
    if request.method == "PUT":
    
        data = json.loads(request.body)
        priority_id = data['priority']
        
        task = Tasks.objects.get(id=task_id)
        priority = Priority.objects.get(id=priority_id)
        
        task.priority = priority
        task.save()
        
        return JsonResponse({"message": "Email sent successfully."}, status=201)
    else:
        return None
    
@csrf_exempt
@login_required

def xStatus(request, task_id):
    devs(request=request)
    
    if request.method == 'PUT':
        
        data = json.loads(request.body)
        status_id = data['status']
        
        task = Tasks.objects.get(id=task_id)
        status = Statues.objects.get(id= int(status_id) + 1)
        
        task.status_id = status
        task.save()
        
        return JsonResponse({"message": "Email sent successfully."}, status=201)
    else:
        return None
 
@csrf_exempt
@login_required           
            
def estimate_hour(request):
    devs(request=request)
    
    if request.method == 'PUT':
        
        data = json.loads(request.body)
        
        new_progress = data.get('new_progress', '')
        task_id = data.get('task_id', '')
        
        task = Tasks.objects.get(id=task_id)
        new_progress = float(new_progress) + task.progress_hours
        task.progress_hours = new_progress
        task.save()
        
        return JsonResponse({"message": "Email sent successfully."}, status=201)
    else:
        return None