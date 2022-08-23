from django.urls import path
from . import handler

app_name='class'
urlpatterns=[
    path('<id>/', handler.ClassView.as_view(), name='detail'),
    path('register/', handler.ClassRegister.as_view(), name='register')
]
