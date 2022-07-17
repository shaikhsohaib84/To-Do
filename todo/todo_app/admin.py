from django.contrib import admin
from .models import ToDoUser, Task, SubTask

# Register your models here.
admin.site.register(ToDoUser)
admin.site.register(Task)
admin.site.register(SubTask)