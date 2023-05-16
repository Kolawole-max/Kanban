from django.urls import path
from . import views

urlpatterns = [
    path("logout", views.logout_, name="logout_"),
    path("", views.home, name="home"),
    path("login", views.login_ ,name="login"),
    path("register", views.register, name='register'),
    path("change_password", views.change_password, name="change_password"),
    path("createproject", views.create_project, name="create_project"),
    path("createtasks/<str:project_id>", views.create_task_post, name="create_task_post"),
    path("addtask/<str:project_id>", views.create_task, name="create_task"), 
    path("project/<str:project_id>", views.display_task, name="display_task"), 
    path("task/<str:task_id>", views.task_page, name='task_page'),
    path("edittask/<str:task_id>", views.edittask, name='edittask'),
    
    ### API ###
    path("comment/<str:task_id>", views.comment, name='comment'),
    path("priority/<str:task_id>", views.priority, name='priority'),
    path("status/<str:task_id>", views.xStatus, name='status'),
    path("role", views.xUserType, name='xrole'),
    path("hour", views.estimate_hour, name='hour'),
]