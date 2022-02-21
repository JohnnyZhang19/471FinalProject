from django.contrib.auth.models import auth
from django.shortcuts import render, redirect

from . import forms
from . import models


def register(request):
    if request.method == 'POST':
        """
        user register view method
        """
        form_obj = forms.reg_form(request.POST, request.FILES)
        if form_obj.is_valid():
            #confirm password
            form_obj.cleaned_data.pop('repassword')
            #use django to create a new user, and store the data that entered in the web to our database
            user_obj = models.RegisterUser.objects.create_user(**form_obj.cleaned_data, is_staff=1, is_superuser=1)

            #auto login after register
            auth.login(request, user_obj)

            #jump to the main page
            return redirect("/")
        else:
            return render(request, "project/register.html", {'formobj': form_obj})

    else:
        #combine the forms.py with the webpage
        form_obj = forms.reg_form()
        return render(request, "project/register.html",{'formobj': form_obj})


