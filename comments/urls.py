from django.urls import path
from . import views

app_name = 'comments'
urlpatterns = [

    path('blogComment/<int:blogid>/', views.do_comments, name='blogComment')
]
