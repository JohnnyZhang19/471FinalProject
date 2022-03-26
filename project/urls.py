from django.urls import path
from . import views

app_name = 'project'
urlpatterns = [
    #user register url
    path("register/", views.register, name = 'register'),
    path("login/", views.login, name='login'),
    path("logout/", views.logout, name='logout')
]