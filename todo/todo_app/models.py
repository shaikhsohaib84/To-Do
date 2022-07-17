from statistics import mode
from django.db import models

# Create your models here.
class ToDoUser(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    name = models.CharField(max_length=20, blank=False, null=False)
    email = models.EmailField(max_length=120, blank=False, null=False, unique=True)
    password = models.TextField(max_length=255, blank=False, null=False)

    class Meta:
        db_table = 'toDoUser'
    
    def __str__(self):
        return f"Created user - {self.name}"

class Task(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    title = models.CharField(max_length=150, unique=True, null=False, blank=False)
    user = models.ForeignKey(ToDoUser, on_delete=models.CASCADE)

    class Meta:
        db_table = 'task'

    def __str__(self):
        return f"{self.title} -Task added for User - {self.user.name}"

class SubTask(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    class Meta:
        db_table = 'subTask'
        
    def __str__(self):
        return f"{self.task.title} created on {self.created_date}"