from django.contrib import admin

from .models import RegisterUser, Category, Tag, Bloginfo


class BloginfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_time', 'modified_time', 'category', 'author', 'views')

admin.site.register(RegisterUser)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Bloginfo, BloginfoAdmin)

