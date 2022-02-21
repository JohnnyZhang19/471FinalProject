from django.db import models
from django.contrib.auth.models import AbstractUser


class RegisterUser(AbstractUser):
    # user information, extend admin.auth.user
    nickname = models.CharField(max_length=32, verbose_name="Nickname")

    telephone = models.CharField(max_length=13, null=True, unique=True, verbose_name='888-888-8888')

    profile_photo = models.ImageField(upload_to='profile_photo', null=True, blank=True, verbose_name='profile photo')

    def __str__(self):
        return self.username

    class Meat:
        verbase_name = "user information form"
        verbose_name_plural = verbase_name