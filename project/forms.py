
from django import forms
from django.core.exceptions import ValidationError
from . import models

class reg_form(forms.Form):
    # <input type = 'text'/>
    username = forms.CharField(
        max_length=20,
        label="username",
        error_messages={
            "max_length" : "username must in 20 character",
            "required": "username cannot be empty"
        },
        widget=forms.widgets.TextInput(
            attrs={'class': "form-control"},
        )
    )

    # <input type = 'password'/>
    password = forms.CharField(
        max_length=20,
        label="password",
        error_messages={
            "min_length": "password must larger than 6 character",
            "required": "password cannot be empty"
        },
        # let the input type to password as *
        widget=forms.widgets.PasswordInput(
            attrs={'class': "form-control"},
        )
    )

    repassword = forms.CharField(
        max_length=20,
        label="confirm",
        error_messages={
            "min_length": "password must larger than character",
            "required": "password cannot be empty"
        },
        # let the input type to password as *
        widget=forms.widgets.PasswordInput(
            attrs={'class': "form-control"},
        )
    )

    nickname=forms.CharField(
        max_length=20,
        label="nickname",
        error_messages={
            "max_length": "nickname must in 20 character"
        },
        # initial=username,
        widget=forms.widgets.TextInput(
            attrs={'class': "form-control"},
        )
    )

    email=forms.EmailField(
        label="email",
        error_messages={
            "invalid": "please enter a right email",
            "required": "email cannot be empty"
        },
        widget = forms.widgets.EmailInput(
            attrs={'class': "form-control"},
        )
    )

    telephone = forms.CharField(
        label="mobile",
        required=False,
        error_messages={
            'max_length': "telephone number must be 11 character"
        },
        widget = forms.widgets.TextInput(
            attrs={'class': "form-control"},
        )
    )

    profile_photo = forms.ImageField(
        label="profile photo",
        widget=forms.widgets.FileInput(
            attrs={'style': "display:none"},
        )

    )

    #confirm password and repassword are the same
    def clean_repassowrd(self):
        passwd=self.cleaned_data.get('password')
        repasswd=self.cleaned_data.get('password')
        if repasswd and repasswd != passwd:
            self.add_error("repassword", ValidationError("the password you entered twice are not the same"))
        else:
            return repasswd

    #check if the username already exist
    def clean_username(self):
        input_username = self.cleaned_data.get('username')

        #ORM
        user = models.RegisterUser.objects.filter(username = input_username)
        if user:
            self.add_error("username", ValidationError("The username already exist, please try another one"))
        else:
            return input_username










