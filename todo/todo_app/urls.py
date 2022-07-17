from django.urls import re_path as url
from .views import UserSignUp, UserLoginIn

urlpatterns = [
    url('^signup/$', UserSignUp.as_view()),
    url('^login/$', UserLoginIn.as_view())
]