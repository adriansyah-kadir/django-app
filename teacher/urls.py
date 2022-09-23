from django.urls import path
from . import handler

app_name = "teacher"

urlpatterns = [path("register/", handler.Register.as_view(), name="register")]
