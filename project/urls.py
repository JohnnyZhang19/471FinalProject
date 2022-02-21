from django.urls import path
from . import views
urlpatterns = [
    #user register url
    path("register/", views.register, name = 'register')
]