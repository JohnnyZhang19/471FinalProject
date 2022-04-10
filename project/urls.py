from django.urls import path, re_path
from . import views

app_name = 'project'
urlpatterns = [
    #user register url
    path("register/", views.register, name='register'),
    path("login/", views.login, name='login'),
    path("logout/", views.logout, name='logout'),
    path("", views.homepageView.as_view(), name='homepage'),
    re_path('archives/(?P<month>[0-9]{1,2})/(?P<year>[0-9]{4})/', views.archives, name='archives'),
    re_path('category/(?P<categoryid>[0-9]+)/', views.categoryView.as_view(), name='category'),
    re_path('tags/(?P<tagid>[0-9]+)/', views.tagView.as_view(), name='tags'),
    re_path('authorPage/(?P<userid>[0-9]+)/', views.authorPage.as_view(), name='authorPage'),
    re_path('blogDetail/(?P<blogid>[0-9]+)/', views.blogDetail.as_view(), name='blogDetail')
]
