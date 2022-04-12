from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.utils.html import strip_tags


class RegisterUser(AbstractUser):
    # user information, extend admin.auth.user
    nickname = models.CharField(max_length=32, verbose_name="Nickname")

    telephone = models.CharField(max_length=13, null=True, unique=True, verbose_name='888-888-8888')

    profile_photo = models.ImageField(upload_to='profile_photo', null=True, blank=True, verbose_name='profile photo')

    def __str__(self):
        return self.username

    class Meat:
        verbose_name = "user information form"
        verbose_name_plural = verbose_name


class Category(models.Model):
    #category name
    name = models.CharField(max_length=20, verbose_name="Category name")
    #category describe
    describe = models.CharField(max_length=100, verbose_name="describe", null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "project category form"
        verbose_name_plural = verbose_name

class Tag(models.Model):
    #tag name
    name = models.CharField(max_length=20, verbose_name="Tag name")
    #tag describe
    describe = models.CharField(max_length=100, verbose_name="describe", null=True)

    def __str__(self):
        return self.name + "(" + self.describe + ")"

    class Meta:
        verbose_name = "project tag form"
        verbose_name_plural = verbose_name

class Bloginfo(models.Model):
    #Blog title
    title = models.CharField(max_length=50, verbose_name="project title")

    #project body
    body = RichTextUploadingField(verbose_name="project body")

    #create time
    created_time = models.DateTimeField(verbose_name="created time")

    #last edit time
    modified_time = models.DateTimeField(verbose_name="last modified time")

    #excerpt
    excerpt = models.CharField(max_length=200, blank=True, verbose_name="project excerpt")

    #category
    #1 to n relation
    #on_delete CASECADA means, when delete category, all the relation project will be delete too
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="category")

    #tag
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="project tags")

    #author
    author = models.ForeignKey(RegisterUser, on_delete=models.CASCADE, verbose_name="author")

    #viewd times
    views = models.IntegerField(default=0, verbose_name="views")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("project:blogDetail", kwargs={'blogid': self.id})

    def add_one_view(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.excerpt:
            self.excerpt = strip_tags(self.body)[:100]

        # call father's save
        super(Bloginfo, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_time']
        verbose_name = "project form"
        verbose_name_plural = verbose_name





