from django.urls import re_path as url
from .views import (
    UserSignUp, 
    UserLoginIn, 
    CreateTask,
    CreateSubTask,
    GetAllTask,
    GetSubTask,
    UpdateTask,
    UpdateSubTask,
    DeleteTask,
    DeleteSubTask,
    TaskNotification
    )

urlpatterns = [
    url(r'^signup/$', UserSignUp.as_view()),
    url(r'^login/$', UserLoginIn.as_view()),
    url(r'^create-task/$', CreateTask.as_view()),
    url(r'^create-sub-task/$', CreateSubTask.as_view()),
    url(r'^get-all-task/$', GetAllTask.as_view()),
    url(r'^get-sub-task/$', GetSubTask.as_view()),
    url(r'^update-task/$', UpdateTask.as_view()),
    url(r'^update-sub-task/$', UpdateSubTask.as_view()),
    url(r'^delete-task/(?P<taskId>.+)/$', DeleteTask.as_view()),
    url(r'^delete-sub-task/(?P<subTaskId>.+)/$', DeleteSubTask.as_view()),
    url(r'^task-notification/$', TaskNotification.as_view()),
]