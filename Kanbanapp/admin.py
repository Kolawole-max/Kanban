from django.contrib import admin
from .models import *

class Project(admin.ModelAdmin):
    list_display = ("id", "name", "start_date", "end_date", "created_at", "updated_at")
    
class Task(admin.ModelAdmin):
    list_display = ("id", "project_id", "name", "description", "priority", "status_id", "estimate_hours", "progress_hours")
    
class Comment(admin.ModelAdmin):
    list_display = ("id", "user_id", "task_id", "description", "created_at", "updated_at")
    
class Status(admin.ModelAdmin):
    list_display = ("id", "name")
    
class Prioritys(admin.ModelAdmin):
    list_display = ("id", "name")
    
    
class role(admin.ModelAdmin):
    list_display = ("id", "name")
    
class user(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email", "role_id")


# Register your models here.
admin.site.register(Role, role)
admin.site.register(Users, user)
admin.site.register(Projects, Project)
admin.site.register(Project_roles)
admin.site.register(Tasks, Task)
admin.site.register(Comments, Comment)
admin.site.register(Statues, Status)
admin.site.register(Priority, Prioritys)