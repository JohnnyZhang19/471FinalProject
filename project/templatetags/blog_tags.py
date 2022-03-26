from django import template
from ..models import Bloginfo, Category, Tag
from django.db.models.aggregates import Count

register = template.Library()

@register.simple_tag
def get_newest_blogs():
    #get the newest 5 blogs
    return Bloginfo.objects.all().order_by("-created_time")[:5]

@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_blogs=Count('bloginfo')).filter(num_blogs__gt=0)


@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_blogs=Count('bloginfo')).filter(num_blogs__gt=0)


@register.simple_tag
def get_archives():
    return Bloginfo.objects.dates('created_time', 'month', order='DESC')