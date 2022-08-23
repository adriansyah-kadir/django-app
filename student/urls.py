from django.urls import path
from . import handler

app_name = "student"
urlpatterns = [path("register/", handler.RegisterView.as_view(), name="register")]
