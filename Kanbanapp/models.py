from asyncio import Task
from datetime import datetime
from turtle import mode
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

#--------------- Create your models here. --------------------------

class Role(models.Model):
    name = models.TextField(null=False, blank=False, max_length=364)
    
    def __str__(self):
        return f" {self.name}"

class Users(AbstractUser):
    role_id = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL, blank=True)
    email_verified = models.BooleanField(default=False)
    remember_token = models.BooleanField(default=False)
    
    def __str__(self):
        return f" {self.first_name} {self.last_name}"

class Projects(models.Model):
    name = models.TextField(null=False, blank=False, max_length=364)
    slug = models.TextField(null=False, blank=False, max_length=364)
    description = models.TextField(null=False, blank=False, max_length=364)
    start_date = models.DateField(blank=False, default=timezone.now())
    end_date = models.DateField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f" {self.name}"

class Statues(models.Model):
    name = models.TextField(null=False, blank=False, max_length=364)
    
    def __str__(self):
        return f" {self.name}"

class Priority(models.Model):
    name = models.TextField(null=False, blank=False, max_length=364)
    
    def __str__(self):
        return f" {self.name}"


#######################


class Project_roles(models.Model):
    project_id = models.OneToOneField(Projects, null=True, on_delete=models.SET_NULL)
    user_id = models.ForeignKey(Users, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    
class Tasks(models.Model):
    project_id = models.ForeignKey(Projects, null=True, on_delete = models.SET_NULL)
    name = models.TextField(null=False, blank=False, max_length=364)
    description = models.TextField(null=False, blank=False, max_length=364)
    assignee_id = models.ManyToManyField(Users, null=True)
    priority = models.ForeignKey(Priority, blank=True, null=True, on_delete=models.SET_NULL)
    status_id = models.ForeignKey(Statues, null=True, on_delete=models.SET_NULL)
    estimate_hours = models.FloatField(blank=False)
    progress_hours = models.FloatField(blank=False) 
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f" {self.name}"


class Comments(models.Model):
    user_id = models.ForeignKey(Users, null=True, on_delete=models.SET_NULL)
    task_id = models.ForeignKey(Tasks, null=True, on_delete=models.SET_NULL, related_name='task_comment')
    description = models.TextField(null=False, blank=False, max_length=364)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f" {self.description}"
    
    def serialize(self):
        return {
            'id' : self.id,
            'user' : self.user_id.id,
            'task' : self.task_id.id,
            'description': self.description
        }